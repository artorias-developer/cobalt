from os import environ
from pathlib import Path
from asyncio import create_subprocess_exec
from asyncio.subprocess import PIPE, STDOUT
from codecs import getincrementaldecoder
from tempfile import TemporaryDirectory
from typing import Dict, Optional, Any, List, AsyncGenerator, Union, Tuple, Literal
from urllib.parse import quote

from orjson import dumps

from domain.exceptions import (
    NotFoundError,
    UnexpectedError
)
from application.contracts.clients import AbstractContainersClient
from application.contracts.clients import AbstractSocketClient
from application.clients.sockets.shared import (
    SocketError,
    SocketResponse
)
from application.clients.containers.shared import (
    ContainerLog,
    ContainerStatus
)


class ContainerHandle:
    """
    Lightweight container reference returned by "container_list". Exposes the same "show" and "delete"
    methods the cleanup code uses.
    """
    id: str
    names: List[str]

    def __init__(
        self,
        client: "DockerClient",
        container_id: str,
        names: List[str]
    ):
        self._client = client

        self.id = container_id
        self.names = names

    async def show(self) -> Dict[str, Any]:
        """
        Gets the full container inspect.

        Parameters:
        - None.

        Returns:
        - Dict: Container inspect.
        """
        return await self._client._container_inspect(self.id)

    async def delete(
        self,
        force: bool = False,
        v: bool = False
    ) -> None:
        """
        Removes the container.

        Parameters:
        - force: Force removal of running container.
        - v: Remove associated volumes.

        Returns:
        - None.
        """
        await self._client.container_remove(
            container_name=self.id,
            force=force,
            volumes=v
        )


class DockerClient(AbstractContainersClient):
    """
    Docker client. Talks to the Docker Engine API through a socket client, images are built with "docker build"
    CLI, because the BuildKit builder is only available there (the HTTP build endpoint needs a gRPC session for it).
    """
    _BUILD_ERROR_TAIL = 3000
    _BUILD_FLAGS = {
        "nocache": "--no-cache",
        "pull": "--pull"
    }
    _BUILD_OPTIONS = {
        "target": "--target",
        "platform": "--platform",
        "network": "--network"
    }

    socket_client: AbstractSocketClient
    socket_path: str
    docker_cli: str

    def __init__(
        self,
        socket_client: AbstractSocketClient,
        socket_path: str = "/var/run/docker.sock",
        docker_cli: str = "docker"
    ):
        self.socket_client = socket_client
        self.socket_path = socket_path
        self.docker_cli = docker_cli

    async def initialize(self) -> None:
        """
        Open the underlying socket client session and prepare the client for use. Should be called on
        application startup if the client isn't used as an async context manager.

        Parameters:
        - None.

        Returns:
        - None.
        """
        await self.socket_client.initialize()

    async def close(self) -> None:
        """
        Close the underlying socket client session and free its connections. Should be called on application
        shutdown if the client wasn't used as an async context manager.

        Parameters:
        - None.

        Returns:
        - None.
        """
        await self.socket_client.close()

    async def _call(
        self,
        path: str,
        error: UnexpectedError,
        method: Literal["GET", "POST", "PUT", "PATCH", "DELETE"] = "GET",
        ok: Tuple[int, ...] = (200,),
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Any] = None,
        not_found: Optional[NotFoundError] = None
    ) -> SocketResponse:
        """
        Performs a request and maps the failures to domain exceptions.

        Parameters:
        - path: Request path.
        - error: Exception raised on connection errors and unexpected statuses.
        - method: HTTP method.
        - ok: Statuses considered successful.
        - params: Query params.
        - json: JSON body.
        - not_found: Exception raised on 404, if it is expected.

        Returns:
        - SocketResponse: Successful response.
        """
        try:
            response = await self.socket_client.request(
                path=path,
                method=method,
                params=params,
                json=json
            )
        except SocketError as e:
            raise error from e

        if response.status in ok:
            return response

        if response.status == 404 and not_found is not None:
            raise not_found

        raise error

    async def _container_inspect(
        self,
        container_name: str
    ) -> Dict[str, Any]:
        """
        Gets the container inspect by name or ID.

        Parameters:
        - container_name: Container name or ID.

        Returns:
        - Dict: Container inspect.
        """
        response = await self._call(
            path=f"/containers/{quote(container_name, safe='')}/json",
            error=UnexpectedError('Error while inspecting container "{name}"', name=container_name),
            not_found=NotFoundError('Container "{name}" not found', name=container_name)
        )

        return response.json()

    async def image_build(
        self,
        context_path: Path,
        container_file: Optional[str] = None,
        tag: Optional[str] = None,
        build_args: Optional[Dict[str, Any]] = None,
        labels: Optional[Dict[str, str]] = None,
        **kwargs: Any
    ) -> str:
        """
        Builds the image from containerfile using "docker build" with BuildKit.

        Parameters:
        - context_path: Path to build context.
        - container_file: Container file to build, relative to the context.
        - tag: Image tag.
        - build_args: Build arguments.
        - labels: Image labels.
        - **kwargs: Build options: nocache, pull, target, platform, network.

        Returns:
        - str: Built image ID or tag.
        """
        unknown = set(kwargs) - set(self._BUILD_FLAGS) - set(self._BUILD_OPTIONS)

        if unknown:
            raise ValueError(f"Unsupported build options: {', '.join(sorted(unknown))}")

        with TemporaryDirectory() as temp_dir:
            iid_file = Path(temp_dir) / "image.id"

            command = [
                self.docker_cli,
                "build",
                "--progress=plain",
                "--iidfile", str(iid_file)
            ]

            if container_file:
                command += ["--file", str(Path(context_path) / container_file)]

            if tag:
                command += ["--tag", tag]

            for key, value in (build_args or {}).items():
                command += ["--build-arg", f"{key}={value}"]

            for key, value in (labels or {}).items():
                command += ["--label", f"{key}={value}"]

            for key, flag in self._BUILD_FLAGS.items():
                if kwargs.get(key):
                    command.append(flag)

            for key, flag in self._BUILD_OPTIONS.items():
                if kwargs.get(key):
                    command += [flag, str(kwargs[key])]

            command.append(str(context_path))

            env = {
                **environ,
                "DOCKER_BUILDKIT": "1",
                "DOCKER_HOST": f"unix://{self.socket_path}"
            }

            try:
                process = await create_subprocess_exec(
                    *command,
                    stdout=PIPE,
                    stderr=STDOUT,
                    env=env
                )

                output, _ = await process.communicate()
            except OSError as e:
                raise UnexpectedError(
                    'Error while building image "{tag}": cannot run "{cli}"',
                    tag=tag,
                    cli=self.docker_cli
                ) from e

            if process.returncode != 0:
                tail = output.decode("utf-8", errors="replace")[-self._BUILD_ERROR_TAIL:]

                raise UnexpectedError(
                    'Error while building image "{tag}":\n{output}',
                    tag=tag,
                    output=tail
                )

            image_id = iid_file.read_text().strip() if iid_file.exists() else None

        return image_id or tag

    async def image_remove(
        self,
        image: str,
        force: bool = False,
        no_prune: bool = False
    ) -> None:
        """
        Removes docker image.

        Parameters:
        - image: Image name or ID
        - force: Force remove even if used
        - no_prune: Do not delete untagged parents
        """
        await self._call(
            path=f"/images/{quote(image, safe='/:@')}",
            method="DELETE",
            params={
                "force": force,
                "noprune": no_prune
            },
            error=UnexpectedError('Error while removing image "{image}"', image=image),
            not_found=NotFoundError('Image "{image}" not found', image=image)
        )

    async def image_prune(
        self,
        filters: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Prunes images by filters.

        Parameters:
        - filters: Filters to apply.

        Returns:
        - None.
        """
        await self._call(
            path="/images/prune",
            method="POST",
            params={
                "filters": dumps(filters).decode() if filters else None
            },
            error=UnexpectedError("Error while pruning images")
        )

    async def container_list(
        self,
        all_containers: bool = False,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Any]:
        """
        Lists containers by filters.

        Parameters:
        - all_containers: Get all the containers.
        - filters: Filters to apply.

        Returns:
        - List: List of container objects.
        """
        response = await self._call(
            path="/containers/json",
            params={
                "all": all_containers,
                "filters": dumps(filters).decode() if filters else None
            },
            error=UnexpectedError("Error while listing containers")
        )

        return [
            ContainerHandle(
                client=self,
                container_id=item["Id"],
                names=[name.lstrip("/") for name in item.get("Names", [])]
            )
            for item in response.json()
        ]

    async def container_create(
        self,
        image: str,
        name: Optional[str] = None,
        ports: Optional[Dict[int, int]] = None,
        volumes: Optional[Dict[str, Dict[str, str]]] = None,
        environment: Optional[Dict[str, str]] = None,
        labels: Optional[Dict[str, str]] = None,
        command: Optional[Union[str, List[str]]] = None,
        entrypoint: Optional[List[str]] = None,
        **kwargs: Any
    ) -> None:
        """
        Creates the container without starting it.

        Parameters:
        - image: Image name or ID.
        - name: Container name.
        - ports: Port mappings {container_port: host_port}.
        - volumes: Volume mappings {host_path: {'bind': container_path, 'mode': 'rw'}}.
        - environment: Environment variables.
        - labels: Container labels.
        - command: Command to run.
        - entrypoint: Entrypoint override.
        - **kwargs: Keyword arguments.

        Returns:
        - None.
        """
        config = {
            "Image": image,
            "AttachStdin": kwargs.get("stdin_open", False),
            "AttachStdout": True,
            "AttachStderr": True,
            "Tty": kwargs.get("tty", False),
            "OpenStdin": kwargs.get("stdin_open", False),
            "StdinOnce": False,
            "HostConfig": {
                "RestartPolicy": {
                    "Name": kwargs.get("restart_policy", "unless-stopped")
                },
                "StopTimeout": kwargs.get("stop_grace_period", 30),
                "Init": kwargs.get("init", False)
            }
        }

        if name:
            config["Hostname"] = name

        if ports:
            port_bindings = {}

            for container_port, host_port in ports.items():
                if isinstance(container_port, str) and "/" in container_port:
                    key = container_port
                else:
                    key = f"{container_port}/tcp"

                port_bindings[key] = [{"HostPort": str(host_port)}]

            config["HostConfig"]["PortBindings"] = port_bindings

        if volumes:
            binds = []

            for host_path, vol_config in volumes.items():
                container_path = vol_config.get("bind", vol_config)
                mode = vol_config.get("mode", "rw") if isinstance(vol_config, dict) else "rw"
                binds.append(f"{host_path}:{container_path}:{mode}")

            config["HostConfig"]["Binds"] = binds

        if environment:
            config["Env"] = [f"{k}={v}" for k, v in environment.items()]

        if labels:
            config["Labels"] = labels

        if command:
            config["Cmd"] = command if isinstance(command, list) else ["/bin/sh", "-c", command]

        if entrypoint:
            config["Entrypoint"] = entrypoint

        if "security_opt" in kwargs:
            config["HostConfig"]["SecurityOpt"] = kwargs["security_opt"]

        if "network_mode" in kwargs:
            config["HostConfig"]["NetworkMode"] = kwargs["network_mode"]

        if "config_variables" in kwargs:
            config.update(kwargs["config_variables"])

        await self._call(
            path="/containers/create",
            method="POST",
            params={
                "name": name
            },
            json=config,
            ok=(201,),
            error=UnexpectedError('Error while creating container "{name}"', name=name)
        )

    async def container_start(
        self,
        container_name: str
    ) -> None:
        """
        Starts the existing container.

        Parameters:
        - container_name: Container name.

        Returns:
        - None.
        """
        await self._call(
            path=f"/containers/{quote(container_name, safe='')}/start",
            method="POST",
            ok=(204, 304),
            error=UnexpectedError('Error while starting container "{name}"', name=container_name),
            not_found=NotFoundError('Container "{name}" not found', name=container_name)
        )

    async def container_stop(
        self,
        container_name: str,
        timeout: int = 60
    ) -> None:
        """
        Stops the running container.

        Parameters:
        - container_name: Container name.
        - timeout: Seconds to wait before forceful stop.

        Returns:
        - None.
        """
        await self._call(
            path=f"/containers/{quote(container_name, safe='')}/stop",
            method="POST",
            params={
                "t": timeout
            },
            ok=(204, 304),
            error=UnexpectedError('Error while stopping container "{name}"', name=container_name),
            not_found=NotFoundError('Container "{name}" not found', name=container_name)
        )

    async def container_remove(
        self,
        container_name: str,
        force: bool = False,
        volumes: bool = False
    ) -> None:
        """
        Removes the container.

        Parameters:
        - container_name: Container name.
        - force: Force removal of running container.
        - volumes: Remove associated volumes.

        Returns:
        - None.
        """
        await self._call(
            path=f"/containers/{quote(container_name, safe='')}",
            method="DELETE",
            params={
                "force": force,
                "v": volumes
            },
            ok=(204,),
            error=UnexpectedError('Error while removing container "{name}"', name=container_name),
            not_found=NotFoundError('Container "{name}" not found', name=container_name)
        )

    async def container_restart(
        self,
        container_name: str,
        timeout: int = 60
    ) -> None:
        """
        Restarts the container.

        Parameters:
        - container_name: Container name.
        - timeout: Seconds to wait before forceful restart.

        Returns:
        - None.
        """
        await self._call(
            path=f"/containers/{quote(container_name, safe='')}/restart",
            method="POST",
            params={
                "t": timeout
            },
            ok=(204,),
            error=UnexpectedError('Error while restarting container "{name}"', name=container_name),
            not_found=NotFoundError('Container "{name}" not found', name=container_name)
        )

    async def container_wait(
        self,
        container_name: str
    ) -> None:
        """
        Waits for the container to stop.

        Parameters:
        - container_name: Container name.

        Returns:
        - None.
        """
        await self._call(
            path=f"/containers/{quote(container_name, safe='')}/wait",
            method="POST",
            error=UnexpectedError('Error while waiting for container "{name}"', name=container_name),
            not_found=NotFoundError('Container "{name}" not found', name=container_name)
        )

    @staticmethod
    async def _iter_log_lines(
        chunks: AsyncGenerator[bytes, None],
        tty: bool
    ) -> AsyncGenerator[str, None]:
        """
        Turns the raw logs stream into text lines. Without TTY the stream is multiplexed: every frame is an
        8-byte header (stream type, 3 zero bytes, big-endian payload size) followed by the payload.

        Parameters:
        - chunks: Raw chunks of the logs stream.
        - tty: Whether the container has a TTY, then the stream is plain.

        Returns:
        - AsyncGenerator: Lines with their trailing newline.
        """
        decoder = getincrementaldecoder("utf-8")(errors="replace")
        buffer = bytearray()
        text = ""

        async for chunk in chunks:
            payloads = []

            if tty:
                payloads.append(chunk)
            else:
                buffer.extend(chunk)

                while len(buffer) >= 8:
                    size = int.from_bytes(buffer[4:8], "big")

                    if len(buffer) < 8 + size:
                        break

                    payloads.append(bytes(buffer[8:8 + size]))
                    del buffer[:8 + size]

            for payload in payloads:
                text += decoder.decode(payload)

                while (index := text.find("\n")) != -1:
                    yield text[:index + 1]
                    text = text[index + 1:]

        text += decoder.decode(b"", final=True)

        if text:
            yield text

    async def container_logs(
        self,
        container_name: str,
        tail: int = 300,
        timestamps: bool = False
    ) -> List[ContainerLog]:
        """
        Gets the container logs.

        Parameters:
        - container_name: Container name.
        - tail: Number of lines from end.
        - timestamps: Show timestamps.

        Returns:
        - List: List of ContainerLog objects.
        """
        error = UnexpectedError('Error while getting logs for container "{name}"', name=container_name)

        inspect = await self._container_inspect(container_name)
        tty = inspect.get("Config", {}).get("Tty", False)

        try:
            return [
                ContainerLog(message=line)
                async for line in self._iter_log_lines(
                    chunks=self.socket_client.stream(
                        path=f"/containers/{quote(container_name, safe='')}/logs",
                        params={
                            "stdout": True,
                            "stderr": True,
                            "follow": False,
                            "tail": tail,
                            "timestamps": timestamps
                        }
                    ),
                    tty=tty
                )
            ]
        except SocketError as e:
            if e.status == 404:
                raise NotFoundError('Container "{name}" not found', name=container_name) from e

            raise error from e

    async def container_stream_logs(
        self,
        container_name: str,
        tail: int = 0,
        timestamps: bool = False
    ) -> AsyncGenerator[ContainerLog, Any]:
        """
        Streams the container logs in real-time.

        Parameters:
        - container_name: Container name.
        - tail: Number of lines from end to start with.
        - timestamps: Show timestamps.

        Returns:
        - AsyncGenerator: ContainerLog object.
        """
        inspect = await self._container_inspect(container_name)
        tty = inspect.get("Config", {}).get("Tty", False)

        try:
            async for line in self._iter_log_lines(
                chunks=self.socket_client.stream(
                    path=f"/containers/{quote(container_name, safe='')}/logs",
                    params={
                        "stdout": True,
                        "stderr": True,
                        "follow": True,
                        "tail": tail,
                        "timestamps": timestamps
                    }
                ),
                tty=tty
            ):
                yield ContainerLog(
                    message=line
                )
        except SocketError as e:
            if e.status == 404:
                raise NotFoundError('Container "{name}" not found', name=container_name) from e

            raise UnexpectedError(
                'Error while streaming logs for container "{name}"',
                name=container_name
            ) from e

    async def container_status(
        self,
        container_name: str
    ) -> ContainerStatus:
        """
        Gets the container status.

        Parameters:
        - container_name: Container name.

        Returns:
        - ContainerStatus: ContainerStatus object.
        """
        inspect = await self._container_inspect(container_name)

        running = inspect["State"]["Running"]

        host_port = None
        port_bindings = inspect.get("HostConfig", {}).get("PortBindings") or {}

        for bindings in port_bindings.values():
            if bindings:
                host_port = int(bindings[0]["HostPort"])
                break

        return ContainerStatus(
            running=running,
            port=host_port
        )

    async def container_execute(
        self,
        container_name: str,
        command: List[str]
    ) -> None:
        """
        Executes a command inside the container.

        Parameters:
        - container_name: Container name.
        - command: Command to execute.

        Returns:
        - None.
        """
        error = UnexpectedError('Error while executing command in container "{name}"', name=container_name)

        created = await self._call(
            path=f"/containers/{quote(container_name, safe='')}/exec",
            method="POST",
            json={
                "Cmd": command,
                "AttachStdout": True,
                "AttachStderr": True
            },
            ok=(201,),
            error=error,
            not_found=NotFoundError('Container "{name}" not found', name=container_name)
        )

        await self._call(
            path=f"/exec/{created.json()['Id']}/start",
            method="POST",
            json={
                "Detach": True,
                "Tty": False
            },
            error=error
        )

    async def volume_prune(
        self,
        filters: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Prunes volumes by filters.

        Parameters:
        - filters: Filters to apply.

        Returns:
        - None.
        """
        await self._call(
            path="/volumes/prune",
            method="POST",
            params={
                "filters": dumps(filters).decode() if filters else None
            },
            error=UnexpectedError("Error while pruning volumes")
        )

    async def builder_prune(
        self,
        reserved_space: Optional[int] = None,
        max_used_space: Optional[int] = None,
        min_free_space: Optional[int] = None,
        all_cache: bool = False,
        filters: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Prunes the builder cache.

        Parameters:
        - reserved_space: Amount of disk space in bytes to keep for cache.
        - max_used_space: Maximum amount of disk space allowed to keep for cache.
        - min_free_space: Target amount of free disk space after pruning.
        - all_cache: Remove all types of build cache.
        - filters: Filters to apply.

        Returns:
        - None.
        """
        await self._call(
            path="/build/prune",
            method="POST",
            params={
                "reserved-space": reserved_space,
                "max-used-space": max_used_space,
                "min-free-space": min_free_space,
                "all": all_cache or None,
                "filters": dumps(filters).decode() if filters else None
            },
            error=UnexpectedError("Error while pruning builder cache")
        )
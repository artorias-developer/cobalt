#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from io import BytesIO
from pathlib import Path
from tarfile import open as tarfile_open
from typing import Dict, Optional, Any, List, AsyncGenerator, Union, Callable

from aiodocker import Docker
from aiodocker.containers import DockerContainer
from aiodocker.exceptions import DockerError
from orjson import dumps

from domain.exceptions import (
    NotFoundError,
    UnexpectedError
)
from application.contracts.managers import AbstractI18nManager
from application.contracts.clients import AbstractContainersClient
from application.clients.containers.shared import (
    ContainerLog,
    ContainerStatus
)


class DockerClient(AbstractContainersClient):
    """
    Docker client.
    """
    i18n_manager: AbstractI18nManager

    _: Callable
    _client: Docker

    def __init__(
        self,
        i18n_manager: AbstractI18nManager
    ):
        self.i18n_manager = i18n_manager

        self._ = i18n_manager.gettext

    async def initialize(self) -> None:
        """
        Initializes the client.

        Parameters:
        - None.

        Returns:
        - None.
        """
        self._client = Docker()

    async def close(self) -> None:
        """
        Closes the Docker client.

        Parameters:
        - None.

        Returns:
        - None.
        """
        await self._client.close()

    async def _get_container_by_name(
        self,
        name: str
    ) -> DockerContainer:
        """
        Gets container by name from Docker API.

        Parameters:
        - name: Container name.

        Returns:
        - Container object.
        """
        try:
            containers = await self._client.containers.list(all=True)

            for container in containers:
                container_names = container._container.get("Names", [])

                if any(container_name.lstrip('/') == name for container_name in container_names):
                    return container

        except DockerError as e:
            raise UnexpectedError(self._('Error while getting container "{name}"').format(name=name)) from e

        raise NotFoundError(self._('Container "{name}" not found').format(name=name))

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
        Builds the image from containerfile.

        Parameters:
        - context_path: Path to build context.
        - container_file: Container file to build.
        - tag: Image tag.
        - build_args: Build arguments.
        - labels: Image labels.
        - **kwargs: Keyword arguments.

        Returns:
        - str: Built image ID or tag.
        """
        try:
            tar_obj = BytesIO()

            with tarfile_open(fileobj=tar_obj, mode='w') as tar:
                tar.add(context_path, arcname='.')

            tar_obj.seek(0)

            params = {
                "rm": True,
                **kwargs
            }

            if container_file:
                params["path_dockerfile"] = container_file

            if tag:
                params["tag"] = tag

            if build_args:
                params["buildargs"] = build_args

            if labels:
                params["labels"] = labels

            build_log = []
            build_result = await self._client.images.build(fileobj=tar_obj, encoding="application/x-tar", **params)

            for line in build_result:
                build_log.append(line)

            image_id = None

            for line in reversed(build_log):
                if "aux" in line and "ID" in line["aux"]:
                    image_id = line["aux"]["ID"]
                    break

            return image_id or tag

        except DockerError as e:
            raise UnexpectedError(self._('Error while building image "{tag}"').format(tag=tag)) from e

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
        try:
            await self._client.images.delete(
                name=image,
                force=force,
                noprune=no_prune
            )
        except DockerError as e:
            raise UnexpectedError(self._('Error while removing image "{image}"').format(image=image)) from e

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
        try:
            await self._client.images.prune(
                filters=filters or {}
            )
        except DockerError as e:
            raise UnexpectedError(self._('Error while pruning images')) from e

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
        try:
            return await self._client.containers.list(
                all=all_containers,
                filters=filters or {}
            )
        except DockerError as e:
            raise UnexpectedError(self._('Error while listing containers')) from e

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
        try:
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

            await self._client.containers.create(
                config=config,
                name=name
            )
        except DockerError as e:
            raise UnexpectedError(self._('Error while creating container "{name}"').format(name=name)) from e

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
        try:
            container = await self._get_container_by_name(container_name)
            await container.start()
        except (NotFoundError, UnexpectedError):
            raise
        except DockerError as e:
            raise UnexpectedError(self._('Error while starting container "{name}"').format(name=container_name)) from e

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
        try:
            container = await self._get_container_by_name(container_name)
            await container.stop(timeout=float(timeout))
        except (NotFoundError, UnexpectedError):
            raise
        except DockerError as e:
            raise UnexpectedError(self._('Error while stopping container "{name}"').format(name=container_name)) from e

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
        try:
            container = await self._get_container_by_name(container_name)
            await container.delete(force=force, v=volumes)
        except (NotFoundError, UnexpectedError):
            raise
        except DockerError as e:
            raise UnexpectedError(self._('Error while removing container "{name}"').format(name=container_name)) from e

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
        try:
            container = await self._get_container_by_name(container_name)
            await container.restart(timeout=timeout)
        except (NotFoundError, UnexpectedError):
            raise
        except DockerError as e:
            raise UnexpectedError(self._('Error while restarting container "{name}"').format(name=container_name)) from e

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
        try:
            container = await self._get_container_by_name(container_name)
            await container.wait()
        except (NotFoundError, UnexpectedError):
            raise
        except DockerError as e:
            raise UnexpectedError(self._('Error while waiting for container "{name}"').format(name=container_name)) from e

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
        try:
            container = await self._get_container_by_name(container_name)

            logs = await container.log(
                stdout=True,
                stderr=True,
                follow=False,
                tail=tail,
                timestamps=timestamps
            )

            return [
                ContainerLog(message=log)
                for log in logs
            ]
        except (NotFoundError, UnexpectedError):
            raise
        except DockerError as e:
            raise UnexpectedError(self._('Error while getting logs for container "{name}"').format(name=container_name)) from e

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
        try:
            container = await self._get_container_by_name(container_name)

            async for log in container.log(
                stdout=True,
                stderr=True,
                follow=True,
                tail=tail,
                timestamps=timestamps
            ):
                yield ContainerLog(
                    message=log
                )
        except (NotFoundError, UnexpectedError):
            raise
        except DockerError as e:
            raise UnexpectedError(self._('Error while streaming logs for container "{name}"').format(name=container_name)) from e

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
        try:
            container = await self._get_container_by_name(container_name)
            inspect = await container.show()

            running = inspect["State"]["Running"]

            host_port = None
            port_bindings = inspect.get("HostConfig", {}).get("PortBindings", {})

            for bindings in port_bindings.values():
                if bindings:
                    host_port = int(bindings[0]["HostPort"])
                    break

            return ContainerStatus(
                running=running,
                port=host_port
            )
        except (NotFoundError, UnexpectedError):
            raise
        except DockerError as e:
            raise UnexpectedError(self._('Error while getting status for container "{name}"').format(name=container_name)) from e

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
        try:
            container = await self._get_container_by_name(container_name)

            exec_obj = await container.exec(
                cmd=command,
                stdout=True,
                stderr=True
            )

            await exec_obj.start(
                detach=True
            )
        except (NotFoundError, UnexpectedError):
            raise
        except DockerError as e:
            raise UnexpectedError(self._('Error while executing command in container "{name}"').format(name=container_name)) from e

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
        try:
            await self._client.volumes.prune(
                filters=filters or {}
            )
        except DockerError as e:
            raise UnexpectedError(self._("Error while pruning volumes")) from e

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
        try:
            params = {}

            if reserved_space is not None:
                params["reserved-space"] = str(reserved_space)

            if max_used_space is not None:
                params["max-used-space"] = str(max_used_space)

            if min_free_space is not None:
                params["min-free-space"] = str(min_free_space)

            if all_cache:
                params["all"] = "1"

            if filters:
                params["filters"] = dumps(filters)

            await self._client._query_json(
                "build/prune",
                method="POST",
                params=params
            )
        except DockerError as e:
            raise UnexpectedError(self._("Error while pruning builder cache")) from e
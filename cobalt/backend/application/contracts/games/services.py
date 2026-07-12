#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from os import path
from re import compile
from abc import ABC, abstractmethod
from pathlib import Path
from secrets import choice
from string import ascii_letters, digits
from socket import socket, AF_INET, SOCK_STREAM, SOCK_DGRAM
from typing import Optional, Dict, Any, Union

from aiofiles import os, open
from aioshutil import rmtree

from domain.enums import ServerStateEnum
from domain.exceptions import NotFoundError
from application.contracts.managers import AbstractConnectionsManager
from application.contracts.clients import AbstractContainersClient
from application.contracts.services import AbstractServersService as CoreServersService
from application.contracts.loggers import AbstractLogger
from application.clients.containers.shared import ContainersConstants
from application.managers.events.shared import ServersEventsEnum
from application.managers.connections.shared import RoomsConstants
from application.dtos import ServerUpdateDto


class AbstractServersService(ABC):
    """
    Abstract server service.
    """
    _CONTAINER_INSTALLER_FILE = "Container.installer"
    _CONTAINER_RUNTIME_FILE = "Container.runtime"
    _CONTAINER_UPGRADER_FILE = "Container.upgrader"
    _STEAM_BUILD_ID_PATTERN = compile(r'"buildid"\s+"(\d+)"')

    build_dir: Path
    app_containers_dir: Path
    core_servers_service: CoreServersService
    containers_client: AbstractContainersClient
    connections_manager: AbstractConnectionsManager
    logger: AbstractLogger

    def __init__(
        self,
        build_dir: Path,
        app_containers_dir: Path,
        core_servers_service: CoreServersService,
        containers_client: AbstractContainersClient,
        connections_manager: AbstractConnectionsManager,
        logger: AbstractLogger
    ):
        self.build_dir = build_dir
        self.app_containers_dir = app_containers_dir
        self.core_servers_service = core_servers_service
        self.containers_client = containers_client
        self.connections_manager = connections_manager
        self.logger = logger

    async def _remove_container(
        self,
        container_name: str
    ) -> None:
        """
        Removes an existing server container.

        Parameters:
        - container_name: Container name.

        Returns:
        - None.
        """
        try:
            await self.containers_client.container_remove(
                container_name=container_name,
                force=True,
                volumes=True
            )
        except NotFoundError:
            pass
        except Exception:
            self.logger.exception(f'Error while removing container "{container_name}":')

    async def _remove_image(
        self,
        image_name: str
    ) -> None:
        """
        Removes an existing server image.

        Parameters:
        - image_name: Image name.

        Returns:
        - None.
        """
        try:
            await self.containers_client.image_remove(
                image=image_name,
                force=True
            )
        except NotFoundError:
            pass
        except Exception:
            self.logger.exception(f'Error while removing image "{image_name}":')

    async def _cleanup_container_resources(
        self,
        container_name: str
    ) -> None:
        """
        Removes a container and its associated image.

        Parameters:
        - container_name: Container name (also used as image name).

        Returns:
        - None.
        """
        await self._remove_container(
            container_name=container_name
        )

        await self._remove_image(
            image_name=container_name
        )

    async def _update_server_state(
        self,
        server_id: int,
        state: Optional[ServerStateEnum] = None,
        version: Optional[str] = None,
        with_container_status: bool = False
    ) -> None:
        """
        Updates server and sends new data to all subscribers.

        Parameters:
        - server_id: Server ID.
        - state: Server state.
        - version: Server version.
        """
        request_dto = ServerUpdateDto(
            state=state,
            version=version
        )

        await self.core_servers_service.update_one(
            server_id=server_id,
            dto=request_dto
        )

        server_data = {
            "server_id": server_id
        }

        if state is not None:
            server_data["state"] = state

        if version is not None:
            server_data["version"] = version

        if with_container_status:
            container_name = ContainersConstants.GAME_CONTAINER_NAME_KEY.format(
                server_id=server_id
            )

            try:
                status = await self.containers_client.container_status(
                    container_name=container_name
                )
            except Exception:
                status = None

            if status is not None:
                server_data["running"] = status.running

        await self.connections_manager.send_to_room(
            room_name=RoomsConstants.SERVERS_STATUSES_KEY,
            data={
                "type": "message",
                "event": ServersEventsEnum.SERVER_STATE,
                "data": server_data
            }
        )

    @staticmethod
    def _is_port_free(
        port: int
    ) -> bool:
        """
        Checks whether a single port is currently free for both TCP and UDP.

        Parameters:
        - port: Port number to check.

        Returns:
        - bool: True if the port is free on both protocols, False otherwise.
        """
        try:
            with socket(AF_INET, SOCK_STREAM) as tcp_sock:
                tcp_sock.bind(('', port))
        except OSError:
            return False

        try:
            with socket(AF_INET, SOCK_DGRAM) as udp_sock:
                udp_sock.bind(('', port))
        except OSError:
            return False

        return True

    def _is_port_range_free(
        self,
        start_port: int,
        count: int
    ) -> bool:
        """
        Checks whether every port in [start_port, start_port + count - 1]
        is currently free for both TCP and UDP.

        Parameters:
        - start_port: First port of the range to check.
        - count: Number of consecutive ports to check.

        Returns:
        - bool: True if all ports in the range are free, False otherwise.
        """
        return all(
            self._is_port_free(start_port + offset)
            for offset in range(count)
        )

    async def _create_container_dir(
        self,
        container_name: str
    ) -> None:
        """
        Creates a server container directory.

        Parameters:
        - container_name: Container name.

        Returns:
        - None.
        """
        app_container_dir = path.join(self.app_containers_dir, container_name)

        await os.makedirs(
            name=app_container_dir,
            exist_ok=True
        )

    async def _remove_container_dir(
        self,
        container_name: str
    ) -> None:
        """
        Removes an existing server container directory.

        Parameters:
        - container_name: Container name.

        Returns:
        - None.
        """
        app_container_dir = path.join(self.app_containers_dir, container_name)

        if await os.path.exists(app_container_dir):
            try:
                await rmtree(app_container_dir)
            except Exception:
                self.logger.exception(f'Error while removing files "{container_name}":')

    async def _verify_installation(
        self,
        container_name: str,
        installation_marker: str
    ) -> None:
        """
        Verifies that the installation was completed successfully.

        Parameters:
        - container_name: Container name.
        - installation_marker: File or directory that indicates a successful installation.

        Returns:
        - None.
        """
        app_container_dir = path.join(self.app_containers_dir, container_name)

        if not await os.path.exists(path.join(app_container_dir, installation_marker)):
            raise Exception(f'Installation failed: "{installation_marker}" not found in "{app_container_dir}"')

    async def _read_steam_version(
        self,
        container_name: str,
        app_id: int
    ) -> str:
        """
        Reads the installed Steam build version from the app manifest file.

        Parameters:
        - container_name: Container name.
        - app_id: Steam application ID.

        Returns:
        - str: Steam build version string.
        """
        manifest_file = path.join(
            self.app_containers_dir,
            container_name,
            "steamapps",
            f"appmanifest_{app_id}.acf"
        )

        async with open(manifest_file, "r") as f:
            content = await f.read()

        match = self._STEAM_BUILD_ID_PATTERN.search(content)

        if not match:
            return "Unknown"

        return match.group(1)

    async def _create_installer_container(
        self,
        server_id: int,
        container_name: str,
        installation_dir: str,
        installation_marker: str,
        is_steam_server: bool = False,
        steam_app_id: Optional[int] = None,
        volumes: Optional[Dict[str, Dict[str, str]]] = None,
        image_build_args: Optional[Dict[str, Any]] = None,
        image_labels: Optional[Dict[str, str]] = None,
        container_file: Optional[str] = None,
        container_environment: Optional[Dict[str, str]] = None,
        container_labels: Optional[Dict[str, str]] = None,
        image_kwargs: Optional[Dict[str, Any]] = None,
        container_kwargs: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Creates an installer container that downloads all the necessary server files.

        Parameters:
        - server_id: Server ID.
        - container_name: Container name (used as image name).
        - installation_dir: Host path to install server files into.
        - installation_marker: File or directory that indicates a successful installation.
        - is_steam_server: Whether the server is installed via Steam.
        - steam_app_id: Steam app ID, required if is_steam_server is True.
        - volumes: Additional volume mappings {host_path: {'bind': container_path, 'mode': 'rw'}}.
        - image_build_args: Image build arguments.
        - image_labels: Image labels.
        - container_file: Container file to build.
        - container_environment: Container environment variables.
        - container_labels: Container labels.
        - image_kwargs: Additional keyword arguments for image build.
        - container_kwargs: Additional keyword arguments for container create.

        Returns:
        - None.
        """
        if is_steam_server and steam_app_id is None:
            raise ValueError('The "steam_app_id" parameter is required if the value of "is_steam_server" is "True"')

        installer_name = f"{container_name}_installer"

        prepared_image_build_args = {
            "SERVER_ROOT": ContainersConstants.SERVER_ROOT,
            **({"APP_ID": str(steam_app_id)} if is_steam_server else {}),
            **(image_build_args or {})
        }

        prepared_image_labels = {
            "managed_by": ContainersConstants.MANAGED_BY,
            **(image_labels or {})
        }

        prepared_image_kwargs = {
            **(image_kwargs or {})
        }

        prepared_volumes = {
            installation_dir: {
                "bind": ContainersConstants.SERVER_ROOT,
                "mode": "rw"
            },
            **(volumes or {})
        }

        if container_file is not None:
            prepared_container_file = container_file
        else:
            prepared_container_file = self._CONTAINER_INSTALLER_FILE

        prepared_container_environment = {
            "SERVER_ROOT": ContainersConstants.SERVER_ROOT,
            **(container_environment or {})
        }

        prepared_container_labels = {
            "cobalt_server": "true",
            "managed_by": ContainersConstants.MANAGED_BY,
            **(container_labels or {})
        }

        prepared_container_kwargs = {
            **({"security_opt": ["seccomp=unconfined"]} if is_steam_server else {}),
            **(container_kwargs or {})
        }

        await self._cleanup_container_resources(
            container_name=installer_name
        )

        try:
            await self._update_server_state(
                server_id=server_id,
                state=ServerStateEnum.PROCESSING
            )

            await self._create_container_dir(
                container_name=container_name
            )

            await self.containers_client.image_build(
                context_path=self.build_dir,
                container_file=prepared_container_file,
                tag=installer_name,
                build_args=prepared_image_build_args,
                labels=prepared_image_labels,
                **prepared_image_kwargs
            )

            await self.containers_client.container_create(
                image=installer_name,
                name=installer_name,
                volumes=prepared_volumes,
                environment=prepared_container_environment,
                labels=prepared_container_labels,
                **prepared_container_kwargs
            )

            await self.containers_client.container_start(
                container_name=installer_name
            )

            await self.containers_client.container_wait(
                container_name=installer_name
            )

            await self._verify_installation(
                container_name=container_name,
                installation_marker=installation_marker
            )

            if is_steam_server:
                version = await self._read_steam_version(
                    container_name=container_name,
                    app_id=steam_app_id
                )
            else:
                version = None

            await self._update_server_state(
                server_id=server_id,
                version=version
            )
        except Exception:
            await self._remove_container_dir(
                container_name=container_name
            )

            await self._update_server_state(
                server_id=server_id,
                state=ServerStateEnum.FAILED
            )
            raise
        finally:
            await self._cleanup_container_resources(
                container_name=installer_name
            )

    async def _create_upgrader_container(
        self,
        server_id: int,
        version: str,
        container_name: str,
        installation_dir: str,
        is_steam_server: bool = False,
        steam_app_id: Optional[int] = None,
        volumes: Optional[Dict[str, Dict[str, str]]] = None,
        image_build_args: Optional[Dict[str, Any]] = None,
        image_labels: Optional[Dict[str, str]] = None,
        container_file: Optional[str] = None,
        container_environment: Optional[Dict[str, str]] = None,
        container_labels: Optional[Dict[str, str]] = None,
        image_kwargs: Optional[Dict[str, Any]] = None,
        container_kwargs: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Creates an upgrader container that upgrades existing server.

        Parameters:
        - server_id: Server ID.
        - version: Server version.
        - container_name: Container name (used as image name).
        - installation_dir: Host path with existing server files.
        - is_steam_server: Whether the server is installed via Steam.
        - steam_app_id: Steam app ID, required if is_steam_server is True.
        - volumes: Additional volume mappings {host_path: {'bind': container_path, 'mode': 'rw'}}.
        - image_build_args: Image build arguments.
        - image_labels: Image labels.
        - container_file: Container file to build.
        - container_environment: Container environment variables.
        - container_labels: Container labels.
        - image_kwargs: Additional keyword arguments for image build.
        - container_kwargs: Additional keyword arguments for container create.

        Returns:
        - None.
        """
        if is_steam_server and steam_app_id is None:
            raise ValueError('The "steam_app_id" parameter is required if the value of "is_steam_server" is "True"')

        upgrader_name = f"{container_name}_upgrader"

        prepared_image_build_args = {
            "SERVER_ROOT": ContainersConstants.SERVER_ROOT,
            **({"APP_ID": str(steam_app_id)} if is_steam_server else {}),
            **(image_build_args or {})
        }

        prepared_image_labels = {
            "managed_by": ContainersConstants.MANAGED_BY,
            **(image_labels or {})
        }

        prepared_image_kwargs = {
            **(image_kwargs or {})
        }

        prepared_volumes = {
            installation_dir: {
                "bind": ContainersConstants.SERVER_ROOT,
                "mode": "rw"
            },
            **(volumes or {})
        }

        if container_file is not None:
            prepared_container_file = container_file
        else:
            prepared_container_file = self._CONTAINER_UPGRADER_FILE

        prepared_container_environment = {
            "SERVER_ROOT": ContainersConstants.SERVER_ROOT,
            **(container_environment or {})
        }

        prepared_container_labels = {
            "cobalt_server": "true",
            "managed_by": ContainersConstants.MANAGED_BY,
            **(container_labels or {})
        }

        prepared_container_kwargs = {
            **({"security_opt": ["seccomp=unconfined"]} if is_steam_server else {}),
            **(container_kwargs or {})
        }

        await self._cleanup_container_resources(
            container_name=upgrader_name
        )

        try:
            await self.containers_client.container_stop(
                container_name=container_name
            )

            await self._update_server_state(
                server_id=server_id,
                state=ServerStateEnum.UPGRADING,
                version=version,
                with_container_status=True
            )

            await self.containers_client.image_build(
                context_path=self.build_dir,
                container_file=prepared_container_file,
                tag=upgrader_name,
                build_args=prepared_image_build_args,
                labels=prepared_image_labels,
                **prepared_image_kwargs
            )

            await self.containers_client.container_create(
                image=upgrader_name,
                name=upgrader_name,
                volumes=prepared_volumes,
                environment=prepared_container_environment,
                labels=prepared_container_labels,
                **prepared_container_kwargs
            )

            await self.containers_client.container_start(
                container_name=upgrader_name
            )

            await self.containers_client.container_wait(
                container_name=upgrader_name
            )

            await self.containers_client.container_start(
                container_name=container_name
            )

            if is_steam_server:
                version = await self._read_steam_version(
                    container_name=container_name,
                    app_id=steam_app_id
                )
            else:
                version = None

            await self._update_server_state(
                server_id=server_id,
                state=ServerStateEnum.CREATED,
                version=version,
                with_container_status=True
            )
        except Exception:
            await self._update_server_state(
                server_id=server_id,
                state=ServerStateEnum.UPGRADE_FAILED
            )
            raise
        finally:
            await self._cleanup_container_resources(
                container_name=upgrader_name
            )

    async def _create_runtime_container(
        self,
        server_id: int,
        container_name: str,
        installation_dir: str,
        ports: Dict[Union[int, str], Union[int, str]],
        is_steam_server: bool = False,
        volumes: Optional[Dict[str, Dict[str, str]]] = None,
        image_build_args: Optional[Dict[str, Any]] = None,
        image_labels: Optional[Dict[str, str]] = None,
        container_file: Optional[str] = None,
        container_environment: Optional[Dict[str, str]] = None,
        container_labels: Optional[Dict[str, str]] = None,
        image_kwargs: Optional[Dict[str, Any]] = None,
        container_kwargs: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Creates a runtime container that starts the server.

        Parameters:
        - server_id: Server ID.
        - container_name: Container name.
        - installation_dir: Host path with existing server files.
        - ports: Container ports.
        - is_steam_server: Whether the server is installed via Steam.
        - volumes: Additional volume mappings {host_path: {'bind': container_path, 'mode': 'rw'}}.
        - image_build_args: Image build arguments.
        - image_labels: Image labels.
        - container_file: Container file to build.
        - container_environment: Container environment variables.
        - container_labels: Container labels.
        - image_kwargs: Additional keyword arguments for image build.
        - container_kwargs: Additional keyword arguments for container create.

        Returns:
        - None.
        """
        prepared_image_build_args = {
            "SERVER_ROOT": ContainersConstants.SERVER_ROOT,
            **(image_build_args or {})
        }

        prepared_image_labels = {
            "managed_by": ContainersConstants.MANAGED_BY,
            **(image_labels or {})
        }

        prepared_image_kwargs = {
            **(image_kwargs or {})
        }

        prepared_volumes = {
            installation_dir: {
                "bind": ContainersConstants.SERVER_ROOT,
                "mode": "rw"
            },
            **(volumes or {})
        }

        if container_file is not None:
            prepared_container_file = container_file
        else:
            prepared_container_file = self._CONTAINER_RUNTIME_FILE

        prepared_container_environment = {
            "SERVER_ROOT": ContainersConstants.SERVER_ROOT,
            "SERVER_FIFO": ContainersConstants.SERVER_FIFO,
            **(container_environment or {})
        }

        prepared_container_labels = {
            "cobalt_server": "true",
            "managed_by": ContainersConstants.MANAGED_BY,
            **(container_labels or {})
        }

        prepared_container_kwargs = {
            "network_mode": ContainersConstants.NETWORK_MODE,
            **({"security_opt": ["seccomp=unconfined"]} if is_steam_server else {}),
            **(container_kwargs or {})
        }

        await self._cleanup_container_resources(
            container_name=container_name
        )

        try:
            await self.containers_client.image_build(
                container_file=prepared_container_file,
                context_path=self.build_dir,
                tag=container_name,
                build_args=prepared_image_build_args,
                labels=prepared_image_labels,
                **prepared_image_kwargs
            )

            await self.containers_client.container_create(
                image=container_name,
                name=container_name,
                ports=ports,
                volumes=prepared_volumes,
                environment=prepared_container_environment,
                labels=prepared_container_labels,
                stdin_open=True,
                stop_grace_period=65,
                restart_policy="unless-stopped",
                **prepared_container_kwargs
            )

            await self.containers_client.container_start(
                container_name=container_name
            )

            await self._update_server_state(
                server_id=server_id,
                state=ServerStateEnum.CREATED
            )
        except Exception:
            await self._cleanup_container_resources(
                container_name=container_name
            )

            await self._remove_container_dir(
                container_name=container_name
            )

            await self._update_server_state(
                server_id=server_id,
                state=ServerStateEnum.FAILED
            )
            raise

    def get_available_port(
        self,
        max_attempts: int = 1000
    ) -> int:
        """
        Gets a random available port that is free on both TCP and UDP.

        Parameters:
        - max_attempts: Maximum number of candidate ports to try before giving up.

        Returns:
        - int: Available port number.
        """
        for _ in range(max_attempts):
            with socket(AF_INET, SOCK_STREAM) as sock:
                sock.bind(('', 0))
                sock.listen(1)
                port: int = sock.getsockname()[1]

            if self._is_port_free(port):
                return port

        raise RuntimeError(f"Could not find an available port free on both TCP and UDP after {max_attempts} attempts")

    def get_available_port_range(
        self,
        count: int,
        max_attempts: int = 1000
    ) -> int:
        """
        Gets a starting port of a contiguous range of available ports.

        Parameters:
        - count: Number of consecutive ports required.
        - max_attempts: Maximum number of candidate ports to try before giving up.

        Returns:
        - int: The first port of a free contiguous range of size `count`.
        """
        for _ in range(max_attempts):
            with socket(AF_INET, SOCK_STREAM) as sock:
                sock.bind(('', 0))
                sock.listen(1)
                candidate: int = sock.getsockname()[1]

            if candidate + count - 1 > 65535:
                continue

            if self._is_port_range_free(candidate, count):
                return candidate

        raise RuntimeError(f"Could not find {count} consecutive available ports after {max_attempts} attempts")

    @staticmethod
    def generate_random_key(
        length: int = 32
    ) -> str:
        """
        Generates a random key.

        Parameters:
        - length: Length of the key. Defaults to 32.

        Returns:
        - str: Random cluster key string.
        """
        alphabet = ascii_letters + digits
        return ''.join(choice(alphabet) for _ in range(length))

    @abstractmethod
    async def create(
        self,
        server_id: int,
        container_name: str,
        version: str,
        download_link: Optional[str]
    ) -> None:
        """
        Creates a new server container.

        Parameters:
        - server_id: Server ID.
        - container_name: Container name.
        - version: Game version.
        - download_link: Download link.

        Returns:
        - None.
        """
        ...

    @abstractmethod
    async def upgrade(
        self,
        server_id: int,
        container_name: str,
        version: str,
        download_link: Optional[str]
    ) -> None:
        """
        Upgrades an existing server container.

        Parameters:
        - server_id: Server ID.
        - container_name: Container name.
        - version: Game version.
        - download_link: Download link.

        Returns:
        - None.
        """
        ...

    async def delete(
        self,
        container_name: str
    ) -> None:
        """
        Deletes an existing server container.

        Parameters:
        - container_name: Container name.

        Returns:
        - None.
        """
        await self._remove_container(
            container_name=container_name
        )

        await self._remove_image(
            image_name=container_name
        )

        await self._remove_container_dir(
            container_name=container_name
        )

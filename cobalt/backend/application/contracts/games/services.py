#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from os import path
from abc import ABC, abstractmethod
from pathlib import Path
from secrets import choice
from string import ascii_letters, digits
from socket import socket, AF_INET, SOCK_STREAM
from typing import Optional, Dict, Any, Union

from aiofiles import os
from aioshutil import rmtree

from application.managers.events.shared import ServersEventsEnum
from domain.enums import ServerStatusEnum
from application.contracts.managers import AbstractConnectionsManager
from application.contracts.clients import AbstractContainersClient
from application.contracts.services import AbstractServersService as CoreServersService
from application.contracts.loggers import AbstractLogger
from application.clients.containers.shared import ContainersConstants
from application.managers.connections.shared import RoomsConstants
from application.dtos import ServerUpdateDto


class AbstractServersService(ABC):
    """
    Abstract server service.
    """
    _CONTAINER_INSTALLER_FILE = "Container.installer"
    _CONTAINER_RUNTIME_FILE = "Container.runtime"

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
        except Exception:
            self.logger.exception(f'Error while removing image "{image_name}":')

    async def _remove_files(
        self,
        container_name: str
    ) -> None:
        """
        Removes an existing server files.

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

    async def _update_server_status(
        self,
        server_id: int,
        status: ServerStatusEnum
    ) -> None:
        """
        Updates server status and sends it to all subscribers.

        Parameters:
        - server_id: Server ID.
        - status: Server status.
        """
        request_dto = ServerUpdateDto(
            status=status
        )

        await self.core_servers_service.update_one(
            server_id=server_id,
            dto=request_dto
        )

        await self.connections_manager.send_to_room(
            room_name=RoomsConstants.SERVERS_STATUSES_KEY,
            data={
                "type": "message",
                "event": ServersEventsEnum.SERVER_STATUS,
                "data": {
                    "server_id": server_id,
                    "status": status
                }
            }
        )

    @staticmethod
    def get_available_port() -> int:
        """
        Gets a random available port.

        Parameters:
        - None.

        Returns:
        - int: Available port number.
        """
        with socket(AF_INET, SOCK_STREAM) as sock:
            sock.bind(('', 0))
            sock.listen(1)
            port = sock.getsockname()[1]

        return port

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
        download_link: str
    ) -> None:
        """
        Creates a new server container.

        Parameters:
        - server_id: Server ID.
        - container_name: Container name.
        - version: Game version.
        - download_link: Download link for Vanilla Terraria.

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

        await self._remove_files(
            container_name=container_name
        )

    async def _create_installer_container(
        self,
        container_file: str,
        container_name: str,
        installation_dir: str,
        image_build_args: Optional[Dict[str, Any]] = None,
        image_labels: Optional[Dict[str, str]] = None,
        container_environment: Optional[Dict[str, str]] = None,
        container_labels: Optional[Dict[str, str]] = None,
        image_kwargs: Optional[Dict[str, Any]] = None,
        container_kwargs: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Creates an installer container that downloads all the necessary server files.

        Parameters:
        - container_file: Container file to build.
        - container_name: Container name (used as image name).
        - installation_dir: Host path to install server files into.
        - image_build_args: Image build arguments.
        - image_labels: Image labels.
        - container_environment: Container environment variables.
        - container_labels: Container labels.
        - image_kwargs: Additional keyword arguments for image build.
        - container_kwargs: Additional keyword arguments for container create.

        Returns:
        - None.
        """
        installer_name = f"{container_name}_installer"
        image_created = False
        container_created = False

        prepared_image_build_args = {
            "SERVER_ROOT": ContainersConstants.SERVER_ROOT,
            **(image_build_args or {})
        }

        prepared_image_labels = {
            "managed_by": ContainersConstants.MANAGED_BY,
            **(image_labels or {})
        }

        prepared_container_environment = {
            "SERVER_ROOT": ContainersConstants.SERVER_ROOT,
            **(container_environment or {})
        }

        prepared_container_labels = {
            "cobalt_server": "true",
            "managed_by": ContainersConstants.MANAGED_BY,
            **(container_labels or {})
        }

        try:
            await self.containers_client.image_build(
                context_path=self.build_dir,
                container_file=container_file,
                tag=installer_name,
                build_args=prepared_image_build_args,
                labels=prepared_image_labels,
                **(image_kwargs or {})
            )

            image_created = True

            await self.containers_client.container_create(
                image=installer_name,
                name=installer_name,
                volumes={
                    installation_dir: {
                        "bind": ContainersConstants.SERVER_ROOT,
                        "mode": "rw"
                    }
                },
                environment=prepared_container_environment,
                labels=prepared_container_labels,
                **(container_kwargs or {})
            )

            container_created = True

            await self.containers_client.container_start(
                container_name=installer_name
            )

            await self.containers_client.container_wait(
                container_name=installer_name
            )
        finally:
            if container_created:
                await self._remove_container(
                    container_name=installer_name
                )

            if image_created:
                await self._remove_image(
                    image_name=installer_name
                )

    async def _create_runtime_container(
        self,
        container_file: str,
        container_name: str,
        ports: Dict[Union[int, str], Union[int, str]],
        volumes: Optional[Dict[str, Dict[str, str]]] = None,
        image_build_args: Optional[Dict[str, Any]] = None,
        image_labels: Optional[Dict[str, str]] = None,
        container_environment: Optional[Dict[str, str]] = None,
        container_labels: Optional[Dict[str, str]] = None,
        image_kwargs: Optional[Dict[str, Any]] = None,
        container_kwargs: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Creates a runtime container that starts the server.

        Parameters:
        - container_file: Container file to build.
        - container_name: Container name.
        - ports: Container ports.
        - volumes: Volume mappings {host_path: {'bind': container_path, 'mode': 'rw'}}.
        - image_build_args: Image build arguments.
        - image_labels: Image labels.
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

        await self.containers_client.image_build(
            container_file=container_file,
            context_path=self.build_dir,
            tag=container_name,
            build_args=prepared_image_build_args,
            labels=prepared_image_labels,
            **(image_kwargs or {})
        )

        await self.containers_client.container_create(
            image=container_name,
            name=container_name,
            ports=ports,
            volumes=volumes,
            environment=prepared_container_environment,
            labels=prepared_container_labels,
            stdin_open=True,
            stop_grace_period=65,
            restart_policy="unless-stopped",
            **(container_kwargs or {})
        )

        await self.containers_client.container_start(
            container_name=container_name
        )
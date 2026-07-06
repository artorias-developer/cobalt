#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List, Optional, Any, AsyncGenerator, Union

from application.clients.containers.shared import (
    ContainerLog,
    ContainerStatus
)


class AbstractContainersClient(ABC):
    """
    Abstract containers client for Docker, Podman, containerd and other OCI-compatible runtimes.
    """

    @abstractmethod
    async def initialize(self) -> None:
        """
        Initializes the client.

        Parameters:
        - None.

        Returns:
        - None.
        """
        ...

    @abstractmethod
    async def close(self) -> None:
        """
        Closes the Docker client.

        Parameters:
        - None.

        Returns:
        - None.
        """
        ...

    @abstractmethod
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
        ...

    @abstractmethod
    async def image_remove(
        self,
        image: str,
        force: bool = False,
        no_prune: bool = False
    ) -> None:
        """
        Removes the image.

        Parameters:
        - image: Image name or ID
        - force: Force remove even if used
        - no_prune: Do not delete untagged parents
        """
        ...

    @abstractmethod
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
        ...

    @abstractmethod
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
        ...

    @abstractmethod
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
        ...

    @abstractmethod
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
        ...

    @abstractmethod
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
        ...

    @abstractmethod
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
        ...

    @abstractmethod
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
        ...

    @abstractmethod
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
        ...

    @abstractmethod
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
        ...

    @abstractmethod
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
        ...

    @abstractmethod
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
        ...

    @abstractmethod
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
        ...

    @abstractmethod
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
        ...

    @abstractmethod
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
        ...
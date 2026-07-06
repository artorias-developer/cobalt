#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from typing import List

from fastapi import APIRouter, Depends

from domain.enums import PermissionsEnum
from application.contracts.managers import AbstractI18nManager
from application.contracts.services import (
    AbstractAuthService,
    AbstractMetricsService
)
from presentation.contracts.http.mappers import AbstractMetricsRouterMapper
from presentation.contracts.http.routers import AbstractHttpMetricsRouter
from presentation.http.fastapi.v1.routers import HttpBaseRouter
from presentation.http.fastapi.v1.schemas import (
    MetricSchema,
    MetricDiskSchema
)


class HttpMetricsRouter(AbstractHttpMetricsRouter, HttpBaseRouter):
    """
    Handles HTTP routes for metrics operations.
    """
    router: APIRouter
    metrics_service: AbstractMetricsService
    metrics_mapper: AbstractMetricsRouterMapper

    def __init__(
        self,
        router: APIRouter,
        metrics_service: AbstractMetricsService,
        metrics_mapper: AbstractMetricsRouterMapper,
        auth_service: AbstractAuthService,
        i18n_manager: AbstractI18nManager
    ):
        HttpBaseRouter.__init__(self, auth_service, i18n_manager)

        self.router = router
        self.metrics_service = metrics_service
        self.metrics_mapper = metrics_mapper

    def register(self) -> None:
        """
        Registers all handlers.

        Parameters:
        - None.

        Returns:
        - None.
        """
        router = APIRouter(
            prefix="/metrics",
            tags=["Metrics"],
            dependencies=[
                Depends(self.http_session_required)
            ]
        )

        router.add_api_route(
            path="/host/disk",
            endpoint=self.host_disk,
            methods=["GET"],
            operation_id="metrics_host_disk",
            dependencies=[
                Depends(self.http_permission_required(
                    permissions=[
                        PermissionsEnum.DASHBOARD_DISK_VIEW
                    ]
                ))
            ]
        )

        router.add_api_route(
            path="/host/cpu/last",
            endpoint=self.host_last_cpu,
            methods=["GET"],
            operation_id="metrics_host_last_cpu",
            dependencies=[
                Depends(self.http_permission_required(
                    permissions=[
                        PermissionsEnum.DASHBOARD_CPU_VIEW
                    ]
                ))
            ]
        )

        router.add_api_route(
            path="/host/ram/last",
            endpoint=self.host_last_ram,
            methods=["GET"],
            operation_id="metrics_host_last_ram",
            dependencies=[
                Depends(self.http_permission_required(
                    permissions=[
                        PermissionsEnum.DASHBOARD_RAM_VIEW
                    ]
                ))
            ]
        )

        router.add_api_route(
            path="/host/cpu/all",
            endpoint=self.host_all_cpu,
            methods=["GET"],
            operation_id="metrics_host_all_cpu",
            dependencies=[
                Depends(self.http_permission_required(
                    permissions=[
                        PermissionsEnum.DASHBOARD_CPU_VIEW
                    ]
                ))
            ]
        )

        router.add_api_route(
            path="/host/ram/all",
            endpoint=self.host_all_ram,
            methods=["GET"],
            operation_id="metrics_host_all_ram",
            dependencies=[
                Depends(self.http_permission_required(
                    permissions=[
                        PermissionsEnum.DASHBOARD_RAM_VIEW
                    ]
                ))
            ]
        )

        router.add_api_route(
            path="/servers/{server_id}/cpu/last",
            endpoint=self.server_last_cpu,
            methods=["GET"],
            operation_id="metrics_server_last_cpu",
            dependencies=[
                Depends(self.http_permission_required(
                    permissions=[
                        PermissionsEnum.SERVER_CPU_VIEW
                    ]
                ))
            ]
        )

        router.add_api_route(
            path="/servers/{server_id}/ram/last",
            endpoint=self.server_last_ram,
            methods=["GET"],
            operation_id="metrics_server_last_ram",
            dependencies=[
                Depends(self.http_permission_required(
                    permissions=[
                        PermissionsEnum.SERVER_RAM_VIEW
                    ]
                ))
            ]
        )

        router.add_api_route(
            path="/servers/{server_id}/cpu/all",
            endpoint=self.server_all_cpu,
            methods=["GET"],
            operation_id="metrics_server_all_cpu",
            dependencies=[
                Depends(self.http_permission_required(
                    permissions=[
                        PermissionsEnum.SERVER_CPU_VIEW
                    ]
                ))
            ]
        )

        router.add_api_route(
            path="/servers/{server_id}/ram/all",
            endpoint=self.server_all_ram,
            methods=["GET"],
            operation_id="metrics_server_all_ram",
            dependencies=[
                Depends(self.http_permission_required(
                    permissions=[
                        PermissionsEnum.SERVER_RAM_VIEW
                    ]
                ))
            ]
        )

        self.router.include_router(router)

    async def host_disk(
        self,
        refresh: bool = False
    ) -> MetricDiskSchema:
        """
        Gets host disk usage metrics.

        Parameters:
        - refresh: If True, bypasses cache and fetches fresh data.

        Returns:
        - MetricDiskSchema: MetricDiskSchema object.
        """
        response_dto = await self.metrics_service.host_disk(
            refresh=refresh
        )

        return self.metrics_mapper.disk_dto_to_schema(
            dto=response_dto
        )

    async def host_last_cpu(self) -> MetricSchema:
        """
        Gets last host CPU metric value.

        Parameters:
        - None.

        Returns:
        - MetricSchema: MetricSchema object.
        """
        response_dto = await self.metrics_service.host_last_cpu()

        return self.metrics_mapper.dto_to_schema(
            dto=response_dto
        )

    async def host_last_ram(self) -> MetricSchema:
        """
        Gets last host RAM metric value.

        Parameters:
        - None.

        Returns:
        - MetricSchema: MetricSchema object.
        """
        response_dto = await self.metrics_service.host_last_ram()

        return self.metrics_mapper.dto_to_schema(
            dto=response_dto
        )

    async def host_all_cpu(self) -> List[MetricSchema]:
        """
        Gets list of host CPU metrics.

        Parameters:
        - None.

        Returns:
        - List: List of MetricSchema objects.
        """
        response_dtos = await self.metrics_service.host_all_cpu()

        return self.metrics_mapper.dtos_to_schemas(
            dtos=response_dtos
        )

    async def host_all_ram(self) -> List[MetricSchema]:
        """
        Gets list of host RAM metrics.

        Parameters:
        - None.

        Returns:
        - List: List of MetricSchema objects.
        """
        response_dtos = await self.metrics_service.host_all_ram()

        return self.metrics_mapper.dtos_to_schemas(
            dtos=response_dtos
        )

    async def server_last_cpu(
        self,
        server_id: int
    ) -> MetricSchema:
        """
        Gets last server CPU metric value.

        Parameters:
        - server_id: Server ID.

        Returns:
        - MetricSchema: MetricSchema object.
        """
        response_dto = await self.metrics_service.server_last_cpu(
            server_id=server_id
        )

        return self.metrics_mapper.dto_to_schema(
            dto=response_dto
        )

    async def server_last_ram(
        self,
        server_id: int
    ) -> MetricSchema:
        """
        Gets last server RAM metric value.

        Parameters:
        - server_id: Server ID.

        Returns:
        - MetricSchema: MetricSchema object.
        """
        response_dto = await self.metrics_service.server_last_ram(
            server_id=server_id
        )

        return self.metrics_mapper.dto_to_schema(
            dto=response_dto
        )

    async def server_all_cpu(
        self,
        server_id: int
    ) -> List[MetricSchema]:
        """
        Gets list of server CPU metrics.

        Parameters:
        - server_id: Server ID.

        Returns:
        - List: List of MetricSchema objects.
        """
        response_dtos = await self.metrics_service.server_all_cpu(
            server_id=server_id
        )

        return self.metrics_mapper.dtos_to_schemas(
            dtos=response_dtos
        )

    async def server_all_ram(
        self,
        server_id: int
    ) -> List[MetricSchema]:
        """
        Gets list of server RAM metrics.

        Parameters:
        - server_id: Server ID.

        Returns:
        - List: List of MetricSchema objects.
        """
        response_dtos = await self.metrics_service.server_all_ram(
            server_id=server_id
        )

        return self.metrics_mapper.dtos_to_schemas(
            dtos=response_dtos
        )
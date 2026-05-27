#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from datetime import datetime, timedelta, timezone
from typing import Optional, List, Tuple, Dict

from application.contracts.clients import AbstractMetricsClient
from application.contracts.loggers import AbstractLogger
from application.clients.metrics.shared import MetricPoint
from infrastructure.mixins import HttpClientMixin


class PrometheusClient(AbstractMetricsClient, HttpClientMixin):
    """
    Prometheus client.
    """
    DEFAULT_INTERVAL: str = "1m"
    DEFAULT_STEP: int = 3
    DEFAULT_TIME_RANGE_MINUTES: int = 15

    base_url: str

    def __init__(
        self,
        base_url: str,
        logger: AbstractLogger,
        timeout: Optional[float] = 60.0
    ):
        HttpClientMixin.__init__(
            self,
            logger=logger,
            timeout=timeout
        )

        self.base_url = base_url.rstrip("/")

    @staticmethod
    def _build_host_cpu_query(
        interval: str
    ) -> str:
        """
        Builds PromQL query for host CPU metrics.

        Parameters:
        - interval: Query interval.

        Returns:
        - str: PromQL query.
        """
        return f'100 - (avg by (instance) (irate(node_cpu_seconds_total{{mode="idle"}}[{interval}])) * 100)'

    @staticmethod
    def _build_host_memory_query(
        interval: str
    ) -> str:
        """
        Builds PromQL query for host memory metrics.

        Parameters:
        - interval: Query interval.

        Returns:
        - str: PromQL query.
        """
        return f'avg_over_time(((1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100)[{interval}:])'

    @staticmethod
    def _build_container_cpu_query(
        interval: str,
        container: str
    ) -> str:
        """
        Builds PromQL query for container CPU metrics.
        Returns 0 if container CPU usage metric is stale (not updated recently).

        Parameters:
        - interval: Query interval.
        - container: Container name.

        Returns:
        - str: PromQL query.
        """
        return (
            f'('
            f'  (sum(irate(container_cpu_usage_seconds_total{{name="{container}"}}[{interval}]))'
            f'  / scalar(count(node_cpu_seconds_total{{mode="idle"}}))) * 100'
            f'  and on() (time() - container_last_seen{{name="{container}"}} < 30)'
            f') or on() vector(0)'
        )

    @staticmethod
    def _build_container_memory_query(
        container: str
    ) -> str:
        """
        Builds PromQL query for container memory metrics.
        Returns 0 if container memory metric is stale (not updated recently).

        Parameters:
        - interval: Query interval.
        - container: Container name.

        Returns:
        - str: PromQL query.
        """
        return (
            f'('
            f'  (container_memory_working_set_bytes{{name="{container}"}}'
            f'  / on() group_left() node_memory_MemTotal_bytes) * 100'
            f'  and on() (time() - container_last_seen{{name="{container}"}} < 30)'
            f') or on() vector(0)'
        )

    @staticmethod
    def _build_containers_cpu_query(
        interval: str,
        containers: List[str]
    ) -> str:
        """
        Builds PromQL query for multiple containers CPU metrics.
        Returns 0 for containers with stale metrics.

        Parameters:
        - interval: Query interval.
        - containers: List of container names.

        Returns:
        - str: PromQL query.
        """
        names_regex = "|".join(containers)
        return (
            f'(sum by (name) (irate(container_cpu_usage_seconds_total{{name=~"{names_regex}"}}[{interval}]))'
            f' / scalar(count(node_cpu_seconds_total{{mode="idle"}}))) * 100'
            f' and on(name) (time() - container_last_seen{{name=~"{names_regex}"}} < 30)'
        )

    @staticmethod
    def _build_containers_memory_query(
        containers: List[str]
    ) -> str:
        """
        Builds PromQL query for multiple containers memory metrics.
        Returns 0 for containers with stale metrics.

        Parameters:
        - interval: Query interval.
        - containers: List of container names.

        Returns:
        - str: PromQL query.
        """
        names_regex = "|".join(containers)
        return (
            f'('
            f'  avg by (name) (container_memory_working_set_bytes{{name=~"{names_regex}"}}'
            f'  / on() group_left() node_memory_MemTotal_bytes) * 100'
            f'  and on(name) (time() - container_last_seen{{name=~"{names_regex}"}} < 30)'
            f')'
        )

    @staticmethod
    def _round_value(
        value: Optional[float]
    ) -> float:
        """
        Rounds metric value or returns 0.0 if None.

        Parameters:
        - value: Metric value.

        Returns:
        - float: Rounded value.
        """
        return round(value, 2) if value is not None else 0.0

    def _get_time_range(self) -> Tuple[datetime, datetime]:
        """
        Returns the default start and end time for range queries.

        Parameters:
        - None.

        Returns:
        - Tuple: Start and end datetime objects.
        """
        end_time = datetime.now(timezone.utc)
        start_time = end_time - timedelta(minutes=self.DEFAULT_TIME_RANGE_MINUTES) + timedelta(
            seconds=self.DEFAULT_STEP)

        return start_time, end_time

    def _series_to_metric_points(
        self,
        series: List[Tuple[datetime, float]]
    ) -> List[MetricPoint]:
        """
        Converts a time series to a list of MetricPoint objects.

        Parameters:
        - series: List of (datetime, float) tuples.

        Returns:
        - List: List of MetricPoint objects.
        """
        return [
            MetricPoint(
                value=self._round_value(value),
                date=timestamp
            )
            for timestamp, value in series
        ]

    async def _query_instant(
        self,
        query: str
    ) -> Optional[float]:
        """
        Executes instant query and returns single value.

        Parameters:
        - query: PromQL query string.

        Returns:
        - float: Metric value.
        """
        response = await self.request(
            url=f"{self.base_url}/api/v1/query",
            params={"query": query}
        )

        if not response:
            return None

        result = response.get("data", {}).get("result")

        if not result:
            return None

        try:
            _, value = result[0]["value"]
            return float(value)
        except Exception:
            self.logger.exception(f"Unexpected Prometheus data format: {result}")
            return None

    async def _query_instant_multiple(
        self,
        query: str
    ) -> Dict[str, float]:
        """
        Executes instant query and returns multiple values grouped by name.

        Parameters:
        - query: PromQL query string.

        Returns:
        - Dict: Dictionary mapping name to metric value.
        """
        response = await self.request(
            url=f"{self.base_url}/api/v1/query",
            params={"query": query}
        )

        if not response:
            return {}

        results = response.get("data", {}).get("result", [])

        if not results:
            return {}

        values_dict = {}

        try:
            for result in results:
                name = result["metric"].get("name")
                value = float(result["value"][1])

                if name:
                    values_dict[name] = value
        except Exception:
            self.logger.exception(f"Unexpected Prometheus data format: {results}")
            return {}

        return values_dict

    async def _query_range(
        self,
        query: str,
        start_time: datetime,
        end_time: datetime,
        step: int
    ) -> List[Tuple[datetime, float]]:
        """
        Executes range query and returns time series.

        Parameters:
        - query: PromQL query string.
        - start_time: Start time.
        - end_time: End time.
        - step: Step in seconds.

        Returns:
        - List: List of tuples.
        """
        response = await self.request(
            url=f"{self.base_url}/api/v1/query_range",
            params={
                "query": query,
                "start": start_time.timestamp(),
                "end": end_time.timestamp(),
                "step": f"{step}s",
            }
        )

        if not response:
            return []

        result = response.get("data", {}).get("result")

        if not result:
            return []

        time_series = []

        for metric in result:
            for timestamp, value in metric["values"]:
                time_series.append((
                    datetime.fromtimestamp(float(timestamp), tz=timezone.utc),
                    float(value),
                ))

        return sorted(time_series, key=lambda x: x[0])

    async def host_last_cpu(self) -> Optional[MetricPoint]:
        """
        Gets last host CPU metric value.

        Parameters:
        - None.

        Returns:
        - MetricPoint: MetricPoint object.
        """
        cpu_query = self._build_host_cpu_query(
            interval=self.DEFAULT_INTERVAL
        )

        cpu_value = await self._query_instant(
            query=cpu_query
        )

        if cpu_value is None:
            return None

        return MetricPoint(
            value=self._round_value(cpu_value),
            date=datetime.now(timezone.utc)
        )

    async def host_last_ram(self) -> Optional[MetricPoint]:
        """
        Gets last host RAM metric value.

        Parameters:
        - None.

        Returns:
        - MetricPoint: MetricPoint object.
        """
        memory_query = self._build_host_memory_query(
            interval=self.DEFAULT_INTERVAL
        )

        memory_value = await self._query_instant(
            query=memory_query
        )

        if memory_value is None:
            return None

        return MetricPoint(
            value=self._round_value(memory_value),
            date=datetime.now(timezone.utc)
        )

    async def host_all_cpu(self) -> List[MetricPoint]:
        """
        Gets list of host CPU metrics.

        Parameters:
        - None.

        Returns:
        - List: List of MetricPoint objects.
        """
        start_time, end_time = self._get_time_range()

        cpu_query = self._build_host_cpu_query(
            interval=self.DEFAULT_INTERVAL
        )

        cpu_series = await self._query_range(
            query=cpu_query,
            start_time=start_time,
            end_time=end_time,
            step=self.DEFAULT_STEP
        )

        if not cpu_series:
            return []

        return self._series_to_metric_points(
            series=cpu_series
        )

    async def host_all_ram(self) -> List[MetricPoint]:
        """
        Gets list of host RAM metrics.

        Parameters:
        - None.

        Returns:
        - List: List of MetricPoint objects.
        """
        start_time, end_time = self._get_time_range()

        memory_query = self._build_host_memory_query(
            interval=self.DEFAULT_INTERVAL
        )

        memory_series = await self._query_range(
            query=memory_query,
            start_time=start_time,
            end_time=end_time,
            step=self.DEFAULT_STEP
        )

        if not memory_series:
            return []

        return self._series_to_metric_points(
            series=memory_series
        )

    async def container_last_cpu(
        self,
        container: str
    ) -> Optional[MetricPoint]:
        """
        Gets last container CPU metric value.

        Parameters:
        - container: Container name.

        Returns:
        - MetricPoint: MetricPoint object.
        """
        cpu_query = self._build_container_cpu_query(
            interval=self.DEFAULT_INTERVAL,
            container=container
        )

        cpu_value = await self._query_instant(
            query=cpu_query
        )

        if cpu_value is None:
            return None

        return MetricPoint(
            value=self._round_value(cpu_value),
            date=datetime.now(timezone.utc)
        )

    async def container_last_ram(
        self,
        container: str
    ) -> Optional[MetricPoint]:
        """
        Gets last container RAM metric value.

        Parameters:
        - container: Container name.

        Returns:
        - MetricPoint: MetricPoint object.
        """
        memory_query = self._build_container_memory_query(
            container=container
        )

        memory_value = await self._query_instant(
            query=memory_query
        )

        if memory_value is None:
            return None

        return MetricPoint(
            value=self._round_value(memory_value),
            date=datetime.now(timezone.utc)
        )

    async def container_all_cpu(
        self,
        container: str
    ) -> List[MetricPoint]:
        """
        Gets list of container CPU metrics.

        Parameters:
        - container: Container name.

        Returns:
        - List: List of MetricPoint objects.
        """
        start_time, end_time = self._get_time_range()

        cpu_query = self._build_container_cpu_query(
            interval=self.DEFAULT_INTERVAL,
            container=container
        )

        cpu_series = await self._query_range(
            query=cpu_query,
            start_time=start_time,
            end_time=end_time,
            step=self.DEFAULT_STEP
        )

        if not cpu_series:
            return []

        return self._series_to_metric_points(
            series=cpu_series
        )

    async def container_all_ram(
        self,
        container: str
    ) -> List[MetricPoint]:
        """
        Gets list of container RAM metrics.

        Parameters:
        - container: Container name.

        Returns:
        - List: List of MetricPoint objects.
        """
        start_time, end_time = self._get_time_range()

        memory_query = self._build_container_memory_query(
            container=container
        )

        memory_series = await self._query_range(
            query=memory_query,
            start_time=start_time,
            end_time=end_time,
            step=self.DEFAULT_STEP
        )

        if not memory_series:
            return []

        return self._series_to_metric_points(
            series=memory_series
        )

    async def containers_last_cpu(
        self,
        containers: List[str]
    ) -> Dict[str, MetricPoint]:
        """
        Gets last CPU metrics for multiple containers.

        Parameters:
        - containers: List of container names.

        Returns:
        - Dict: Dictionary mapping container name to MetricPoint.
        """
        if not containers:
            return {}

        cpu_values = await self._query_instant_multiple(
            query=self._build_containers_cpu_query(
                interval=self.DEFAULT_INTERVAL,
                containers=containers
            )
        )

        now = datetime.now(timezone.utc)

        return {
            container: MetricPoint(
                value=self._round_value(cpu_values.get(container)),
                date=now
            )
            for container in containers
        }

    async def containers_last_ram(
        self,
        containers: List[str]
    ) -> Dict[str, MetricPoint]:
        """
        Gets last RAM metrics for multiple containers.

        Parameters:
        - containers: List of container names.

        Returns:
        - Dict: Dictionary mapping container name to MetricPoint.
        """
        if not containers:
            return {}

        memory_values = await self._query_instant_multiple(
            query=self._build_containers_memory_query(containers=containers)
        )

        now = datetime.now(timezone.utc)

        return {
            container: MetricPoint(
                value=self._round_value(memory_values.get(container)),
                date=now
            )
            for container in containers
        }
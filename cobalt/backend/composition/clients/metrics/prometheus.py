#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from application.contracts.loggers import AbstractLogger
from application.contracts.clients import (
    AbstractMetricsClient,
    AbstractHttpClient
)
from infrastructure.clients import PrometheusClient
from infrastructure.configs import ApplicationConfig


def create_prometheus_client(
    config: ApplicationConfig,
    http_client: AbstractHttpClient,
    logger: AbstractLogger
) -> AbstractMetricsClient:
    """
    Creates a Prometheus client.

    Parameters:
    - config: ApplicationConfig object.
    - http_client: AbstractHttpClient object.
    - logger: AbstractLogger object.

    Returns:
    - AbstractMetricsClient: AbstractMetricsClient object.
    """
    return PrometheusClient(
        base_url=config.prometheus.url,
        http_client=http_client,
        logger=logger
    )

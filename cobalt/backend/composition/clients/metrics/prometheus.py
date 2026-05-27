#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from application.contracts.loggers import AbstractLogger
from application.contracts.clients import AbstractMetricsClient
from infrastructure.clients.metrics.prometheus import PrometheusClient
from infrastructure.configs import ApplicationConfig


def create_prometheus_client(
    config: ApplicationConfig,
    logger: AbstractLogger
) -> AbstractMetricsClient:
    """
    Creates a Prometheus client.

    Parameters:
    - config: ApplicationConfig object.
    - logger: AbstractLogger object.

    Returns:
    - AbstractMetricsClient: AbstractMetricsClient object.
    """
    return PrometheusClient(
        base_url=config.prometheus.url,
        logger=logger
    )

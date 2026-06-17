#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

class RoomsConstants:
    """
    Rooms-related constants.
    """
    HOST_CPU_METRICS_KEY: str = "metrics:host:cpu"
    HOST_RAM_METRICS_KEY: str = "metrics:host:ram"
    SERVER_CPU_METRICS_KEY: str = "metrics:server:cpu:{server_id}"
    SERVER_RAM_METRICS_KEY: str = "metrics:server:ram:{server_id}"

    HOST_LOGS_KEY: str = "logs:host"
    SERVER_LOGS_KEY: str = "logs:server:{server_id}"

    SERVERS_STATUSES_KEY: str = "servers:statuses"
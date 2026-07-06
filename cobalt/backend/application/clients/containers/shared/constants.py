#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

class ContainersConstants:
    """
    Containers-related constants.
    """
    GAME_CONTAINER_NAME_KEY: str = "cobalt_server_{server_id}"

    MANAGED_BY: str = "cobalt"

    SERVER_ROOT: str = "/opt/cobalt_server"
    SERVER_FIFO: str = "/tmp/cobalt_server_fifo"

    NETWORK_MODE: str = "cobalt_network"
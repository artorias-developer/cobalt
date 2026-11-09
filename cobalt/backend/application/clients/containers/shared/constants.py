#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

class ContainersConstants:
    """
    Containers-related constants.
    """
    SERVER_RUNTIME_KEY: str = "cobalt_server_{server_id}"
    SERVER_INSTALLER_KEY: str = "{container_name}_installer"
    SERVER_UPGRADER_KEY: str = "{container_name}_upgrader"

    MANAGED_BY: str = "cobalt"

    SERVER_ROOT: str = "/opt/cobalt_server"
    SERVER_FIFO: str = "/tmp/cobalt_server_fifo"
    SERVER_INSTALLATION_DIR: str = "/installer_src"

    NETWORK_MODE: str = "{environment}_cobalt_servers_network"
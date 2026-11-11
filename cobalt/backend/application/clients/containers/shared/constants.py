#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from typing import Tuple


class ContainerConstants:
    """
    Container-related constants.
    """
    SERVER_RUNTIME_KEY: str = "cobalt_server_{server_id}"
    SERVER_INSTALLER_KEY: str = "cobalt_server_{server_id}_installer"
    SERVER_UPGRADER_KEY: str = "cobalt_server_{server_id}_upgrader"

    MANAGED_BY: str = "cobalt"
    PORTS_LABEL: str = "cobalt_ports"

    HOST_PROC_NET_DIR: str = "/host/proc/1/net"
    LOCAL_PROC_NET_DIR: str = "/proc/net"
    PROC_NET_SOCKET_FILES: Tuple[str, ...] = ("tcp", "tcp6", "udp", "udp6")

    SERVER_ROOT: str = "/opt/cobalt_server"
    SERVER_FIFO: str = "/tmp/cobalt_server_fifo"
    SERVER_INSTALLATION_DIR: str = "/installer_src"

    NETWORK_MODE: str = "{environment}_cobalt_servers_network"
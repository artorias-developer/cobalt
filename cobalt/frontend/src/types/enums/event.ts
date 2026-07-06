/*
 * Copyright (C) 2026 Artorias
 * Author: Artorias
 * Repository: https://github.com/artorias-developer/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

export enum LogsEventEnum {
  SUBSCRIBE_HOST = "logs_subscribe_host",
  SUBSCRIBE_SERVER = "logs_subscribe_server",
  UNSUBSCRIBE_HOST = "logs_unsubscribe_host",
  UNSUBSCRIBE_SERVER = "logs_unsubscribe_server",
  HOST_LOG = "host_log",
  SERVER_LOG = "server_log"
}

export enum MetricsEventEnum {
  SUBSCRIBE_HOST_CPU = "metrics_subscribe_host_cpu",
  UNSUBSCRIBE_HOST_CPU = "metrics_unsubscribe_host_cpu",
  SUBSCRIBE_HOST_RAM = "metrics_subscribe_host_ram",
  UNSUBSCRIBE_HOST_RAM = "metrics_unsubscribe_host_ram",
  SUBSCRIBE_SERVER_CPU = "metrics_subscribe_server_cpu",
  UNSUBSCRIBE_SERVER_CPU = "metrics_unsubscribe_server_cpu",
  SUBSCRIBE_SERVER_RAM = "metrics_subscribe_server_ram",
  UNSUBSCRIBE_SERVER_RAM = "metrics_unsubscribe_server_ram",
  HOST_CPU_METRIC = "host_cpu_metric",
  SERVER_CPU_METRIC = "server_cpu_metric",
  HOST_RAM_METRIC = "host_ram_metric",
  SERVER_RAM_METRIC = "server_ram_metric"
}

export enum ServersEventEnum {
  SUBSCRIBE_STATES = "servers_subscribe_states",
  UNSUBSCRIBE_STATES = "servers_unsubscribe_states",
  SERVER_STATE = "server_state"
}

export enum RolesEventEnum {
  ROLE_UPDATE = "role_update"
}
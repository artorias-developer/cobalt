/*
 * Copyright (C) 2026 Artorias
 * Author: Artorias
 * Repository: https://github.com/artorias-developer/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import type { InjectionKey } from "vue"
import type {
  IWsClient,
  IDocumentHelper,
  ILocaleHelper,
  IHttpAuthApiService,
  IHttpMetricsApiService,
  IHttpLogsApiService,
  IHttpServersApiService,
  IHttpGamesApiService,
  IHttpRolesApiService,
  IHttpUsersApiService,
  IHttpSettingsApiService,
  IHttpFilesApiService,
  IWsMetricsApiService,
  IWsLogsApiService,
  IWsServersApiService
} from "@/contracts"

export const WS_CLIENT_KEY: InjectionKey<IWsClient> = Symbol("wsClient")
export const DOCUMENT_HELPER_KEY: InjectionKey<IDocumentHelper> = Symbol("documentHelper")
export const LOCALE_HELPER_KEY: InjectionKey<ILocaleHelper> = Symbol("localeHelper")
export const HTTP_AUTH_API_SERVICE_KEY: InjectionKey<IHttpAuthApiService> = Symbol("httpAuthApiService")
export const HTTP_METRICS_API_SERVICE_KEY: InjectionKey<IHttpMetricsApiService> = Symbol("httpMetricsApiService")
export const HTTP_LOGS_API_SERVICE_KEY: InjectionKey<IHttpLogsApiService> = Symbol("httpLogsApiService")
export const HTTP_SERVERS_API_SERVICE_KEY: InjectionKey<IHttpServersApiService> = Symbol("httpServersApiService")
export const HTTP_GAMES_API_SERVICE_KEY: InjectionKey<IHttpGamesApiService> = Symbol("httpGamesApiService")
export const HTTP_ROLES_API_SERVICE_KEY: InjectionKey<IHttpRolesApiService> = Symbol("httpRolesApiService")
export const HTTP_USERS_API_SERVICE_KEY: InjectionKey<IHttpUsersApiService> = Symbol("httpUsersApiService")
export const HTTP_SETTINGS_API_SERVICE_KEY: InjectionKey<IHttpSettingsApiService> = Symbol("httpSettingsApiService")
export const HTTP_FILES_API_SERVICE_KEY: InjectionKey<IHttpFilesApiService> = Symbol("httpFilesApiService")
export const WS_METRICS_API_SERVICE_KEY: InjectionKey<IWsMetricsApiService> = Symbol("wsMetricsApiService")
export const WS_LOGS_API_SERVICE_KEY: InjectionKey<IWsLogsApiService> = Symbol("wsLogsApiService")
export const WS_SERVERS_API_SERVICE_KEY: InjectionKey<IWsServersApiService> = Symbol("wsServersApiService")
export const FORM_KEY = Symbol("form")
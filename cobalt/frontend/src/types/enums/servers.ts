/*
 * Copyright (C) 2026 Artorias
 * Author: Artorias
 * Repository: https://github.com/artorias-developer/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

export enum ServerStateEnum {
  PENDING = "pending",
  INSTALLATION = "installation",
  INSTALL_FAILED = "install_failed",
  INSTALL_CANCELED = "install_canceled",
  INSTALLED = "installed",
  UPGRADING = "upgrading",
  UPGRADE_FAILED = "upgrade_failed",
  UPGRADE_CANCELED = "upgrade_canceled"
}
/*
 * Copyright (C) 2026 ArtoriasCode
 * Author: ArtoriasCode
 * Repository: https://github.com/ArtoriasCode/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import process from "node:process";

import { InstallerApplication } from "./src/InstallerApplication.mjs";

const installDirectory = process.env.COBALT_INSTALL_DIR;

if (!installDirectory) {
  console.error("Error: COBALT_INSTALL_DIR is not set (run install.sh instead)");
  process.exit(1);
}

await new InstallerApplication(installDirectory).run();
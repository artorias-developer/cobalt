/*
 * Copyright (C) 2026 ArtoriasCode
 * Author: ArtoriasCode
 * Repository: https://github.com/ArtoriasCode/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import { spawnSync } from "node:child_process";
import fs from "node:fs";

/**
 * Detects and installs Docker and the Docker Compose plugin.
 */
export class DockerInstaller {
  static PHASE_ID = "docker";

  /**
   * Creates an installer.
   *
   * Parameters:
   * - runner (CommandRunner): Command runner.
   * - tracker (ProgressTracker): Progress tracker.
   * - status (object): Result of DockerInstaller.detect().
   *
   * Returns:
   * - DockerInstaller: A new installer instance.
   */
  constructor(runner, tracker, status) {
    this.runner = runner;
    this.tracker = tracker;
    this.status = status;
  }

  /**
   * Checks whether Docker and Docker Compose are installed.
   *
   * Parameters:
   * - null.
   *
   * Returns:
   * - object: An object with hasDocker (boolean) and hasCompose (boolean).
   */
  static detect() {
    const hasDocker = !spawnSync("docker", ["--version"], { stdio: "ignore" }).error;
    const hasCompose =
      hasDocker && spawnSync("docker", ["compose", "version"], { stdio: "ignore" }).status === 0;
    return { hasDocker, hasCompose };
  }

  /**
   * Installs whatever is missing, reporting progress per executed command.
   *
   * Parameters:
   * - null.
   *
   * Returns:
   * - Promise<void>: Resolves when Docker and Compose are available.
   */
  async install() {
    if (this.status.hasCompose) {
      this.tracker.setTotal(DockerInstaller.PHASE_ID, 1);
      this.tracker.finish(DockerInstaller.PHASE_ID);
      return;
    }

    const commandPlan = this.status.hasDocker ? this.#buildComposePluginPlan() : this.#buildFullInstallPlan();
    this.tracker.setTotal(DockerInstaller.PHASE_ID, commandPlan.length);

    for (const step of commandPlan) {
      this.tracker.detail = [step.command, ...step.commandArguments].join(" ").slice(0, 60);
      await this.runner.run(step.command, step.commandArguments, {
        elevated: true,
        standardInput: step.standardInput,
      });
      this.tracker.advance(DockerInstaller.PHASE_ID);
    }
  }

  /**
   * Plan for installing only the Compose plugin.
   *
   * Parameters:
   * - null.
   *
   * Returns:
   * - object[]: Steps with command, commandArguments and optional standardInput.
   */
  #buildComposePluginPlan() {
    return [
      { command: "apt-get", commandArguments: ["update"] },
      { command: "apt-get", commandArguments: ["install", "-y", "docker-compose-plugin"] },
    ];
  }

  /**
   * Plan for installing Docker Engine and all plugins from the official repository.
   *
   * Parameters:
   * - null.
   *
   * Returns:
   * - object[]: Steps with command, commandArguments and optional standardInput.
   */
  #buildFullInstallPlan() {
    return [
      { command: "apt-get", commandArguments: ["update"] },
      { command: "apt-get", commandArguments: ["install", "-y", "ca-certificates", "curl"] },
      { command: "install", commandArguments: ["-m", "0755", "-d", "/etc/apt/keyrings"] },
      {
        command: "curl",
        commandArguments: [
          "-fsSL",
          "https://download.docker.com/linux/ubuntu/gpg",
          "-o",
          "/etc/apt/keyrings/docker.asc",
        ],
      },
      { command: "chmod", commandArguments: ["a+r", "/etc/apt/keyrings/docker.asc"] },
      {
        command: "tee",
        commandArguments: ["/etc/apt/sources.list.d/docker.sources"],
        standardInput: this.#buildSourcesFile(),
      },
      { command: "apt-get", commandArguments: ["update"] },
      {
        command: "apt-get",
        commandArguments: [
          "install",
          "-y",
          "docker-ce",
          "docker-ce-cli",
          "containerd.io",
          "docker-buildx-plugin",
          "docker-compose-plugin",
        ],
      },
    ];
  }

  /**
   * Builds the contents of the Docker apt sources file.
   *
   * Parameters:
   * - null.
   *
   * Returns:
   * - string: The sources file text.
   */
  #buildSourcesFile() {
    const architecture = spawnSync("dpkg", ["--print-architecture"], { encoding: "utf8" }).stdout.trim();
    return [
      "Types: deb",
      "URIs: https://download.docker.com/linux/ubuntu",
      `Suites: ${this.#readOperatingSystemCodename()}`,
      "Components: stable",
      `Architectures: ${architecture}`,
      "Signed-By: /etc/apt/keyrings/docker.asc",
      "",
    ].join("\n");
  }

  /**
   * Reads the Ubuntu release codename from /etc/os-release.
   *
   * Parameters:
   * - null.
   *
   * Returns:
   * - string: The codename (for example "jammy").
   */
  #readOperatingSystemCodename() {
    const releaseText = fs.readFileSync("/etc/os-release", "utf8");
    const readValue = (key) => releaseText.match(new RegExp(`^${key}=("?)(.*)\\1$`, "m"))?.[2];
    return readValue("UBUNTU_CODENAME") || readValue("VERSION_CODENAME");
  }
}
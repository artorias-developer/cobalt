/*
 * Copyright (C) 2026 ArtoriasCode
 * Author: ArtoriasCode
 * Repository: https://github.com/ArtoriasCode/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import fs from "node:fs";
import path from "node:path";

import { BuildStepCounter } from "../progress/BuildStepCounter.mjs";

/**
 * Pulls, builds and starts the Docker Compose services with real progress.
 */
export class ComposeDeployer {
  static PULL_PHASE_ID = "pull";
  static BUILD_PHASE_ID = "build";
  static START_PHASE_ID = "up";
  static PULLED_PATTERN = /\bPulled\b/;
  static STARTED_PATTERN = /Container\s+(\S+)\s+(?:Started|Running|Healthy)\b/;

  /**
   * Creates a deployer.
   *
   * Parameters:
   * - runner (CommandRunner): Command runner.
   * - tracker (ProgressTracker): Progress tracker.
   * - environmentName (string): "dev" or "prod".
   * - port (string): HTTPS port passed to Compose as HTTPS_PORT.
   * - composeRoot (string): Directory that contains the <environment>/docker-compose.yaml files.
   *
   * Returns:
   * - ComposeDeployer: A new deployer instance.
   */
  constructor(runner, tracker, environmentName, port, composeRoot) {
    this.runner = runner;
    this.tracker = tracker;
    this.port = port;
    this.composeFile = path.join(composeRoot, environmentName, "docker-compose.yaml");
    this.baseArguments = ["compose", "--progress", "plain", "--all-resources", "-f", this.composeFile];
  }

  /**
   * Runs the whole deployment: pull, build, start.
   *
   * Parameters:
   * - null.
   *
   * Returns:
   * - Promise<void>: Resolves when all containers are started.
   */
  async deploy() {
    if (!fs.existsSync(this.composeFile)) throw new Error(`File not found: ${this.composeFile}`);

    const services = await this.#readServices();

    if (!services) {
      await this.#deployCombined();
      return;
    }

    await this.#pullImages(services.filter((service) => service.hasImage && !service.hasBuild));
    await this.#buildImages(services.filter((service) => service.hasBuild));
    await this.#startContainers(services);
  }

  /**
   * Runs a docker compose subcommand with the shared arguments and environment.
   *
   * Parameters:
   * - subcommandArguments (string[]): Subcommand and its arguments.
   * - options (object): Options forwarded to CommandRunner.run().
   *
   * Returns:
   * - Promise<string>: Captured output when requested.
   */
  #runCompose(subcommandArguments, options = {}) {
    return this.runner.run("docker", [...this.baseArguments, ...subcommandArguments], {
      ...options,
      environment: { HTTPS_PORT: this.port, ...options.environment },
    });
  }

  /**
   * Reads the service list from the resolved Compose configuration.
   *
   * Parameters:
   * - null.
   *
   * Returns:
   * - Promise<object[]|null>: Services with name, hasBuild and hasImage, or null when unavailable.
   */
  async #readServices() {
    try {
      const configurationJson = await this.#runCompose(["config", "--format", "json"], {
        captureOutput: true,
      });
      const configuration = JSON.parse(configurationJson);
      const services = Object.entries(configuration.services ?? {}).map(([name, definition]) => ({
        name,
        hasBuild: Boolean(definition.build),
        hasImage: Boolean(definition.image),
      }));
      return services.length > 0 ? services : null;
    } catch {
      return null;
    }
  }

  /**
   * Fallback used when the service list cannot be read: one combined command.
   *
   * Parameters:
   * - null.
   *
   * Returns:
   * - Promise<void>: Resolves when the command exits.
   */
  async #deployCombined() {
    this.tracker.start(ComposeDeployer.START_PHASE_ID, "Building and starting containers");
    this.tracker.setTotal(ComposeDeployer.START_PHASE_ID, 1);
    await this.#runCompose(["up", "-d", "--build"]);
    this.tracker.finish(ComposeDeployer.PULL_PHASE_ID);
    this.tracker.finish(ComposeDeployer.BUILD_PHASE_ID);
    this.tracker.finish(ComposeDeployer.START_PHASE_ID);
  }

  /**
   * Pulls prebuilt images, advancing once per pulled image.
   *
   * Parameters:
   * - services (object[]): Services whose images must be pulled.
   *
   * Returns:
   * - Promise<void>: Resolves when all images are pulled.
   */
  async #pullImages(services) {
    this.tracker.start(ComposeDeployer.PULL_PHASE_ID);

    if (services.length === 0) {
      this.tracker.finish(ComposeDeployer.PULL_PHASE_ID);
      return;
    }

    this.tracker.setTotal(ComposeDeployer.PULL_PHASE_ID, services.length);

    await this.#runCompose(["pull", ...services.map((service) => service.name)], {
      onLine: (line) => {
        if (!ComposeDeployer.PULLED_PATTERN.test(line)) return;
        this.tracker.detail = line.replace(/^[^\w]+/, "").slice(0, 50);
        this.tracker.advance(ComposeDeployer.PULL_PHASE_ID);
      },
    });

    this.tracker.finish(ComposeDeployer.PULL_PHASE_ID);
  }

  /**
   * Builds images one service at a time.
   *
   * Parameters:
   * - services (object[]): Services that must be built.
   *
   * Returns:
   * - Promise<void>: Resolves when all images are built.
   */
  async #buildImages(services) {
    this.tracker.start(ComposeDeployer.BUILD_PHASE_ID);

    if (services.length === 0) {
      this.tracker.finish(ComposeDeployer.BUILD_PHASE_ID);
      return;
    }

    this.tracker.setTotal(ComposeDeployer.BUILD_PHASE_ID, services.length);

    for (let serviceIndex = 0; serviceIndex < services.length; serviceIndex++) {
      await this.#buildService(services[serviceIndex].name, serviceIndex);
    }

    this.tracker.finish(ComposeDeployer.BUILD_PHASE_ID);
  }

  /**
   * Builds a single service, advancing with each completed BuildKit step.
   *
   * Parameters:
   * - serviceName (string): Service to build.
   * - serviceIndex (number): Zero-based position of the service in the build list.
   *
   * Returns:
   * - Promise<void>: Resolves when the service image is built.
   */
  async #buildService(serviceName, serviceIndex) {
    const stepCounter = new BuildStepCounter();
    this.tracker.detail = serviceName;

    await this.#runCompose(["build", serviceName], {
      onLine: (line) => {
        if (!stepCounter.handleLine(line)) return;
        this.tracker.detail = `${serviceName} ${stepCounter.completedSteps}/${stepCounter.totalSteps}`;
        this.tracker.setDone(ComposeDeployer.BUILD_PHASE_ID, serviceIndex + stepCounter.fraction);
      },
    });

    this.tracker.setDone(ComposeDeployer.BUILD_PHASE_ID, serviceIndex + 1);
  }

  /**
   * Starts containers, advancing once per started container.
   *
   * Parameters:
   * - services (object[]): All services of the project.
   *
   * Returns:
   * - Promise<void>: Resolves when the containers are started.
   */
  async #startContainers(services) {
    this.tracker.start(ComposeDeployer.START_PHASE_ID);
    this.tracker.setTotal(ComposeDeployer.START_PHASE_ID, services.length);

    const startedContainers = new Set();

    await this.#runCompose(["up", "-d", "--no-build"], {
      onLine: (line) => {
        const match = line.match(ComposeDeployer.STARTED_PATTERN);
        if (!match || startedContainers.has(match[1])) return;
        startedContainers.add(match[1]);
        this.tracker.detail = match[1];
        this.tracker.setDone(ComposeDeployer.START_PHASE_ID, startedContainers.size);
      },
    });

    this.tracker.finish(ComposeDeployer.START_PHASE_ID);
  }
}
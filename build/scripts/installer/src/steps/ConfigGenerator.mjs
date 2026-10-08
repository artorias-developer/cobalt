/*
 * Copyright (C) 2026 ArtoriasCode
 * Author: ArtoriasCode
 * Repository: https://github.com/ArtoriasCode/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";

/**
 * Generates .env files and alembic.ini from their templates.
 */
export class ConfigGenerator {
  static PHASE_ID = "configs";

  /**
   * Creates a generator.
   *
   * Parameters:
   * - tracker (ProgressTracker): Progress tracker.
   * - environmentName (string): "dev" or "prod".
   * - host (string): IP address or domain.
   * - useBasePath (boolean): Whether to generate a random admin base path.
   * - repositoryRoot (string): Absolute path of the repository root.
   *
   * Returns:
   * - ConfigGenerator: A new generator instance.
   */
  constructor(tracker, environmentName, host, useBasePath, repositoryRoot) {
    this.tracker = tracker;
    this.environmentName = environmentName;
    this.host = host;
    this.useBasePath = useBasePath;
    this.repositoryRoot = repositoryRoot;
  }

  /**
   * Generates all configuration files.
   *
   * Parameters:
   * - null.
   *
   * Returns:
   * - Promise<object>: An object with appBasePath (string, empty when disabled).
   */
  async generate() {
    const sourceDirectory = path.join(this.repositoryRoot, "build", this.environmentName);
    const outputDirectory = path.join(this.repositoryRoot, "generated", this.environmentName, "build");
    const appBasePath = this.useBasePath ? this.#generateSecret(16) : "";
    const serviceReplacements = this.#buildServiceReplacements(appBasePath);

    this.tracker.setTotal(ConfigGenerator.PHASE_ID, Object.keys(serviceReplacements).length + 1);

    for (const [serviceName, replacements] of Object.entries(serviceReplacements)) {
      this.tracker.detail = `${serviceName}/.env`;
      this.#generateEnvironmentFile(serviceName, replacements, sourceDirectory, outputDirectory);
      this.tracker.advance(ConfigGenerator.PHASE_ID);
    }

    this.tracker.detail = "alembic.ini";
    this.#generateAlembicConfiguration();
    this.tracker.advance(ConfigGenerator.PHASE_ID);

    return { appBasePath };
  }

  /**
   * Generates a random hexadecimal secret.
   *
   * Parameters:
   * - byteCount (number): Number of random bytes.
   *
   * Returns:
   * - string: The hexadecimal secret.
   */
  #generateSecret(byteCount) {
    return crypto.randomBytes(byteCount).toString("hex");
  }

  /**
   * Builds the placeholder replacements for each service.
   *
   * Parameters:
   * - appBasePath (string): Admin base path (may be empty).
   *
   * Returns:
   * - object: Map of service name to a list of [placeholder, value] pairs.
   */
  #buildServiceReplacements(appBasePath) {
    const pepper = this.#generateSecret(32);
    const postgresPassword = this.#generateSecret(24);
    const redisPassword = this.#generateSecret(24);

    return {
      backend: [
        ["{{pepper}}", pepper],
        ["{{postgres_password}}", postgresPassword],
        ["{{redis_password}}", redisPassword],
        ["{{domain}}", this.host],
      ],
      postgres: [["{{postgres_password}}", postgresPassword]],
      redis: [["{{redis_password}}", redisPassword]],
      nginx: [
        ["{{domain}}", this.host],
        ["{{base_url}}", appBasePath],
      ],
      frontend: [
        ["{{domain}}", this.host],
        ["{{base_url}}", appBasePath],
      ],
    };
  }

  /**
   * Renders one service .env file from its template.
   *
   * Parameters:
   * - serviceName (string): Service name.
   * - replacements (string[][]): List of [placeholder, value] pairs.
   * - sourceDirectory (string): Directory with .env.example templates.
   * - outputDirectory (string): Directory for generated files.
   *
   * Returns:
   * - void: Nothing.
   */
  #generateEnvironmentFile(serviceName, replacements, sourceDirectory, outputDirectory) {
    const sourcePath = path.join(sourceDirectory, serviceName, ".env.example");
    const destinationPath = path.join(outputDirectory, serviceName, ".env");

    if (!fs.existsSync(sourcePath)) throw new Error(`File not found: ${sourcePath}`);

    fs.mkdirSync(path.dirname(destinationPath), { recursive: true });
    fs.writeFileSync(destinationPath, this.#substitute(fs.readFileSync(sourcePath, "utf8"), replacements));
    if (this.environmentName === "prod") fs.chmodSync(destinationPath, 0o600);
  }

  /**
   * Copies alembic.ini.example to alembic.ini.
   *
   * Parameters:
   * - null.
   *
   * Returns:
   * - void: Nothing.
   */
  #generateAlembicConfiguration() {
    const sourcePath = path.join(this.repositoryRoot, "cobalt", "backend", "alembic.ini.example");
    const destinationPath = path.join(this.repositoryRoot, "cobalt", "backend", "alembic.ini");

    if (!fs.existsSync(sourcePath)) throw new Error(`File not found: ${sourcePath}`);

    fs.copyFileSync(sourcePath, destinationPath);
  }

  /**
   * Replaces the first occurrence of each placeholder on every line.
   *
   * Parameters:
   * - text (string): Template text.
   * - replacements (string[][]): List of [placeholder, value] pairs.
   *
   * Returns:
   * - string: The rendered text.
   */
  #substitute(text, replacements) {
    return text
      .split("\n")
      .map((line) => {
        let renderedLine = line;
        for (const [placeholder, value] of replacements) {
          renderedLine = renderedLine.replace(placeholder, () => value);
        }
        return renderedLine;
      })
      .join("\n");
  }
}
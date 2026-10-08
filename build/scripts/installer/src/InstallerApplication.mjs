/*
 * Copyright (C) 2026 ArtoriasCode
 * Author: ArtoriasCode
 * Repository: https://github.com/ArtoriasCode/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import { spawn, spawnSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import process from "node:process";

import * as clackPrompts from "@clack/prompts";

import { CommandRunner } from "./process/CommandRunner.mjs";
import { ComposeDeployer } from "./steps/ComposeDeployer.mjs";
import { ConfigGenerator } from "./steps/ConfigGenerator.mjs";
import { DockerInstaller } from "./steps/DockerInstaller.mjs";
import { InstallerPrompts } from "./prompts/InstallerPrompts.mjs";
import { ProgressRenderer } from "./progress/ProgressRenderer.mjs";
import { ProgressTracker } from "./progress/ProgressTracker.mjs";
import { SslGenerator } from "./steps/SslGenerator.mjs";
import { TerminalStyle } from "./ui/TerminalStyle.mjs";

/**
 * Coordinates the whole installation: questions, steps, progress and reporting.
 */
export class InstallerApplication {
  static ELEVATION_REFRESH_INTERVAL_MILLISECONDS = 60_000;
  static FAILURE_TAIL_LENGTH = 15;

  /**
   * Creates the application.
   *
   * Parameters:
   * - installDirectory (string): Directory that contains install.sh.
   *
   * Returns:
   * - InstallerApplication: A new application instance.
   */
  constructor(installDirectory) {
    this.installDirectory = path.resolve(installDirectory);
    this.composeRoot = path.resolve(this.installDirectory, "..");
    this.repositoryRoot = path.resolve(this.installDirectory, "..", "..");
    this.logPath = path.join(this.repositoryRoot, "generated", "install.log");
    this.logStream = null;
    this.runner = null;
    this.tracker = null;
    this.renderer = null;
    this.elevationTimer = null;
  }

  /**
   * Runs the installer from the first question to the final report.
   *
   * Parameters:
   * - null.
   *
   * Returns:
   * - Promise<void>: Resolves on success; exits the process on failure.
   */
  async run() {
    const prompts = new InstallerPrompts();
    const answers = await prompts.ask();
    prompts.showSummary(answers);

    const dockerStatus = DockerInstaller.detect();
    this.#requestElevation(dockerStatus);
    this.#openLogStream(answers);

    this.runner = new CommandRunner(this.logStream);
    this.tracker = this.#createTracker(dockerStatus);
    this.renderer = new ProgressRenderer(this.tracker);

    process.on("SIGINT", () => this.#handleInterrupt());

    console.log(TerminalStyle.gutter);
    this.renderer.start();

    try {
      const result = await this.#executeSteps(answers, dockerStatus);
      this.#reportSuccess(answers, result.appBasePath);
    } catch (error) {
      this.#reportFailure(error);
    }
  }

  /**
   * Asks for administrator rights up front when Docker must be installed.
   *
   * Parameters:
   * - dockerStatus (object): Result of DockerInstaller.detect().
   *
   * Returns:
   * - void: Nothing.
   */
  #requestElevation(dockerStatus) {
    const isRoot = typeof process.getuid === "function" && process.getuid() === 0;
    if (dockerStatus.hasCompose || isRoot || typeof process.getuid !== "function") return;

    clackPrompts.log.info("Administrator access is required to install Docker.");
    const result = spawnSync("sudo", ["-v"], { stdio: "inherit" });

    if (result.error || result.status !== 0) {
      clackPrompts.cancel("Could not get administrator access.");
      process.exit(1);
    }

    this.elevationTimer = setInterval(() => {
      spawn("sudo", ["-n", "-v"], { stdio: "ignore" }).on("error", () => {});
    }, InstallerApplication.ELEVATION_REFRESH_INTERVAL_MILLISECONDS);
  }

  /**
   * Opens the install log file, falling back to the system temp directory.
   *
   * Parameters:
   * - answers (object): Result of InstallerPrompts.ask().
   *
   * Returns:
   * - void: Nothing.
   */
  #openLogStream(answers) {
    try {
      fs.mkdirSync(path.dirname(this.logPath), { recursive: true });
    } catch {
      this.logPath = path.join(os.tmpdir(), "cobalt-install.log");
    }

    this.logStream = fs.createWriteStream(this.logPath, { flags: "w" });
    this.logStream.write(
      `Cobalt install: env=${answers.environmentName} host=${answers.host} port=${answers.port} base_path=${answers.useBasePath}\n`,
    );
  }

  /**
   * Creates the progress tracker with weighted phases.
   *
   * Parameters:
   * - dockerStatus (object): Result of DockerInstaller.detect().
   *
   * Returns:
   * - ProgressTracker: A new tracker.
   */
  #createTracker(dockerStatus) {
    return new ProgressTracker([
      { id: DockerInstaller.PHASE_ID, label: "Installing Docker", weight: dockerStatus.hasCompose ? 1 : 15 },
      { id: ConfigGenerator.PHASE_ID, label: "Generating configs", weight: 3 },
      { id: SslGenerator.PHASE_ID, label: "Generating SSL certificate", weight: 2 },
      { id: ComposeDeployer.PULL_PHASE_ID, label: "Pulling images", weight: 15 },
      { id: ComposeDeployer.BUILD_PHASE_ID, label: "Building images", weight: 55 },
      { id: ComposeDeployer.START_PHASE_ID, label: "Starting containers", weight: 10 },
    ]);
  }

  /**
   * Executes every installation step in order.
   *
   * Parameters:
   * - answers (object): Result of InstallerPrompts.ask().
   * - dockerStatus (object): Result of DockerInstaller.detect().
   *
   * Returns:
   * - Promise<object>: An object with appBasePath (string).
   */
  async #executeSteps(answers, dockerStatus) {
    const { environmentName, host, port, useBasePath } = answers;

    this.tracker.start(DockerInstaller.PHASE_ID);
    await new DockerInstaller(this.runner, this.tracker, dockerStatus).install();
    this.tracker.finish(DockerInstaller.PHASE_ID);

    this.tracker.start(ConfigGenerator.PHASE_ID);
    const generationResult = await new ConfigGenerator(
      this.tracker,
      environmentName,
      host,
      useBasePath,
      this.repositoryRoot,
    ).generate();
    this.tracker.finish(ConfigGenerator.PHASE_ID);

    this.tracker.start(SslGenerator.PHASE_ID);
    await new SslGenerator(this.runner, this.tracker, environmentName, host, this.repositoryRoot).generate();
    this.tracker.finish(SslGenerator.PHASE_ID);

    await new ComposeDeployer(this.runner, this.tracker, environmentName, port, this.composeRoot).deploy();

    return generationResult;
  }

  /**
   * Stops the progress line, the elevation refresh and the log stream.
   *
   * Parameters:
   * - null.
   *
   * Returns:
   * - void: Nothing.
   */
  #shutdownInterface() {
    this.renderer.stop();
    if (this.elevationTimer) clearInterval(this.elevationTimer);
    this.logStream.end();
  }

  /**
   * Handles Ctrl+C: stops running commands and exits.
   *
   * Parameters:
   * - null.
   *
   * Returns:
   * - never: The process exits.
   */
  #handleInterrupt() {
    this.runner.terminateAll();
    this.#shutdownInterface();
    console.log(`${TerminalStyle.gutter}${TerminalStyle.red("■")}  Cancelled. Log: ${this.logPath}`);
    process.exit(130);
  }

  /**
   * Prints the failure report and exits with the failing command's exit code.
   *
   * Parameters:
   * - error (Error): The error that stopped the installation.
   *
   * Returns:
   * - never: The process exits.
   */
  #reportFailure(error) {
    const failedActivity = this.tracker.label;
    this.#shutdownInterface();

    console.log(this.renderer.formatLine(TerminalStyle.red("✖")));
    clackPrompts.log.error(`Installation failed: ${error.message}`);

    const outputTail = error.outputTail?.length ? error.outputTail : this.runner.outputTail;
    if (outputTail.length > 0) {
      const visibleLines = outputTail.slice(-InstallerApplication.FAILURE_TAIL_LENGTH);
      console.log(TerminalStyle.dim(visibleLines.map((line) => `${TerminalStyle.gutter}${line}`).join("\n")));
    }

    clackPrompts.outro(`Failed during: ${failedActivity}. Full log: ${this.logPath}`);
    process.exit(error.exitCode || 1);
  }

  /**
   * Prints the success report with the panel URL and credentials.
   *
   * Parameters:
   * - answers (object): Result of InstallerPrompts.ask().
   * - appBasePath (string): Generated admin base path (may be empty).
   *
   * Returns:
   * - void: Nothing.
   */
  #reportSuccess(answers, appBasePath) {
    this.#shutdownInterface();
    console.log(this.renderer.formatLine(TerminalStyle.green("✔")));

    const origin =
      answers.port === "443" ? `https://${answers.host}` : `https://${answers.host}:${answers.port}`;
    const loginUrl = appBasePath ? `${origin}/${appBasePath}/login` : `${origin}/login`;

    const summaryLines = [`URL:      ${loginUrl}`];
    if (appBasePath) summaryLines.push(`Base:     ${appBasePath}`);
    summaryLines.push("Login:    admin", "Password: admin");

    clackPrompts.note(summaryLines.join("\n"), "Cobalt is running");
    clackPrompts.outro("Installation complete");
  }
}
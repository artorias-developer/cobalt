/*
 * Copyright (C) 2026 ArtoriasCode
 * Author: ArtoriasCode
 * Repository: https://github.com/ArtoriasCode/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import process from "node:process";

import * as clackPrompts from "@clack/prompts";

/**
 * Asks the user the installation questions.
 */
export class InstallerPrompts {
  static IP_ADDRESS_PATTERN = /^\d{1,3}(\.\d{1,3}){3}$/;
  static DOMAIN_PATTERN = /^[A-Za-z0-9]([A-Za-z0-9.-]*[A-Za-z0-9])?$/;

  /**
   * Validates the IP address or domain answer.
   *
   * Parameters:
   * - value (string|undefined): Raw answer.
   *
   * Returns:
   * - string|undefined: An error message, or undefined when the value is valid.
   */
  static validateHost(value) {
    const host = (value ?? "").trim();
    if (!host) return "Value cannot be empty";

    if (InstallerPrompts.IP_ADDRESS_PATTERN.test(host)) {
      const isValidAddress = host.split(".").every((octet) => Number(octet) <= 255);
      return isValidAddress ? undefined : "Invalid IP address";
    }

    if (InstallerPrompts.DOMAIN_PATTERN.test(host)) return undefined;

    return "Enter a valid IP or domain (e.g. 203.0.113.10 or example.com)";
  }

  /**
   * Validates the port answer.
   *
   * Parameters:
   * - value (string|undefined): Raw answer.
   *
   * Returns:
   * - string|undefined: An error message, or undefined when the value is valid.
   */
  static validatePort(value) {
    const port = (value ?? "").trim();
    if (!/^\d+$/.test(port)) return "Port must be a number";

    const portNumber = Number(port);
    if (portNumber < 1 || portNumber > 65535) return "Port must be between 1 and 65535";

    return undefined;
  }

  /**
   * Prints the cancellation message and exits.
   *
   * Parameters:
   * - null.
   *
   * Returns:
   * - never: The process exits.
   */
  static cancel() {
    clackPrompts.cancel("Installation cancelled.");
    process.exit(0);
  }

  /**
   * Asks every question in order.
   *
   * Parameters:
   * - null.
   *
   * Returns:
   * - Promise<object>: An object with environmentName, host, port (strings) and useBasePath (boolean).
   */
  async ask() {
    clackPrompts.intro("Cobalt installer");

    const environmentName = await this.#askEnvironment();
    const host = await this.#askHost(environmentName);
    const port = await this.#askPort();
    const useBasePath = await this.#askBasePath();

    return { environmentName, host: host.trim(), port: port.trim(), useBasePath };
  }

  /**
   * Prints a summary of the chosen configuration.
   *
   * Parameters:
   * - answers (object): Result of ask().
   *
   * Returns:
   * - void: Nothing.
   */
  showSummary(answers) {
    clackPrompts.note(
      [
        `Environment:     ${answers.environmentName}`,
        `Host:            ${answers.host}`,
        `HTTPS port:      ${answers.port}`,
        `Admin base path: ${answers.useBasePath ? "yes" : "no"}`,
      ].join("\n"),
      "Configuration",
    );
  }

  /**
   * Asks for the environment.
   *
   * Parameters:
   * - null.
   *
   * Returns:
   * - Promise<string>: "dev" or "prod".
   */
  async #askEnvironment() {
    const answer = await clackPrompts.select({
      message: "Environment",
      options: [
        { value: "dev", label: "dev", hint: "for local development" },
        { value: "prod", label: "prod", hint: "for VPS / VDS" },
      ],
      initialValue: "prod",
    });
    return this.#unwrap(answer);
  }

  /**
   * Asks for the IP address or domain.
   *
   * Parameters:
   * - environmentName (string): Selected environment, used for the default value.
   *
   * Returns:
   * - Promise<string>: The raw answer.
   */
  async #askHost(environmentName) {
    const isDevelopment = environmentName === "dev";
    const answer = await clackPrompts.text({
      message: "IP or domain",
      placeholder: isDevelopment ? "127.0.0.1" : "203.0.113.10 or example.com",
      initialValue: isDevelopment ? "127.0.0.1" : "",
      validate: InstallerPrompts.validateHost,
    });
    return this.#unwrap(answer);
  }

  /**
   * Asks for the HTTPS port.
   *
   * Parameters:
   * - null.
   *
   * Returns:
   * - Promise<string>: The raw answer.
   */
  async #askPort() {
    const answer = await clackPrompts.text({
      message: "HTTPS port",
      placeholder: "443",
      initialValue: "443",
      validate: InstallerPrompts.validatePort,
    });
    return this.#unwrap(answer);
  }

  /**
   * Asks whether to add a random admin base path.
   *
   * Parameters:
   * - null.
   *
   * Returns:
   * - Promise<boolean>: True when a base path should be added.
   */
  async #askBasePath() {
    const answer = await clackPrompts.select({
      message: "Add admin base path?",
      options: [
        { value: true, label: "Yes", hint: "random URL prefix for the admin panel" },
        { value: false, label: "No" },
      ],
      initialValue: true,
    });
    return this.#unwrap(answer);
  }

  /**
   * Returns the answer, or cancels the installation when the user aborted the prompt.
   *
   * Parameters:
   * - answer (any): Value returned by a prompt.
   *
   * Returns:
   * - any: The same answer when it was not cancelled.
   */
  #unwrap(answer) {
    if (clackPrompts.isCancel(answer)) InstallerPrompts.cancel();
    return answer;
  }
}
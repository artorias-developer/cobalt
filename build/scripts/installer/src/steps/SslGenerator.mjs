/*
 * Copyright (C) 2026 ArtoriasCode
 * Author: ArtoriasCode
 * Repository: https://github.com/ArtoriasCode/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import fs from "node:fs";
import path from "node:path";

/**
 * Generates a self-signed SSL certificate for the selected host.
 */
export class SslGenerator {
  static PHASE_ID = "ssl";

  /**
   * Creates a generator.
   *
   * Parameters:
   * - runner (CommandRunner): Command runner.
   * - tracker (ProgressTracker): Progress tracker.
   * - environmentName (string): "dev" or "prod".
   * - host (string): IP address or domain.
   * - repositoryRoot (string): Absolute path of the repository root.
   *
   * Returns:
   * - SslGenerator: A new generator instance.
   */
  constructor(runner, tracker, environmentName, host, repositoryRoot) {
    this.runner = runner;
    this.tracker = tracker;
    this.environmentName = environmentName;
    this.host = host;
    this.repositoryRoot = repositoryRoot;
  }

  /**
   * Creates the certificate and private key with openssl.
   *
   * Parameters:
   * - null.
   *
   * Returns:
   * - Promise<void>: Resolves when the files are written.
   */
  async generate() {
    this.tracker.setTotal(SslGenerator.PHASE_ID, 1);
    this.tracker.detail = this.host;

    const certificateDirectory = this.#prepareCertificateDirectory();

    await this.runner.run("openssl", [
      "req",
      "-x509",
      "-nodes",
      "-newkey",
      "rsa:4096",
      "-keyout",
      path.join(certificateDirectory, "privkey.pem"),
      "-out",
      path.join(certificateDirectory, "fullchain.pem"),
      "-days",
      "3650",
      "-subj",
      `/CN=${this.host}`,
      "-addext",
      `subjectAltName=${this.#buildSubjectAlternativeName()}`,
    ]);

    this.tracker.advance(SslGenerator.PHASE_ID);
  }

  /**
   * Creates the output directory for the certificate.
   *
   * Parameters:
   * - null.
   *
   * Returns:
   * - string: Absolute path of the directory.
   */
  #prepareCertificateDirectory() {
    const safeHostName = this.host.replaceAll(":", "_");
    const certificateDirectory = path.join(
      this.repositoryRoot,
      "generated",
      this.environmentName,
      "build",
      "nginx",
      "ssl",
      "self-signed",
      safeHostName,
    );
    fs.mkdirSync(certificateDirectory, { recursive: true });
    fs.chmodSync(certificateDirectory, 0o755);
    return certificateDirectory;
  }

  /**
   * Builds the subjectAltName value for an IP address or a domain.
   *
   * Parameters:
   * - null.
   *
   * Returns:
   * - string: For example "IP:1.2.3.4" or "DNS:example.com".
   */
  #buildSubjectAlternativeName() {
    const isIpAddress = /^\d{1,3}(\.\d{1,3}){3}$/.test(this.host);
    return isIpAddress ? `IP:${this.host}` : `DNS:${this.host}`;
  }
}
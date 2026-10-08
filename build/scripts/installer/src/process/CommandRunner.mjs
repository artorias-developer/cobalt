/*
 * Copyright (C) 2026 ArtoriasCode
 * Author: ArtoriasCode
 * Repository: https://github.com/ArtoriasCode/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import { spawn } from "node:child_process";
import process from "node:process";

import { CommandError } from "./CommandError.mjs";
import { OutputLineSplitter } from "./OutputLineSplitter.mjs";
import { TerminalStyle } from "../ui/TerminalStyle.mjs";

/**
 * Runs external commands, logs their output and reports lines to a handler.
 */
export class CommandRunner {
  static MAXIMUM_TAIL_LENGTH = 30;

  /**
   * Creates a runner that writes all output to a log stream.
   *
   * Parameters:
   * - logStream (WriteStream): Destination for the full command output.
   *
   * Returns:
   * - CommandRunner: A new runner instance.
   */
  constructor(logStream) {
    this.logStream = logStream;
    this.outputTail = [];
    this.activeProcesses = new Set();
    this.isRoot = typeof process.getuid === "function" && process.getuid() === 0;
  }

  /**
   * Runs a command and resolves when it exits successfully.
   *
   * Parameters:
   * - command (string): Executable to run.
   * - commandArguments (string[]): Arguments passed to the executable.
   * - options (object): elevated (boolean), standardInput (string), environment (object), captureOutput (boolean), onLine (function).
   *
   * Returns:
   * - Promise<string>: Captured standard output when captureOutput is set, otherwise an empty string.
   */
  run(command, commandArguments = [], options = {}) {
    const { elevated = false, standardInput, environment, captureOutput = false, onLine } = options;
    const invocation = this.#buildInvocation(command, commandArguments, elevated);

    this.logStream.write(`\n$ ${[invocation.file, ...invocation.argumentList].join(" ")}\n`);

    return new Promise((resolve, reject) => {
      const lineSplitter = new OutputLineSplitter();
      let capturedOutput = "";
      let isSettled = false;

      const childProcess = spawn(invocation.file, invocation.argumentList, {
        stdio: [standardInput !== undefined ? "pipe" : "ignore", "pipe", "pipe"],
        env: { ...process.env, DEBIAN_FRONTEND: "noninteractive", NO_COLOR: "1", ...environment },
      });
      this.activeProcesses.add(childProcess);

      const handleChunk = (chunk) => {
        this.logStream.write(chunk);
        lineSplitter.push(chunk).forEach((line) => this.#handleLine(line, onLine));
      };

      const settle = (callback) => {
        if (isSettled) return;
        isSettled = true;
        this.activeProcesses.delete(childProcess);
        this.#handleLine(lineSplitter.flush(), onLine);
        callback();
      };

      childProcess.stdout.on("data", (chunk) => {
        if (captureOutput) capturedOutput += chunk.toString();
        handleChunk(chunk);
      });
      childProcess.stderr.on("data", handleChunk);

      childProcess.on("error", (error) =>
        settle(() =>
          reject(new CommandError(`Failed to run ${command}: ${error.message}`, 1, [...this.outputTail])),
        ),
      );

      childProcess.on("close", (exitCode) =>
        settle(() => {
          if (exitCode === 0) {
            resolve(capturedOutput);
          } else {
            reject(new CommandError(`${command} exited with code ${exitCode}`, exitCode ?? 1, [...this.outputTail]));
          }
        }),
      );

      if (standardInput !== undefined) childProcess.stdin.end(standardInput);
    });
  }

  /**
   * Terminates every command that is still running.
   *
   * Parameters:
   * - null.
   *
   * Returns:
   * - void: Nothing.
   */
  terminateAll() {
    for (const childProcess of this.activeProcesses) childProcess.kill("SIGTERM");
  }

  /**
   * Builds the real executable and arguments, adding non-interactive sudo when needed.
   *
   * Parameters:
   * - command (string): Requested executable.
   * - commandArguments (string[]): Requested arguments.
   * - elevated (boolean): Whether the command needs administrator rights.
   *
   * Returns:
   * - object: An object with file (string) and argumentList (string[]).
   */
  #buildInvocation(command, commandArguments, elevated) {
    if (elevated && !this.isRoot) {
      return { file: "sudo", argumentList: ["-n", command, ...commandArguments] };
    }
    return { file: command, argumentList: commandArguments };
  }

  /**
   * Cleans a raw output line, stores it in the tail and forwards it to the handler.
   *
   * Parameters:
   * - rawLine (string): Raw output line.
   * - onLine (function|undefined): Optional handler receiving the cleaned line.
   *
   * Returns:
   * - void: Nothing.
   */
  #handleLine(rawLine, onLine) {
    const line = TerminalStyle.stripAnsi(rawLine).trim();
    if (!line) return;

    this.outputTail.push(line);
    if (this.outputTail.length > CommandRunner.MAXIMUM_TAIL_LENGTH) this.outputTail.shift();

    if (onLine) onLine(line);
  }
}
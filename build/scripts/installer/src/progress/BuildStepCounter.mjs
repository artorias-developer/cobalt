/*
 * Copyright (C) 2026 ArtoriasCode
 * Author: ArtoriasCode
 * Repository: https://github.com/ArtoriasCode/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

/**
 * Counts completed Docker BuildKit steps from plain progress output.
 */
export class BuildStepCounter {
  static STEP_START_PATTERN = /^#(\d+)\s+\[([^\]]*?)\s*(\d+)\/(\d+)\]/;
  static STEP_END_PATTERN = /^#(\d+)\s+(?:DONE|CACHED)\b/;
  static MAXIMUM_FRACTION = 0.99;

  /**
   * Creates an empty counter.
   *
   * Parameters:
   * - null.
   *
   * Returns:
   * - BuildStepCounter: A new counter instance.
   */
  constructor() {
    this.stageNameByStepId = new Map();
    this.stages = new Map();
  }

  /**
   * Processes one output line.
   *
   * Parameters:
   * - line (string): A cleaned line of build output.
   *
   * Returns:
   * - boolean: True when the number of completed steps changed.
   */
  handleLine(line) {
    const startMatch = line.match(BuildStepCounter.STEP_START_PATTERN);
    if (startMatch) {
      const [, stepId, stageName, , stageTotal] = startMatch;
      this.stageNameByStepId.set(stepId, stageName);
      const stage = this.stages.get(stageName) ?? { total: 0, completedStepIds: new Set() };
      stage.total = Math.max(stage.total, Number(stageTotal));
      this.stages.set(stageName, stage);
      return false;
    }

    const endMatch = line.match(BuildStepCounter.STEP_END_PATTERN);
    if (endMatch && this.stageNameByStepId.has(endMatch[1])) {
      const stage = this.stages.get(this.stageNameByStepId.get(endMatch[1]));
      const sizeBefore = stage.completedStepIds.size;
      stage.completedStepIds.add(endMatch[1]);
      return stage.completedStepIds.size !== sizeBefore;
    }

    return false;
  }

  /**
   * Total number of known steps.
   *
   * Parameters:
   * - null.
   *
   * Returns:
   * - number: The step count.
   */
  get totalSteps() {
    let total = 0;
    for (const stage of this.stages.values()) total += stage.total;
    return total;
  }

  /**
   * Number of completed steps.
   *
   * Parameters:
   * - null.
   *
   * Returns:
   * - number: The completed step count.
   */
  get completedSteps() {
    let completed = 0;
    for (const stage of this.stages.values()) {
      completed += Math.min(stage.completedStepIds.size, stage.total);
    }
    return completed;
  }

  /**
   * Completion fraction, capped so a build is never reported finished before it exits.
   *
   * Parameters:
   * - null.
   *
   * Returns:
   * - number: A value between 0 and 0.99.
   */
  get fraction() {
    const total = this.totalSteps;
    return total ? Math.min(this.completedSteps / total, BuildStepCounter.MAXIMUM_FRACTION) : 0;
  }
}
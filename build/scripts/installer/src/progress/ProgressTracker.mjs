/*
 * Copyright (C) 2026 ArtoriasCode
 * Author: ArtoriasCode
 * Repository: https://github.com/ArtoriasCode/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

/**
 * Tracks weighted installation phases. The percentage only changes when
 * a real unit of work is reported as completed.
 */
export class ProgressTracker {
  /**
   * Creates a tracker from phase definitions.
   *
   * Parameters:
   * - phaseDefinitions (object[]): Phases with id (string), label (string) and weight (number).
   *
   * Returns:
   * - ProgressTracker: A new tracker instance.
   */
  constructor(phaseDefinitions) {
    this.phases = phaseDefinitions.map((phaseDefinition) => ({
      ...phaseDefinition,
      total: 1,
      done: 0,
    }));
    this.currentPhaseId = null;
    this.detail = "";
  }

  /**
   * Finds a phase by identifier.
   *
   * Parameters:
   * - phaseId (string): Phase identifier.
   *
   * Returns:
   * - object: The matching phase.
   */
  getPhase(phaseId) {
    return this.phases.find((phase) => phase.id === phaseId);
  }

  /**
   * Marks a phase as the current one.
   *
   * Parameters:
   * - phaseId (string): Phase identifier.
   * - label (string|undefined): Optional replacement label.
   *
   * Returns:
   * - void: Nothing.
   */
  start(phaseId, label) {
    this.currentPhaseId = phaseId;
    this.detail = "";
    if (label) this.getPhase(phaseId).label = label;
  }

  /**
   * Sets how many units of work a phase contains.
   *
   * Parameters:
   * - phaseId (string): Phase identifier.
   * - total (number): Number of units.
   *
   * Returns:
   * - void: Nothing.
   */
  setTotal(phaseId, total) {
    const phase = this.getPhase(phaseId);
    phase.total = Math.max(1, total);
    phase.done = Math.min(phase.done, phase.total);
  }

  /**
   * Sets completed units for a phase. Progress never moves backwards.
   *
   * Parameters:
   * - phaseId (string): Phase identifier.
   * - done (number): Completed units.
   *
   * Returns:
   * - void: Nothing.
   */
  setDone(phaseId, done) {
    const phase = this.getPhase(phaseId);
    phase.done = Math.max(phase.done, Math.min(done, phase.total));
  }

  /**
   * Adds completed units to a phase.
   *
   * Parameters:
   * - phaseId (string): Phase identifier.
   * - amount (number): Units to add.
   *
   * Returns:
   * - void: Nothing.
   */
  advance(phaseId, amount = 1) {
    this.setDone(phaseId, this.getPhase(phaseId).done + amount);
  }

  /**
   * Marks a phase as fully completed.
   *
   * Parameters:
   * - phaseId (string): Phase identifier.
   *
   * Returns:
   * - void: Nothing.
   */
  finish(phaseId) {
    const phase = this.getPhase(phaseId);
    phase.done = phase.total;
  }

  /**
   * Overall completion percentage based on phase weights.
   *
   * Parameters:
   * - null.
   *
   * Returns:
   * - number: A value between 0 and 100.
   */
  get percent() {
    const totalWeight = this.phases.reduce((sum, phase) => sum + phase.weight, 0);
    const completedWeight = this.phases.reduce(
      (sum, phase) => sum + (phase.weight * phase.done) / phase.total,
      0,
    );
    return totalWeight ? (completedWeight / totalWeight) * 100 : 0;
  }

  /**
   * Human-readable description of the current activity.
   *
   * Parameters:
   * - null.
   *
   * Returns:
   * - string: The label with counters and detail.
   */
  get label() {
    const phase = this.currentPhaseId ? this.getPhase(this.currentPhaseId) : null;
    if (!phase) return "Preparing";

    let text = phase.label;
    if (phase.total > 1) {
      text += ` (${Math.min(phase.total, Math.floor(phase.done + 1e-9))}/${phase.total})`;
    }
    if (this.detail) text += ` · ${this.detail}`;
    return text;
  }
}
/*
 * Copyright (C) 2026 ArtoriasCode
 * Author: ArtoriasCode
 * Repository: https://github.com/ArtoriasCode/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

/**
 * Represents a single CPU or RAM metric data point.
 */
export interface MetricEntity {
  value: number
  date: string
}

/**
 * Represents host disk usage metrics.
 */
export interface DiskMetricsEntity {
  free: number
  total: number
  last_check: string
  next_check: string
}
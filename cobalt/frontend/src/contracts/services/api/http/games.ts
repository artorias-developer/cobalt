/*
 * Copyright (C) 2026 Artorias
 * Author: Artorias
 * Repository: https://github.com/artorias-developer/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import type { GameEntity, GamesPageEntity, GamesPageRequest } from "@/types"

/**
 * Interface for games API service operations.
 * Defines contract for managing games.
 * Implementation-agnostic - not tied to any specific HTTP client.
 */
export interface IHttpGamesApiService {
  /**
   * Gets a paginated list of games.
   *
   * Parameters:
   * - params: GamesPageRequest object.
   *
   * Returns:
   * - Promise<GamesPageEntity>: Paginated list of games.
   */
  getPage(params: GamesPageRequest): Promise<GamesPageEntity>

  /**
   * Gets an existing game by ID.
   *
   * Parameters:
   * - gameId: Game ID.
   *
   * Returns:
   * - Promise<GameEntity>: Game entity.
   */
  getOne(gameId: number): Promise<GameEntity>
}
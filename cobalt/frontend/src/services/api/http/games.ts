/*
 * Copyright (C) 2026 ArtoriasCode
 * Author: ArtoriasCode
 * Repository: https://github.com/ArtoriasCode/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import type { IHttpClient, IHttpGamesApiService } from "@/contracts"
import type { GameEntity, GamesPageEntity, GamesPageRequest } from "@/types"

/**
 * API service for games endpoints.
 */
export class HttpGamesApiService implements IHttpGamesApiService {
  private readonly prefix = "/api/v1/games"
  private readonly client: IHttpClient

  constructor(client: IHttpClient) {
    this.client = client
  }

  /**
   * Gets a paginated list of games.
   *
   * Parameters:
   * - params: GamesPageRequest object.
   *
   * Returns:
   * - Promise<GamesPageEntity>: Paginated list of games.
   */
  async getPage(params: GamesPageRequest): Promise<GamesPageEntity> {
    return this.client.get<GamesPageEntity>(`${this.prefix}/`, { params })
  }

  /**
   * Gets an existing game by ID.
   *
   * Parameters:
   * - gameId: Game ID.
   *
   * Returns:
   * - Promise<GameEntity>: Game entity.
   */
  async getOne(gameId: number): Promise<GameEntity> {
    return this.client.get<GameEntity>(`${this.prefix}/${gameId}`)
  }
}
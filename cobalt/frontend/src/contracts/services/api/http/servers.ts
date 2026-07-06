/*
 * Copyright (C) 2026 Artorias
 * Author: Artorias
 * Repository: https://github.com/artorias-developer/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import type {
  ServerEntity,
  ServersPageEntity,
  ServerStatusEntity,
  ServersPageRequest,
  ServerCreateRequest,
  ServerUpdateRequest,
  ServerExecuteRequest
} from "@/types"

/**
 * Interface for servers API service operations.
 * Defines contract for managing game servers.
 * Implementation-agnostic - not tied to any specific HTTP client.
 */
export interface IHttpServersApiService {
  /**
   * Gets a paginated list of servers.
   *
   * Parameters:
   * - params: ServersPageRequest object.
   *
   * Returns:
   * - Promise<ServersPageResponse>: Paginated list of servers.
   */
  getPage(params: ServersPageRequest): Promise<ServersPageEntity>

  /**
   * Gets an existing server.
   *
   * Parameters:
   * - serverId: Server ID.
   *
   * Returns:
   * - Promise<ServerEntity>: Server entity.
   */
  getOne(serverId: number): Promise<ServerEntity>

  /**
   * Creates a new server.
   *
   * Parameters:
   * - data: ServerCreateRequest object.
   *
   * Returns:
   * - Promise<ServerEntity>: Created server entity.
   */
  createOne(data: ServerCreateRequest): Promise<ServerEntity>

  /**
   * Updates an existing server.
   *
   * Parameters:
   * - serverId: Server ID.
   * - data: ServerUpdateRequest object.
   *
   * Returns:
   * - Promise<ServerEntity>: Updated server entity.
   */
  updateOne(serverId: number, data: ServerUpdateRequest): Promise<ServerEntity>

  /**
   * Deletes an existing server.
   *
   * Parameters:
   * - serverId: Server ID.
   *
   * Returns:
   * - Promise<void>.
   */
  deleteOne(serverId: number): Promise<void>

  /**
   * Deletes multiple existing servers.
   *
   * Parameters:
   * - ids: List of server IDs.
   *
   * Returns:
   * - Promise<void>.
   */
  deleteMany(ids: number[]): Promise<void>

  /**
   * Starts an existing server.
   *
   * Parameters:
   * - serverId: Server ID.
   *
   * Returns:
   * - Promise<void>.
   */
  start(serverId: number): Promise<void>

  /**
   * Stops an existing server.
   *
   * Parameters:
   * - serverId: Server ID.
   *
   * Returns:
   * - Promise<void>.
   */
  stop(serverId: number): Promise<void>

  /**
   * Restarts an existing server.
   *
   * Parameters:
   * - serverId: Server ID.
   *
   * Returns:
   * - Promise<void>.
   */
  restart(serverId: number): Promise<void>

  /**
   * Executes a command inside the server container.
   *
   * Parameters:
   * - serverId: Server ID.
   * - data: ServerExecuteRequest object.
   *
   * Returns:
   * - Promise<void>.
   */
  execute(serverId: number, data: ServerExecuteRequest): Promise<void>

  /**
   * Gets the server container status.
   *
   * Parameters:
   * - serverId: Server ID.
   *
   * Returns:
   * - Promise<ServerStatusEntity>: Server status entity.
   */
  status(serverId: number): Promise<ServerStatusEntity>
}
/*
 * Copyright (C) 2026 ArtoriasCode
 * Author: ArtoriasCode
 * Repository: https://github.com/ArtoriasCode/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import type { IHttpClient, IHttpServersApiService } from "@/contracts"
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
 * API service for servers endpoints.
 */
export class HttpServersApiService implements IHttpServersApiService {
  private readonly prefix = "/api/v1/servers"
  private readonly client: IHttpClient

  constructor(client: IHttpClient) {
    this.client = client
  }

  /**
   * Gets a paginated list of servers.
   *
   * Parameters:
   * - params: ServersPageRequest object.
   *
   * Returns:
   * - Promise<ServersPageResponse>: Paginated list of servers.
   */
  async getPage(params: ServersPageRequest): Promise<ServersPageEntity> {
    return this.client.get<ServersPageEntity>(`${this.prefix}/`, { params })
  }

  /**
   * Gets an existing server.
   *
   * Parameters:
   * - serverId: Server ID.
   *
   * Returns:
   * - Promise<ServerEntity>: Server entity.
   */
  async getOne(serverId: number): Promise<ServerEntity> {
    return this.client.get<ServerEntity>(`${this.prefix}/${serverId}`)
  }

  /**
   * Creates a new server.
   *
   * Parameters:
   * - data: ServerCreateRequest object.
   *
   * Returns:
   * - Promise<ServerEntity>: Created server entity.
   */
  async createOne(data: ServerCreateRequest): Promise<ServerEntity> {
    return this.client.post<ServerEntity>(`${this.prefix}/`, data)
  }

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
  async updateOne(serverId: number, data: ServerUpdateRequest): Promise<ServerEntity> {
    return this.client.patch<ServerEntity>(`${this.prefix}/${serverId}`, data)
  }

  /**
   * Deletes an existing server.
   *
   * Parameters:
   * - serverId: Server ID.
   *
   * Returns:
   * - Promise<void>.
   */
  async deleteOne(serverId: number): Promise<void> {
    return this.client.delete<void>(`${this.prefix}/${serverId}`)
  }

  /**
   * Deletes multiple existing servers.
   *
   * Parameters:
   * - ids: List of server IDs.
   *
   * Returns:
   * - Promise<void>.
   */
  async deleteMany(ids: number[]): Promise<void> {
    return this.client.delete<void>(`${this.prefix}/batch`, { data: ids })
  }

  /**
   * Starts an existing server.
   *
   * Parameters:
   * - serverId: Server ID.
   *
   * Returns:
   * - Promise<void>.
   */
  async start(serverId: number): Promise<void> {
    return this.client.post<void>(`${this.prefix}/${serverId}/start`)
  }

  /**
   * Stops an existing server.
   *
   * Parameters:
   * - serverId: Server ID.
   *
   * Returns:
   * - Promise<void>.
   */
  async stop(serverId: number): Promise<void> {
    return this.client.post<void>(`${this.prefix}/${serverId}/stop`)
  }

  /**
   * Restarts an existing server.
   *
   * Parameters:
   * - serverId: Server ID.
   *
   * Returns:
   * - Promise<void>.
   */
  async restart(serverId: number): Promise<void> {
    return this.client.post<void>(`${this.prefix}/${serverId}/restart`)
  }

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
  async execute(serverId: number, data: ServerExecuteRequest): Promise<void> {
    return this.client.post<void>(`${this.prefix}/${serverId}/execute`, data)
  }

  /**
   * Gets the server container status.
   *
   * Parameters:
   * - serverId: Server ID.
   *
   * Returns:
   * - Promise<ServerStatusEntity>: Server status entity.
   */
  async status(serverId: number): Promise<ServerStatusEntity> {
    return this.client.get<ServerStatusEntity>(`${this.prefix}/${serverId}/status`)
  }
}
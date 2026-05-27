/*
 * Copyright (C) 2026 ArtoriasCode
 * Author: ArtoriasCode
 * Repository: https://github.com/ArtoriasCode/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

/**
 * Interface for HTTP client operations.
 * Defines contract for making HTTP requests.
 * Implementation-agnostic - not tied to any specific HTTP library.
 */
export interface IHttpClient {
  /**
   * Perform a GET request.
   *
   * Parameters:
   * - url: Request URL path.
   * - config: Optional request configuration.
   *
   * Returns:
   * - Promise<T>: Promise resolving to response data of type T.
   */
  get<T = any>(url: string, config?: Record<string, any>): Promise<T>

  /**
   * Perform a POST request.
   *
   * Parameters:
   * - url: Request URL path.
   * - data: Request body data.
   * - config: Optional request configuration.
   *
   * Returns:
   * - Promise<T>: Promise resolving to response data of type T.
   */
  post<T = any>(url: string, data?: any, config?: Record<string, any>): Promise<T>

  /**
   * Perform a PUT request.
   *
   * Parameters:
   * - url: Request URL path.
   * - data: Request body data.
   * - config: Optional request configuration.
   *
   * Returns:
   * - Promise<T>: Promise resolving to response data of type T.
   */
  put<T = any>(url: string, data?: any, config?: Record<string, any>): Promise<T>

  /**
   * Perform a PATCH request.
   *
   * Parameters:
   * - url: Request URL path.
   * - data: Request body data.
   * - config: Optional request configuration.
   *
   * Returns:
   * - Promise<T>: Promise resolving to response data of type T.
   */
  patch<T = any>(url: string, data?: any, config?: Record<string, any>): Promise<T>

  /**
   * Perform a DELETE request.
   *
   * Parameters:
   * - url: Request URL path.
   * - config: Optional request configuration.
   *
   * Returns:
   * - Promise<T>: Promise resolving to response data of type T.
   */
  delete<T = any>(url: string, config?: Record<string, any>): Promise<T>
}
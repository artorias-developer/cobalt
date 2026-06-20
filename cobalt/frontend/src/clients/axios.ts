/*
 * Copyright (C) 2026 ArtoriasCode
 * Author: ArtoriasCode
 * Repository: https://github.com/ArtoriasCode/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import axios, { AxiosError } from "axios"
import type { AxiosInstance, AxiosRequestConfig, AxiosResponse } from "axios"
import type { Router } from "vue-router"
import { notify } from "@kyvg/vue3-notification"

import { RoutesEnum } from "@/types"
import type { IHttpClient } from "@/contracts"

/**
 * HTTP Client class for Cobalt API requests with centralized error handling
 * and automatic authentication redirects.
 */
export class HttpAxiosClient implements IHttpClient {
  private client: AxiosInstance
  private router: Router
  private isRedirecting = false

  /**
   * Creates a new HttpAxiosClient instance with configured axios client.
   *
   * Parameters:
   * - router: Router instance used for auth redirects.
   * - baseURL: Base URL for all API requests (default: empty string)
   */
  constructor(router: Router, baseURL?: string) {
    this.router = router

    this.client = axios.create({
      baseURL,
      timeout: 0,
      withCredentials: true,
      headers: {
        "Content-Type": "application/json"
      }
    })

    this.setupInterceptors()
  }

  /**
   * Setup request and response interceptors for the axios client.
   * Response interceptor handles errors globally.
   *
   * Parameters:
   * - null.
   *
   * Returns:
   * - void.
   */
  private setupInterceptors(): void {
    this.client.interceptors.response.use(
      (response) => response,
      (error: AxiosError) => {
        this.handleError(error)

        if (error.response?.status === 401) {
          return new Promise(() => {})
        }

        return Promise.reject(error)
      }
    )
  }

  /**
   * Handle HTTP errors with appropriate logging and redirects.
   * Redirects to login page on 401 Unauthorized (only once).
   *
   * Parameters:
   * - error: Axios error object containing response details.
   *
   * Returns:
   * - void.
   */
  private handleError(error: AxiosError): void {
    if (!error.response) {
      console.error("Network error:", error.message)
      return
    }

    const status = error.response.status

    if (status === 401) {
      if (this.router.currentRoute.value.name !== RoutesEnum.LOGIN && !this.isRedirecting) {
        this.isRedirecting = true
        notify({
          type: "error",
          text: (error.response.data as any)?.message ?? "Invalid session"
        })
        this.router.push({ name: RoutesEnum.LOGIN }).finally(() => {
          this.isRedirecting = false
        })
      }
    }
  }

  /**
   * Perform a GET request.
   *
   * Parameters:
   * - url: Request URL path.
   * - config: Optional Axios request configuration.
   *
   * Returns:
   * - Promise<T>: Promise resolving to response data of type T.
   */
  async get<T = any>(url: string, config?: AxiosRequestConfig): Promise<T> {
    const response: AxiosResponse<T> = await this.client.get(url, config)
    return response.data
  }

  /**
   * Perform a POST request.
   *
   * Parameters:
   * - url: Request URL path.
   * - data: Request body data.
   * - config: Optional Axios request configuration.
   *
   * Returns:
   * - Promise<T>: Promise resolving to response data of type T.
   */
  async post<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    const response: AxiosResponse<T> = await this.client.post(url, data, config)
    return response.data
  }

  /**
   * Perform a PUT request.
   *
   * Parameters:
   * - url: Request URL path.
   * - data: Request body data.
   * - config: Optional Axios request configuration.
   *
   * Returns:
   * - Promise<T>: Promise resolving to response data of type T.
   */
  async put<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    const response: AxiosResponse<T> = await this.client.put(url, data, config)
    return response.data
  }

  /**
   * Perform a PATCH request.
   *
   * Parameters:
   * - url: Request URL path.
   * - data: Request body data.
   * - config: Optional Axios request configuration.
   *
   * Returns:
   * - Promise<T>: Promise resolving to response data of type T.
   */
  async patch<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    const response: AxiosResponse<T> = await this.client.patch(url, data, config)
    return response.data
  }

  /**
   * Perform a DELETE request.
   *
   * Parameters:
   * - url: Request URL path.
   * - config: Optional Axios request configuration.
   *
   * Returns:
   * - Promise<T>: Promise resolving to response data of type T.
   */
  async delete<T = any>(url: string, config?: AxiosRequestConfig): Promise<T> {
    const response: AxiosResponse<T> = await this.client.delete(url, config)
    return response.data
  }
}
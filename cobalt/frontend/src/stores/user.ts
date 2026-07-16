// Copyright (C) 2026 Artorias
// Author: Artorias
// Repository: https://github.com/artorias-developer/cobalt
// SPDX-License-Identifier: AGPL-3.0-or-later

import { defineStore } from "pinia"
import { ref } from "vue"

import type { PermissionEnum, RoleEntity, UserEntity, UserMeEntity, SettingsEntity } from "@/types"

export const useUserStore = defineStore("user", () => {
  const user = ref<UserMeEntity | null>(null)

  /**
   * Sets the current authenticated user.
   *
   * Parameters:
   * - data: UserMeEntity to set.
   *
   * Returns:
   * - void.
   */
  function setUser(data: UserMeEntity): void {
    user.value = data
  }

  /**
   * Updates the current user from a UserEntity (after edit).
   * Preserves settings from the existing store state.
   *
   * Parameters:
   * - data: UserEntity to merge into the current user.
   *
   * Returns:
   * - void.
   */
  function updateUser(data: UserEntity): void {
    if (!user.value) return
    user.value = { ...user.value, ...data }
  }

  /**
   * Sets the current user's role.
   *
   * Parameters:
   * - role: Role entity to set.
   *
   * Returns:
   * - void.
   */
  function setUserRole(role: RoleEntity): void {
    if (!user.value) return
    user.value = { ...user.value, role }
  }

  /**
   * Sets the current user's settings.
   *
   * Parameters:
   * - settings: Settings entity to set.
   *
   * Returns:
   * - void.
   */
  function setUserSettings(settings: SettingsEntity): void {
    if (!user.value) return
    user.value = { ...user.value, settings }
  }

  /**
   * Clears the current authenticated user.
   *
   * Parameters:
   * - null.
   *
   * Returns:
   * - void.
   */
  function clearUser(): void {
    user.value = null
  }

  /**
   * Checks whether the current user has a specific permission.
   *
   * Parameters:
   * - permission: Permission to check.
   *
   * Returns:
   * - boolean: `true` if the user has the permission, `false` otherwise.
   */
  function hasPermission(permission: PermissionEnum): boolean {
    if (!user.value) return false
    return user.value.role.permissions.includes(permission)
  }

  /**
   * Checks whether the current user has at least one permission from the provided list.
   *
   * Parameters:
   * - permissions: Array of permissions to check.
   *
   * Returns:
   * - boolean: `true` if the user has at least one of the permissions, `false` otherwise.
   */
  function hasAnyPermission(permissions: PermissionEnum[]): boolean {
    const currentUser = user.value
    if (!currentUser) return false
    return permissions.some(permission => currentUser.role.permissions.includes(permission))
  }

  return { user, setUser, updateUser, setUserRole, setUserSettings, clearUser, hasPermission, hasAnyPermission }
})
<!--
  - Copyright (C) 2026 ArtoriasCode
  - Author: ArtoriasCode
  - Repository: https://github.com/ArtoriasCode/cobalt
  - SPDX-License-Identifier: AGPL-3.0-or-later
  -->

<template>
  <Block class="settings">
    <div class="heading">
      <Header
        :icon="settingsIcon"
        icon-color="blue"
        :title="$t('settings.title')"
        :description="$t('settings.description')"
        :icon-filled="true"
      />
    </div>
    <BlockTabs :tabs="tabs" v-model="activeTab">
      <template #general>
        <Form
          ref="generalSettingsForm"
          class="form"
          :on-submit="() => generalSettingsForm?.validate() && handleSave()"
        >
          <div class="field">
            <FieldLabel
              :text="$t('settings.general.theme.title')"
              :description="$t('settings.general.theme.description')"
            />
            <Select
              v-model="generalSettings.theme"
              :options="themeOptions"
              :placeholder="$t('settings.general.theme.placeholder')"
            />
          </div>
          <div class="field">
            <FieldLabel
              :text="$t('settings.general.timezone.title')"
              :description="$t('settings.general.timezone.description')"
            />
            <Select
              v-model="generalSettings.timezone"
              :options="timezoneOptions"
              :placeholder="$t('settings.general.timezone.placeholder')"
            />
          </div>
          <div class="field">
            <FieldLabel
              :text="$t('settings.general.language.title')"
              :description="$t('settings.general.language.description')"
            />
            <Select
              v-model="generalSettings.language"
              :options="languageOptions"
              :placeholder="$t('settings.general.language.placeholder')"
            />
          </div>
        </Form>
      </template>
      <template #security>
        <Form
          ref="securitySettingsForm"
          class="form"
          :on-submit="() => securitySettingsForm?.validate() && handleChangeCredentials()"
        >
          <div class="field">
            <FieldLabel
              :text="$t('settings.security.login.title')"
              :description="$t('settings.security.login.description')"
            />
            <Input
              v-model="securitySettings.login"
              :placeholder="$t('settings.security.login.placeholder')"
              name="login"
            />
          </div>
          <div class="field">
            <FieldLabel
              :text="$t('settings.security.password.title')"
              :description="$t('settings.security.password.description')"
            />
            <div class="inputs">
              <Input
                v-model="securitySettings.old_password"
                type="password"
                :placeholder="$t('settings.security.password.old.placeholder')"
                name="old-password"
              />
              <Input
                v-model="securitySettings.new_password"
                type="password"
                :placeholder="$t('settings.security.password.new.placeholder')"
                name="new-password"
              />
            </div>
          </div>
        </Form>
      </template>
      <template #system>
        <div v-if="hasSettingsSystemAccess" class="form">
          <div v-if="hasSettingsCacheClearAccess" class="field">
            <FieldLabel
              :text="$t('settings.system.cache.title')"
              :description="$t('settings.system.cache.description')"
            />
            <SolidButton
              type="button"
              :text="$t('common.clear')"
              color="gray"
              name="clear-cache"
              @click="handleClearCache"
            />
          </div>
          <div v-if="hasSettingsContainersClearAccess" class="field">
            <FieldLabel
              :text="$t('settings.system.containers.title')"
              :description="$t('settings.system.containers.description')"
            />
            <SolidButton
              type="button"
              :text="$t('common.clear')"
              color="gray"
              name="clear-containers"
              @click="handleClearContainers"
            />
          </div>
        </div>
        <div v-else class="empty-state">
          <Message
            :icon="padlockIcon"
            :text="$t('common.accessDenied')"
          />
        </div>
      </template>
    </BlockTabs>
    <div class="footer" v-if="activeTab !== 'system'">
      <SolidButton
        v-if="activeTab === 'general'"
        type="button"
        :text="$t('common.save')"
        color="blue"
        name="settings-save-general"
        @click="generalSettingsForm?.validate() && handleSave()"
      />
      <SolidButton
        v-if="activeTab === 'security'"
        type="button"
        :text="$t('common.save')"
        color="blue"
        name="settings-save-security"
        @click="securitySettingsForm?.validate() && handleChangeCredentials()"
      />
    </div>
  </Block>
</template>

<script setup lang="ts">
import { useI18n } from "vue-i18n"
import { ref, inject, onMounted, computed } from "vue"
import { useRouter } from "vue-router"
import { useNotification } from "@kyvg/vue3-notification"

import { HTTP_SETTINGS_API_SERVICE_KEY, HTTP_AUTH_API_SERVICE_KEY } from "@/utils"
import { useUserStore } from "@/stores"
import { LanguageEnum, PermissionsEnum, RoutesEnum } from "@/types"
import type { AuthChangeCredentialsRequest, SelectOption } from "@/types"

import Block from "@/components/ui/Block.vue"
import Header from "@/components/ui/Header.vue"
import FieldLabel from "@/components/ui/forms/FieldLabel.vue"
import Input from "@/components/ui/forms/Input.vue"
import Select from "@/components/ui/forms/Select.vue"
import SolidButton from "@/components/ui/forms/buttons/SolidButton.vue"
import Form from "@/components/ui/forms/Form.vue"
import Message from "@/components/ui/Message.vue"
import BlockTabs from "@/components/ui/tabs/BlockTabs.vue"
import settingsIcon from "@/assets/images/svg/settings.svg?raw"
import padlockIcon from "@/assets/images/svg/padlock.svg?raw"

const httpSettingsApiService = inject(HTTP_SETTINGS_API_SERVICE_KEY)!
const httpAuthApiService = inject(HTTP_AUTH_API_SERVICE_KEY)!
const userStore = useUserStore()
const { notify } = useNotification()
const { t } = useI18n()
const router = useRouter()

const activeTab = ref<string | null>(null)
const generalSettingsForm = ref<InstanceType<typeof Form> | null>(null)
const securitySettingsForm = ref<InstanceType<typeof Form> | null>(null)

const tabs = computed(() => [
  {
    label: t("settings.tabs.general"),
    value: "general"
  },
  {
    label: t("settings.tabs.security"),
    value: "security"
  },
  {
    label: t("settings.tabs.system"),
    value: "system"
  }
])

const generalSettings = ref({
  theme: "dark",
  timezone: "UTC",
  language: "en"
})

const securitySettings = ref({
  login: "",
  old_password: "",
  new_password: ""
})

const themeOptions = computed((): SelectOption[] => [
  {
    value: "dark",
    label: t("settings.general.theme.options.dark")
  }
])

const timezoneOptions: SelectOption[] = [
  {
    value: "UTC-12",
    label: "UTC-12"
  },
  {
    value: "UTC-11",
    label: "UTC-11"
  },
  {
    value: "UTC-10",
    label: "UTC-10"
  },
  {
    value: "UTC-9",
    label: "UTC-9"
  },
  {
    value: "UTC-8",
    label: "UTC-8"
  },
  {
    value: "UTC-7",
    label: "UTC-7"
  },
  {
    value: "UTC-6",
    label: "UTC-6"
  },
  {
    value: "UTC-5",
    label: "UTC-5"
  },
  {
    value: "UTC-4",
    label: "UTC-4"
  },
  {
    value: "UTC-3",
    label: "UTC-3"
  },
  {
    value: "UTC-2",
    label: "UTC-2"
  },
  {
    value: "UTC-1",
    label: "UTC-1"
  },
  {
    value: "UTC",
    label: "UTC"
  },
  {
    value: "UTC+1",
    label: "UTC+1"
  },
  {
    value: "UTC+2",
    label: "UTC+2"
  },
  {
    value: "UTC+3",
    label: "UTC+3"
  },
  {
    value: "UTC+4",
    label: "UTC+4"
  },
  {
    value: "UTC+5",
    label: "UTC+5"
  },
  {
    value: "UTC+6",
    label: "UTC+6"
  },
  {
    value: "UTC+7",
    label: "UTC+7"
  },
  {
    value: "UTC+8",
    label: "UTC+8"
  },
  {
    value: "UTC+9",
    label: "UTC+9"
  },
  {
    value: "UTC+10",
    label: "UTC+10"
  },
  {
    value: "UTC+11",
    label: "UTC+11"
  },
  {
    value: "UTC+12",
    label: "UTC+12"
  }
]

const languageOptions: SelectOption[] = [
  {
    value: LanguageEnum.EN,
    label: t("settings.general.language.options.en")
  },
  {
    value: LanguageEnum.RU,
    label: t("settings.general.language.options.ru")
  },
  {
    value: LanguageEnum.UK,
    label: t("settings.general.language.options.uk")
  }
]

/**
 * Loads settings from the user store into the form.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - void.
 */
function loadSettings(): void {
  const settings = userStore.user?.settings
  if (!settings) return

  generalSettings.value = {
    theme: settings.theme,
    timezone: settings.timezone,
    language: settings.language
  }

  securitySettings.value.login = userStore.user?.login ?? ""
}

/**
 * Saves the current settings form state via the API
 * and updates the user store on success.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - Promise<void>.
 */
async function handleSave(): Promise<void> {
  try {
    const updated = await httpSettingsApiService.updateMe({
      theme: generalSettings.value.theme,
      timezone: generalSettings.value.timezone,
      language: generalSettings.value.language
    })

    userStore.setUserSettings(updated)

    notify({
      type: "success",
      text: t("settings.general.save.success")
    })
  } catch (error: any) {
    notify({
      type: "error",
      text: error?.response?.data?.message ?? t("settings.general.save.error")
    })
  }
}

/**
 * Changes login and/or password via the API.
 * Clears the credentials form on success.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - Promise<void>.
 */
async function handleChangeCredentials(): Promise<void> {
  const payload: AuthChangeCredentialsRequest = {
    login: securitySettings.value.login || undefined,
    old_password: securitySettings.value.old_password || undefined,
    new_password: securitySettings.value.new_password || undefined
  }

  if (!payload.login && !payload.old_password && !payload.new_password) return

  try {
    await httpAuthApiService.changeCredentials(payload)

    if (payload.login && userStore.user) {
      userStore.updateUser({
        ...userStore.user,
        login: payload.login
      })
    }

    securitySettings.value = {
      login: securitySettings.value.login,
      old_password: "",
      new_password: ""
    }

    notify({
      type: "success",
      text: t("settings.security.save.success")
    })
  } catch (error: any) {
    notify({
      type: "error",
      text: error?.response?.data?.message ?? t("settings.security.save.error")
    })
  }
}

/**
 * Clears application cache via the API.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - Promise<void>.
 */
async function handleClearCache(): Promise<void> {
  try {
    await httpSettingsApiService.clearCache()
    userStore.clearUser()

    await router.push({
      name: RoutesEnum.LOGIN
    })

    notify({
      type: "success",
      text: t("settings.system.cache.clear.success")
    })
  } catch (error: any) {
    notify({
      type: "error",
      text: error?.response?.data?.message ?? t("settings.system.cache.clear.error")
    })
  }
}

/**
 * Clears unused containers data via the API.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - Promise<void>.
 */
async function handleClearContainers(): Promise<void> {
  try {
    await httpSettingsApiService.clearContainers()

    notify({
      type: "success",
      text: t("settings.system.containers.clear.success")
    })
  } catch (error: any) {
    notify({
      type: "error",
      text: error?.response?.data?.message ?? t("settings.system.containers.clear.error")
    })
  }
}

/**
 * Checks whether the current has access to at least one system setting.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - boolean: `true` if the user has the required permission, `false` otherwise.
 */
const hasSettingsSystemAccess = computed((): boolean =>
  userStore.hasAnyPermission([
    PermissionsEnum.SETTINGS_CACHE_CLEAR,
    PermissionsEnum.SETTINGS_CONTAINERS_CLEAR
  ])
)

/**
 * Checks whether the current user has access to clear cache.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - boolean: `true` if the user has the required permission, `false` otherwise.
 */
const hasSettingsCacheClearAccess = computed((): boolean =>
  userStore.hasPermission(PermissionsEnum.SETTINGS_CACHE_CLEAR)
)

/**
 * Checks whether the current user has access to clear containers.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - boolean: `true` if the user has the required permission, `false` otherwise.
 */
const hasSettingsContainersClearAccess = computed((): boolean =>
  userStore.hasPermission(PermissionsEnum.SETTINGS_CONTAINERS_CLEAR)
)

onMounted(() => {
  loadSettings()
})
</script>

<style scoped lang="scss">
.settings {
  min-height: 500px;

  .heading {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: $space-xl;
    padding: $space-xl;
  }

  .form {
    gap: 0;

    .field {
      display: flex;
      align-items: center;
      gap: $space-xl;
      padding: $space-xl 0;
      border-bottom: 1px solid $color-border-alt;

      .label {
        flex-shrink: 0;
        width: 100%;
        max-width: 400px;
      }

      .inputs {
        width: 100%;
        display: flex;
        gap: $space-md;
      }
    }
  }

  .empty-state {
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .footer {
    padding: $space-xl;
    border-top: 1px solid $color-border-alt;
  }
}

@media (max-width: 768px) {
  .settings {
    .heading {
      gap: $space-lg;
      padding: $space-lg;
    }

    .form {
      .field {
        flex-direction: column;
        align-items: flex-start;
        gap: $space-lg;
        padding: $space-lg 0;

        &:last-child {
          border-bottom: none;
        }

        .label {
          width: 100%;
        }

        .inputs {
          width: 100%;
          flex-direction: column;
        }
      }

      .empty {
        font-size: $font-sm;
        padding: $space-lg 0;
      }
    }

    .footer {
      padding: $space-lg;
    }
  }
}
</style>
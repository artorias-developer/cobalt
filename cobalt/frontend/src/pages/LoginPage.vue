<!--
  - Copyright (C) 2026 ArtoriasCode
  - Author: ArtoriasCode
  - Repository: https://github.com/ArtoriasCode/cobalt
  - SPDX-License-Identifier: AGPL-3.0-or-later
  -->

<template>
  <div class="page">
    <Block class="login" padded gapped>
      <ul class="header">
        <li class="image">
          <div class="icon">
            <img :src="logoIcon" alt="Logo"/>
          </div>
        </li>
        <li class="text">
          <h2>Cobalt</h2>
        </li>
      </ul>
      <Form
        ref="loginForm"
        class="form"
        :on-submit="() => loginForm?.validate() && handleLogin()"
      >
        <Input
          v-model="login"
          :validationName="$t('login.login.label')"
          :label="$t('login.login.label')"
          :placeholder="$t('login.login.placeholder')"
          name="login"
          :required="true"
        />
        <Input
          v-model="password"
          :validationName="$t('login.password.label')"
          :label="$t('login.password.label')"
          :placeholder="$t('login.password.placeholder')"
          name="password"
          :required="true"
        />
      </Form>
      <div class="actions">
        <SolidButton
          type="button"
          :text="$t('login.signIn.label')"
          color="blue"
          name="sign-in"
          @click="loginForm?.validate() && handleLogin()"
        />
      </div>
    </Block>
  </div>
</template>

<script setup lang="ts">
import { ref, inject } from "vue"
import { useI18n } from "vue-i18n"
import { useRouter } from "vue-router"
import { useNotification } from "@kyvg/vue3-notification"

import { HTTP_AUTH_API_SERVICE_KEY, HTTP_USERS_API_SERVICE_KEY, WS_CLIENT_KEY } from "@/utils"
import { useUserStore } from "@/stores"
import { RoutesEnum } from "@/types"

import Block from "@/components/ui/Block.vue"
import Input from "@/components/ui/forms/Input.vue"
import SolidButton from "@/components/ui/forms/buttons/SolidButton.vue"
import Form from "@/components/ui/forms/Form.vue"
import logoIcon from "@/assets/images/svg/logo.svg"

const httpAuthApiService = inject(HTTP_AUTH_API_SERVICE_KEY)!
const httpUsersApiService = inject(HTTP_USERS_API_SERVICE_KEY)!
const wsClient = inject(WS_CLIENT_KEY)!
const userStore = useUserStore()
const router = useRouter()
const { notify } = useNotification()
const { t } = useI18n()

const loginForm = ref<InstanceType<typeof Form> | null>(null)
const login = ref<string>("")
const password = ref<string>("")

/**
 * Handles the login form submission.
 * On success fetches the current user and redirects to the dashboard.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - Promise<void>.
 */
async function handleLogin(): Promise<void> {
  try {
    await httpAuthApiService.login({
      login: login.value,
      password: password.value
    })

    const user = await httpUsersApiService.getMe()
    userStore.setUser(user)

    if (!wsClient.isConnected()) {
      wsClient.connect(`wss://${window.location.host}/api/v1/ws`)
    }

    await router.push({
      name: RoutesEnum.DASHBOARD
    })
  } catch (error: any) {
    notify({
      type: "error",
      text: error?.response?.data?.message ?? t("login.signIn.error")
    })
  }
}
</script>

<style scoped lang="scss">
.page {
  width: 100%;
  height: 100vh;
  height: 100dvh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: $space-xl;
  box-sizing: border-box;

  .login {
    max-width: 420px;

    .header {
      display: flex;
      justify-content: center;
      align-items: center;
      gap: $space-md;

      .image {
        .icon {
          width: 26px;
          height: 26px;

          img {
            width: 100%;
            height: 100%;
          }
        }
      }

      .text {
        display: flex;
        flex-direction: column;
        gap: $space-sm;

        h2 {
          font-size: $font-xxl;
          font-weight: 700;
          color: var(--color-title);
          line-height: 1;
        }

        p {
          font-size: $font-sm;
          font-weight: 600;
          color: var(--color-description);
          line-height: 1;
          text-wrap: nowrap;
        }
      }
    }

    .actions {
      display: flex;
      flex-direction: column;

      .button {
        width: 100%;
      }
    }
  }
}

@media (max-width: 768px) {
  .page {
    padding: $space-md;
  }
}
</style>
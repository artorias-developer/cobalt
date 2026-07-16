import { createApp } from "vue"

import { bootstrap } from "@/boostrap"

import App from "@/App.vue"

const app = createApp(App)

bootstrap(app)
app.mount("#app")
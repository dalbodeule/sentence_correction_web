// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: true },
  app: {
    head: {
      charset: "utf-8",
      viewport: "width=device-width, initial-scale=1"
    }
  },
  modules: [
      "@pinia/nuxt"
  ],
  runtimeConfig: {
    public: {
      BACKEND_URL: process.env.BACKEND_URL ?? "http://localhost:8000"
    }
  }
})

// https://nuxt.com/docs/api/configuration/nuxt-config



import {viteCommonjs} from "@originjs/vite-plugin-commonjs";

export default defineNuxtConfig({
  devtools: { enabled: true },
  css: [
    '@fortawesome/fontawesome-svg-core/styles.css'
  ],
  app: {
    head: {
      charset: "utf-8",
      viewport: "width=device-width, initial-scale=1"
    }
  },
  modules: [
    "@pinia/nuxt",
    "nuxt-gtag",
    "@nuxtjs/google-adsense"
  ],
  runtimeConfig: {
    public: {
      backendUrl: process.env.NUXT_BACKEND_URL ?? "http://localhost:8000"
    }
  },
  gtag: {
    id: 'G-8YGDCCQEZT'
  },
  googleAdsense: {
    id: 'ca-pub-2810659463174293'
  },
  vite: {
    plugins: [
      viteCommonjs()
    ]
  }
})

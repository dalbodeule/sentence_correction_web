// https://nuxt.com/docs/api/configuration/nuxt-config
import {viteCommonjs} from "@originjs/vite-plugin-commonjs";

export default defineNuxtConfig({
  devtools: { enabled: true },
  build: {
    transpile: ['diff', 'Dayjs'],
  },
  css: [
    '@fortawesome/fontawesome-svg-core/styles.css'
  ],
  app: {
    head: {
      meta: [
        { name: 'charset', content: 'utf-8' },
        { name: 'viewport', content: "width=device-width, initial-scale=1" },
        { name: 'naver-site-verification', content: "580bdcf52bca3a7aeb0714be32c41d3b5b98436f" }
      ]
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
})

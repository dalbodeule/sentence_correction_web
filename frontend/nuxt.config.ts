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
      "@pinia/nuxt",
      "nuxt-gtag",
      "@nuxtjs/google-adsense"
  ],
  runtimeConfig: {
    public: {
      backendUrl: "http://localhost:8000"
    }
  },
  gtag: {
    id: 'G-8YGDCCQEZT'
  },
  googleAdsense: {
    id: 'ca-pub-2810659463174293'
  }
})

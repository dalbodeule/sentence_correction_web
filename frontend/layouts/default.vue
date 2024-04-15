<script setup lang="ts">
import { useAuthStore } from "~/stores/auth";

const user = useAuthStore()

;(async() => {
  await user.getUserMeta()
})()
</script>

<template>
  <Header />
  <Adsbygoogle ad-slot="2521832268" ad-format="fluid" ad-layout-key="-6t+ed+2i-1n-4w" />
  <NuxtPage />
  <Footer />
</template>

<style src="~/node_modules/bulma/bulma.scss"></style>/
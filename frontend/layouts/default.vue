<script setup lang="ts">
import { useAuthStore } from "~/stores/auth";

const user = useAuthStore()

;(async() => {
  await user.getUserMeta()
})()
</script>

<template>
  <Header />
  <div class="container" style="margin-top: 20px; min-height: 80vh;">
    <Adsbygoogle ad-slot="8101462005" ad-format="auto" v-bind:ad-full-width-responsive="true" />
    <NuxtPage />
    <Adsbygoogle ad-slot="2521832268" ad-format="fluid" ad-layout-key="-6t+ed+2i-1n-4w" />
  </div>
  <Footer />
</template>

<style src="~/node_modules/bulma/bulma.scss"></style>/
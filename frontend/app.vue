<script setup lang="ts">
import {useAuthStore} from "~/stores/auth";

useHead({
  title: '맞춤법 검사기'
})

const user = useAuthStore()

;(async() => {
  await user.getUserMeta()
})()
</script>

<template>
  <Header />
  <NuxtPage />
  <Footer />
</template>

<style src="node_modules/bulma/bulma.scss"></style>/
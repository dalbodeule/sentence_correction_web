<script setup lang="ts">
import {useAuthStore} from "~/stores/auth";

const auth = useAuthStore()
const router = useRouter()
const config = useRuntimeConfig()

useHead({
  title: '맞춤법 검사기 :: 로그인'
})

const methods: Array<{url: string, display: string, vendor: string}> = [
  { url: `${config.public.backendUrl}/login/google`, display: 'Google로 로그인', vendor: 'google'},
]

if (auth.authenticated) {
  router.push('/')
}
</script>

<template>
  <div class="container">
    <div class="box">
      <div v-for="method in methods">
        <a v-bind:href="method.url" class="button is-align-self-center">{{ method.display }}</a>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>
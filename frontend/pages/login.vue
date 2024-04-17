<script setup lang="ts">
import {useAuthStore} from "~/stores/auth";

const auth = useAuthStore()
const router = useRouter()
const config = useRuntimeConfig()

useHead({
  title: '맞춤법 검사기 :: 로그인'
})

const methods: Array<{url: string, display: string, id: string, color: string, bgcolor: string, icon: boolean}> = [
  { url: `${config.public.backendUrl}/login/google`, display: 'Google 로그인', id: 'google', icon: true, color: '#444', bgcolor: '#ffffff'},
//  { url: `${config.public.backendUrl}/login/naver`, display: 'Naver 로그인', id: 'naver', icon: false, color: '#ffffff', bgcolor: '#03c75a'},
  { url: `${config.public.backendUrl}/login/github`, display: 'Github 로그인', id: 'github', icon: true, color: '#333', bgcolor: '#fafafa'},
]

if (auth.authenticated) {
  router.push('/')
}
</script>

<template>
  <div class="container box" style="min-height: 80vh">
    <div v-for="method in methods" style="margin-left: auto; margin-top: 20px;">
      <a v-if="method.icon" v-bind:href="method.url" class="button is-align-self-center" v-bind:style="`background: ${method.bgcolor}; color: ${method.color}; width: 180px;`">
        <font-awesome-icon :icon="['fab', method.id]"/>&nbsp; {{ method.display }}
      </a>
      <a v-else v-bind:href="method.url" class="button is-align-self-center" v-bind:style="`background: ${method.bgcolor}; color: ${method.color}; width: 180px;`">
        <img v-bind:src="`/${method.id}-logo.png`" alt="" style="height: 20px"/>&nbsp; {{ method.display }}
      </a>
    </div>
  </div>
</template>

<style scoped>

</style>
<script setup lang="ts">
import {useAuthStore, UserRole} from "~/stores/auth";

const user = useAuthStore()
const router = useRouter()

useHead({
  title: "맞춤법 검사기 :: 관리자 페이지",
})

useSeoMeta({
  robots: { index: false }
})

;(async() => {
  if(!user.authenticated ||!(user.userInfo.role == UserRole.ADMIN || user.userInfo.role == UserRole.MODERATOR))
    await router.push('/')
})()
</script>

<template>
  <div class="box">

  </div>
</template>

<style scoped>

</style>
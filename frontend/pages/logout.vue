<script setup lang="ts">
import {useAuthStore} from "~/stores/auth";

const auth = useAuthStore()
const router = useRouter()

useHead({
  title: '맞춤법 검사기 :: 로그아웃'
})

;(async() => {
  try {
    if(auth.authenticated) await auth.logout()
  } catch(e) {
    console.log(e)
  } finally {
    await router.push('/')
  }
})()
</script>

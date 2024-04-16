import { defineStore } from 'pinia';
import nuxt from 'nuxt';

interface IUser {
  name: string,
  email: string,
  id: number,
  profile: string
}

export const useAuthStore = defineStore('auth', () => {
  const authenticated = ref(false)
  const loading = ref(false)
  const userInfo = ref({
    name: "",
    email: "",
    id: 0,
    profile: '',
  })

  const config = useRuntimeConfig()
  const BASE_URL = config.public.backendUrl

  const getUserMeta = async () => {
    loading.value = true
    try {
      const response: IUser = await $fetch(`${BASE_URL}/login/username`, {
        method: "GET",
        credentials: 'include',
      })
      if (response) {
        userInfo.value.id = response.id
        userInfo.value.profile = response.profile
        userInfo.value.name = response.name
        userInfo.value.email = response.email
        authenticated.value = true
      } else {
        // refreshToken.value = null
        authenticated.value = false

        // await refresh()
        await getUserMeta()
      }
    } catch(e) {
      userInfo.value = { id: 0, email: "", profile: "", name: "" }
      authenticated.value = false
    }
  }

  const logout = async () => {
    loading.value = true
    try {
      const response = await $fetch(`${BASE_URL}/login/logout`, {
        credentials: 'include',
      })
    } catch(e) {
      throw e
    } finally {
      loading.value = false
      authenticated.value = false
      userInfo.value = {
        id: 0,
        email: "",
        name: "",
        profile: '',
      }
      loading.value = false
    }
  };

  return { authenticated, loading, logout, userInfo, getUserMeta }
});

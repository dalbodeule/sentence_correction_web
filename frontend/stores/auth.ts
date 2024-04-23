import { defineStore } from 'pinia';
import nuxt from 'nuxt';

export enum UserRole {
  ADMIN = 2,
  MODERATOR = 1,
  USER = 0
}

interface IUser {
  name: string,
  email: string,
  id: number,
  profile: string,
  role: number
}

export const useAuthStore = defineStore('auth', () => {
  const authenticated = ref(false)
  const loading = ref(false)
  const userInfo = ref({
    name: "",
    email: "",
    id: 0,
    profile: '',
    role: UserRole.USER
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
        userInfo.value.role = response.role as UserRole
        authenticated.value = true
      } else {
        // refreshToken.value = null
        authenticated.value = false

        // await refresh()
        await getUserMeta()
      }
    } catch(e) {
      userInfo.value = { id: 0, email: "", profile: "", name: "", role: UserRole.USER }
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
        role: UserRole.USER
      }
      loading.value = false
    }
  };

  return { authenticated, loading, logout, userInfo, getUserMeta, UserRole }
});

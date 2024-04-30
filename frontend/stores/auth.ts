import { defineStore } from 'pinia';

export enum UserRole {
  ADMIN = 2,
  MODERATOR = 1,
  USER = 0
}

const _15MIN = 15 * 60 * 1000;

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
    role: UserRole.USER,
    lastUpdate: new Date()
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
        userInfo.value = {
          id: response.id,
          profile: response.profile,
          name: response.name,
          email: response.email,
          role: response.role as UserRole,
          lastUpdate: new Date(),
        }
        authenticated.value = true
      } else {
        // refreshToken.value = null
        authenticated.value = false
        userInfo.value = {
          name: "",
          email: "",
          id: 0,
          profile: '',
          role: UserRole.USER,
          lastUpdate: new Date()
        }

        await getUserMeta()
      }
    } catch(e) {
      userInfo.value = { id: 0, email: "", profile: "", name: "", role: UserRole.USER, lastUpdate: new Date() }
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
        role: UserRole.USER,
        lastUpdate: new Date()
      }
      loading.value = false
    }
  };

  const refreshToken = async () => {
    if (userInfo.value.lastUpdate.getTime() + _15MIN > new Date().getTime())
      return
    if (!authenticated) return

    loading.value = true
    try {
      const response: IUser = await $fetch(`${BASE_URL}/login/refresh`, {
        method: "GET",
        credentials: 'include',
      })
      userInfo.value = {
        id: response.id,
        profile: response.profile,
        name: response.name,
        email: response.email,
        role: response.role as UserRole,
        lastUpdate: new Date(),
      }
      authenticated.value = true
    } catch(e) {
      authenticated.value = false
      userInfo.value = {
        id: 0,
        email: "",
        name: "",
        profile: '',
        role: UserRole.USER,
        lastUpdate: new Date()
      }
    } finally {
      loading.value = false
    }
  }

  return { authenticated, loading, logout, userInfo, getUserMeta, UserRole, refreshToken }
});

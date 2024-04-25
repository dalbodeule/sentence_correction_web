<script setup lang="ts">
import type {Ref} from "vue";

const opened = ref(false)
const content: Ref<{id: number, user_id: number, content: string, created_at: Date, updated_at: Date} | null> = ref(null)
const config = useRuntimeConfig()

const close = () => {
  opened.value = false
}

;(async () => {
  const data: {id: number, user_id: number, content: string, created_at: string, updated_at: string} | null =
      await $fetch(`${config.public.backendUrl}/notification/latest`, {
        method: 'GET'
      })
  if(data) {
    content.value = {
      id: data.id,
      user_id: data.user_id,
      content: data.content,
      created_at: new Date(data.created_at),
      updated_at: new Date(data.updated_at),
    }
    opened.value = true
  }
})()
</script>

<template>
<div class="notification is-warning" v-if="opened">
  <p>{{ content?.content || "" }}</p>
  <button class="delete" @click="close"></button>
</div>
</template>

<style scoped>

</style>
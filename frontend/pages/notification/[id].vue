<script setup lang="ts">
import type {Ref} from "vue";
import {useAuthStore, UserRole} from "~/stores/auth";
import dayjs from "dayjs";

const config = useRuntimeConfig()

useHead({
  title: '맞춤법 검사기 :: 공지사항',
  meta: [
    { name: 'description', content: '맞춤법 검사기 - AI 기반의 맞춤법 검사기!'}
  ],
  htmlAttrs: {
    lang: 'ko'
  }
})
useSeoMeta({
  ogTitle: '맞춤법 검사기 :: 공지사항',
  ogType: 'website',
  ogSiteName: '맞춤법 검사기',
  ogDescription: '맞춤법 검사기 - AI 기반의 맞춤법 검사기!',
  ogImage: '/favicon.png',
  robots: {
    all: true
  }
})

interface IDataset {
  id: number,
  user_id: number,
  content: string,
  created_at: Date,
  updated_at: Date
}

const route = useRoute()
const user = useAuthStore()
const page = ref(parseInt(<string>route.params.id) ?? 1)

const notificationId = ref(0)
const notificationContent = ref("")

const maxPage = ref(0)
const elements: Ref<IDataset[]> = ref([])

const update = async (page: number) => {
  const p: {size: number, pages: number} = await $fetch(`${config.public.backendUrl}/notification/size`, {
      method: 'GET'
    })
  maxPage.value = p.pages
  if(page < 0 || page > maxPage.value) { return }

  const q: { id: number, user_id: number, content: string, created_at: string, updated_at: string}[] =
      await $fetch(`${config.public.backendUrl}/notification/list/${page}`, {
        method: 'GET',
        credentials: 'include',
      })
  elements.value = []
  q.map((value) => {
    elements.value.push({
      id: value.id,
      user_id: value.user_id,
      content: value.content,
      created_at: new Date(value.created_at),
      updated_at: new Date(value.updated_at),
    })
  })
}

const addOrUpdate = async (id: number = 0) => {
  if (user.userInfo.role != UserRole.ADMIN && user.userInfo.role != UserRole.MODERATOR)
    return

  const d = await $fetch(`${config.public.backendUrl}/notification/create`, {
    method: 'POST',
    credentials: 'include',
    body: JSON.stringify({ id, content: notificationContent.value })
  })

  await update(1)
}

const updateSet = (id: number = 0, content: string = '') => {
  if (user.userInfo.role != UserRole.ADMIN && user.userInfo.role != UserRole.MODERATOR)
    return

  notificationId.value = id
  notificationContent.value = content
}

const removeNotification = (id: number = 0) => {
  if (user.userInfo.role != UserRole.ADMIN && user.userInfo.role != UserRole.MODERATOR)
    return

}


;(async() => {
  await update(page.value)
})()
</script>

<template>
  <div class="box">
    <table class="table is-fullwidth is-striped">
      <thead>
        <tr>
          <th>ID</th>
          <th>메세지</th>
          <th>생성일</th>
          <th>업데이트</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="element in elements" :key="element.id">
          <td>{{ element.id }}</td>
          <td>{{ element.content }}
            <div v-if="user.userInfo.role == UserRole.ADMIN || user.userInfo.role == UserRole.MODERATOR" style="display: inline-block; float: right;">
              <button @click="updateSet(element.id, element.content)"><font-awesome-icon :icon="['fas', 'pencil']" /></button> &nbsp;
              <button @click="removeNotification(element.id)"><font-awesome-icon :icon="['fas', 'x']" /></button>
            </div>
          </td>
          <td>{{ dayjs(element.created_at).format('YYYY-MM-DD HH:mm:ss') }}</td>
          <td>{{ dayjs(element.updated_at).format('YYYY-MM-DD HH:mm:ss') }}</td>
        </tr>
      </tbody>
    </table>
    <div style="height: 5em">
      <form class="form-control" @submit.prevent="addOrUpdate(notificationId)"  v-if="user.userInfo.role == UserRole.MODERATOR || user.userInfo.role == UserRole.ADMIN">
        <div class="field has-addons">
          <p class="control">
            <button class="button" @click="updateSet()" type="button">{{ notificationId }}</button>
          </p>
          <div class="control is-expanded">
            <input type="text" class="input" maxlength="250" placeholder="공지해야 할 내용을 적어주세요." v-model="notificationContent">
          </div>
          <div class="control">
            <input type="submit" class="button" value="공지하기!">
          </div>
        </div>
      </form>
    </div>
    <nav class="pagination is-centered" role="pagination" aria-label="Page navigation">
      <NuxtLink v-bind:href="`/notification/${page - 1}`" :disabled="page == 1" class="pagination-previous">이전</NuxtLink>
      <NuxtLink v-bind:href="`/notification/${page + 1}`" :disabled="page - 1 == maxPage" class="pagination-next">다음</NuxtLink>
      <ul class="pagination-list">
        <li>
          <NuxtLink href="/list/1" class="pagination-link" aria-label="Goto page 1">1</NuxtLink>
        </li>
        <li>
          <span class="pagination-ellipsis">&hellip;</span>
        </li>
        <li>
          <NuxtLink class="pagination-link" v-bind:href="`/notification/${page - 1}`" :disabled="page == 1" :aria-label="`Goto page ${page - 1}`">{{ page - 1}}</NuxtLink>
        </li>
        <li>
          <a class="pagination-link is-current" :aria-label="`Page ${page}`" aria-current="page">{{ page }}</a>
        </li>
        <li>
          <NuxtLink class="pagination-link" v-bind:href="`/notification/${page + 1}`" :disabled="page == 1" :aria-label="`Goto page ${page + 1}`">{{ page + 1}}</NuxtLink>
        </li>
        <li>
          <span class="pagination-ellipsis">&hellip;</span>
        </li>
        <li>
          <NuxtLink :href="`/list/${maxPage}`" class="pagination-link" :aria-label="`Goto page ${maxPage}`">{{ maxPage }}</NuxtLink>
        </li>
      </ul>
    </nav>
  </div>
</template>

<style scoped>
  [disabled] {
    pointer-events: none;
  }
</style>
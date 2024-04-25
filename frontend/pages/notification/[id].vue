<script setup lang="ts">
import type {Ref} from "vue";

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
const page = ref(parseInt(<string>route.params.id) ?? 1)

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

(async() => {
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
          <td>{{ element.content }}</td>
          <td>{{ element.created_at.toISOString().replace("T", " ").substring(0, 19) }}</td>
          <td>{{ element.updated_at.toISOString().replace("T", " ").substring(0, 19) }}</td>
        </tr>
      </tbody>
    </table>
    <div style="height: 5em;"/>
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
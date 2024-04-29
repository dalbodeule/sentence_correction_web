<script setup lang="ts">
import type {Ref} from "vue";
import dayjs from "dayjs";

const config = useRuntimeConfig()

useHead({
  title: '맞춤법 검사기 :: 규칙 제안 리스트',
  meta: [
    { name: 'description', content: '맞춤법 검사기 - AI 기반의 맞춤법 검사기!'}
  ],
  htmlAttrs: {
    lang: 'ko'
  }
})
useSeoMeta({
  ogTitle: '맞춤법 검사기 :: 규칙 제안 리스트',
  ogType: 'website',
  ogSiteName: '맞춤법 검사기',
  ogDescription: '맞춤법 검사기 - AI 기반의 맞춤법 검사기!',
  ogImage: '/favicon.png',
  robots: {
    all: true
  }
})

enum DatasetStatus {
  PENDING = 0,
  APPROVED = 1,
  REJECTED = 2,
}

interface IDataset{
    id: number
    text: string
    correction: string
    memo: string
    status: DatasetStatus
    created_at: Date
    updated_at: Date
}

const route = useRoute()
const page = ref(parseInt(<string>route.params.id) ?? 1)

const maxPage = ref(0)
const elements: Ref<IDataset[]> = ref([])

const update = async (page: number) => {
  const p: {size: number, pages: number} = await $fetch(`${config.public.backendUrl}/dataset/size`, {
      method: 'GET'
    })
  maxPage.value = p.pages
  if(page < 0 || page > maxPage.value) { return }

  const q: { id: number, text: string, correction: string, memo: string, status: DatasetStatus, created_at: string, updated_at: string}[] =
      await $fetch(`${config.public.backendUrl}/dataset/list/${page}`, {
        method: 'GET',
        credentials: 'include',
      })
  elements.value = []
  q.map((value) => {
    elements.value.push({
      id: value.id,
      text: value.text,
      correction: value.correction,
      memo: value.memo,
      status: value.status,
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
          <th>원 문장</th>
          <th>교정 문장</th>
          <th>메모</th>
          <th style="width: 5em;">상태</th>
          <th style="width: 8em;">생성일</th>
          <th style="width: 8em;">업데이트</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="element in elements" :key="element.id">
          <td>{{ element.id }}</td>
          <td>{{ element.text }}</td>
          <td>{{ element.correction }}</td>
          <td>{{ element.memo }}</td>
          <td v-if="element.status == DatasetStatus.APPROVED" class="is-primary">승인</td>
          <td v-else-if="element.status == DatasetStatus.REJECTED" class="is-warning">거부</td>
          <td v-else class="is-info">대기중</td>
          <td>{{ dayjs(element.created_at).format('YYYY-MM-DD HH:mm:ss') }}</td>
          <td>{{ dayjs(element.updated_at).format('YYYY-MM-DD HH:mm:ss') }}</td>
        </tr>
      </tbody>
    </table>
    <div style="height: 5em;"/>
    <nav class="pagination is-centered" role="pagination" aria-label="Page navigation">
      <NuxtLink v-bind:href="`/link/${page - 1}`" :disabled="page == 1" class="pagination-previous">이전</NuxtLink>
      <NuxtLink v-bind:href="`/link/${page + 1}`" :disabled="page - 1 == maxPage" class="pagination-next">다음</NuxtLink>
      <ul class="pagination-list">
        <li>
          <NuxtLink href="/list/1" class="pagination-link" aria-label="Goto page 1">1</NuxtLink>
        </li>
        <li>
          <span class="pagination-ellipsis">&hellip;</span>
        </li>
        <li>
          <NuxtLink class="pagination-link" v-bind:href="`/link/${page - 1}`" :disabled="page == 1" :aria-label="`Goto page ${page - 1}`">{{ page - 1}}</NuxtLink>
        </li>
        <li>
          <a class="pagination-link is-current" :aria-label="`Page ${page}`" aria-current="page">{{ page }}</a>
        </li>
        <li>
          <NuxtLink class="pagination-link" v-bind:href="`/link/${page + 1}`" :disabled="page == 1" :aria-label="`Goto page ${page + 1}`">{{ page + 1}}</NuxtLink>
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
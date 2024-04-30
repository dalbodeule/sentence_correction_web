<script setup lang="ts">
import type {Ref} from "vue";
import dayjs from "dayjs";
import {useAuthStore} from "~/stores/auth";
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";
import {DatasetStatus, LOADING} from "~/common/enum";

const config = useRuntimeConfig()
const user = useAuthStore()

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

const modModal = ref(false)
const modIdx = ref(0)
const modStatus = ref(DatasetStatus.PENDING)
const modLoadingStatus = ref(LOADING.DEFAULT)
const modMemo = ref("")

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

const showModModal = (idx: number) => {
  modModal.value = true
  modIdx.value = idx

  const data = elements.value.find((item) => item.id === idx)

  modStatus.value = data!!.status
  modMemo.value = data!!.memo
}

const setStatus = async () => {
  if(user.userInfo.role != UserRole.ADMIN && user.userInfo.role != UserRole.MODERATOR) return

  modLoadingStatus.value = LOADING.LOADING

  try {
    const q: { id: number }[] =
      await $fetch(`${config.public.backendUrl}/dataset/setstatus`, {
        method: 'POST',
        credentials: 'include',
        body: JSON.stringify({id: modIdx.value, status: modStatus.value, memo: modMemo.value}),
      })
    modLoadingStatus.value = LOADING.DONE

    setTimeout(async () => { modModal.value = false }, 3000)
    await update(page.value)
  } catch(e) {
    console.log(e)
    modLoadingStatus.value = LOADING.ERROR
  }
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
          <th style="width: 6em;">상태</th>
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
          <td v-if="element.status == DatasetStatus.APPROVED" class="is-primary" @click="showModModal(element.id)">
            승인 <font-awesome-icon :icon="['fas', 'pencil']" v-if="user.userInfo.role == UserRole.ADMIN || user.userInfo.role == UserRole.MODERATOR" />
          </td>
          <td v-else-if="element.status == DatasetStatus.REJECTED" class="is-warning" @click="showModModal(element.id)">
            거부 <font-awesome-icon :icon="['fas', 'pencil']" v-if="user.userInfo.role == UserRole.ADMIN || user.userInfo.role == UserRole.MODERATOR" />
          </td>
          <td v-else class="is-info" @click="showModModal(element.id)">
            대기중 <font-awesome-icon :icon="['fas', 'pencil']" v-if="user.userInfo.role == UserRole.ADMIN || user.userInfo.role == UserRole.MODERATOR" />
          </td>
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

  <div class="modal" v-bind:class="modModal ? 'is-active' : ''">
    <div class="modal-background"></div>
    <form class="modal-card" @submit.prevent="setStatus">
      <div class="modal-card-head">
        <p class="modal-card-title">제안 수정하기</p>
        <button class="delete" type="button" aria-label="close" @click="modModal = false"></button>
      </div>
      <section class="modal-card-body">
        <p class="title">제안 수정 내용을 확인해주세요!</p>
        <table class="table is-fullwidth is-striped">
          <thead>
            <tr>
              <th style="width: 4em;">구분</th>
              <th>내용</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>ID</td>
              <td>{{ modIdx }}</td>
            </tr>
            <tr>
              <td>상태</td>
              <td>
                <div class="buttons has-addons">
                  <button class="button is-info" :class="modStatus == DatasetStatus.PENDING ? 'is-active' : ''" @click="modStatus = DatasetStatus.PENDING" type="button">
                    대기중
                  </button>
                  <button class="button is-primary" :class="modStatus == DatasetStatus.APPROVED ? 'is-active' : ''" @click="modStatus = DatasetStatus.APPROVED" type="button">
                    승인
                  </button>
                  <button class="button is-warning" :class="modStatus == DatasetStatus.REJECTED ? 'is-active' : ''" @click="modStatus = DatasetStatus.REJECTED" type="button">
                    거부
                  </button>
                </div>
              </td>
            </tr>
            <tr>
              <td>메모</td>
              <td><input class="input" type="text" v-model="modMemo" maxlength="250"></td>
            </tr>
          </tbody>
        </table>
        <div class="notification is-success" v-if="modLoadingStatus == LOADING.DONE">
          제안 수정에 성공했습니다.
        </div>
        <div class="notification is-warning" v-else-if="modLoadingStatus == LOADING.ERROR">
          제안 수정에 실패했습니다.
        </div>
      </section>
      <footer class="modal-card-foot">
        <div class="buttons">
          <button class="button is-success" type="submit" :disabled="modLoadingStatus == LOADING.LOADING">수정하기</button>
          <button class="button" @click="modModal=false" type="button" :disabled="modLoadingStatus == LOADING.LOADING">취소</button>
        </div>
      </footer>
    </form>
  </div>
</template>

<style scoped>
  [disabled] {
    pointer-events: none;
  }
</style>
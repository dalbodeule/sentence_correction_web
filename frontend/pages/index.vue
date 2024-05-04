<script setup lang="ts">
import {useAuthStore} from "~/stores/auth";
import type {Ref} from "vue";
import {LOADING} from "~/common/enum";
import useGoogleRecaptcha from "~/composables/useGoogleRecaptcha";

const content = ref("")
const loading = ref(LOADING.DEFAULT)

const postModal = ref(false)
const originText = ref("")
const fixedText = ref("")
const memo = ref("")
const postLoading = ref(LOADING.DEFAULT)

const phrases: Ref<string[]> = ref([])
const correction: Ref<string[]> = ref([])
const result: Ref<string[]> = ref([])

const auth = useAuthStore()
const config = useRuntimeConfig()

const { executeRecaptcha } = useGoogleRecaptcha()

useHead({
  title: '맞춤법 검사기',
  meta: [
    { name: 'description', content: '맞춤법 검사기 - AI 기반의 맞춤법 검사기!'}
  ],
  htmlAttrs: {
    lang: 'ko'
  }
})
useSeoMeta({
  ogTitle: '맞춤법 검사기',
  ogType: 'website',
  ogSiteName: '맞춤법 검사기',
  ogDescription: '맞춤법 검사기 - AI 기반의 맞춤법 검사기!',
  ogImage: '/favicon.png',
  robots: {
    all: true
  }
})

function chunkArray<T>(array: T[], size: number) {
  const chunked_arr = [];
  for (let i = 0; i < array.length; i += size) {
    const chunk = array.slice(i, i + size);
    chunked_arr.push(chunk);
  }
  return chunked_arr;
}

const submit = async () => {
  await auth.getUserMeta()
  if(!auth.authenticated) return;

  phrases.value = []
  correction.value = []

  try {
    loading.value = LOADING.PHRASED
    const data: { pharse: string[]} = await $fetch(`${config.public.backendUrl}/correction/phrases`, {
      method: 'POST',
      credentials: 'include',
      body: JSON.stringify({'content': content.value.replaceAll("\n", " ")}),
    })

    loading.value = LOADING.PHRASE_DONE
    const chunks = chunkArray(data.pharse, 16);

    const data1: string[][] = []

    for (const chunk of chunks) {
      const response: { content: string[] } = await $fetch(`${config.public.backendUrl}/correction/correction`, {
        method: 'POST',
        credentials: 'include',
        body: JSON.stringify({'content': chunk}),
      });
      data1.push(response.content)
    }


    phrases.value = data.pharse.map(s => s.trim())
    correction.value = data1.flat().map(s => s.trim())
    result.value = correction.value
  } catch(e) {
    loading.value = LOADING.ERROR
    throw e
  } finally {
    loading.value = LOADING.DONE
  }
}

const updateResult = (idx: number, value: string) => {
  result.value[idx] = value
}

const showResult = () => {
  content.value = result.value.join(" ")
  loading.value = LOADING.RESULT
}

const modalResult = (idx: number, origin: string, fixed: string) => {
  postLoading.value = LOADING.DEFAULT
  postModal.value = true
  originText.value = origin
  fixedText.value = fixed
}

const postResult = async () => {
  postLoading.value = LOADING.LOADING
  try {
    const { token } = await executeRecaptcha('proposeRule')
    if(!token) {
      postLoading.value = LOADING.ERROR
      return
    }

    const data: { id: number } = await $fetch(`${config.public.backendUrl}/dataset/create`, {
        method: 'POST',
        credentials: 'include',
        body: JSON.stringify({
          text: originText.value,
          correction: fixedText.value,
          memo: memo.value,
          recaptcha_response: token
        }),
      })

    postLoading.value = LOADING.DONE
    setTimeout(() => { postModal.value = false }, 3000)
  } catch(e) {
    postLoading.value = LOADING.ERROR
  }
}

const reset = () => {
  content.value = ""
  phrases.value = []
  correction.value = []
  result.value = []
  loading.value = LOADING.DEFAULT
}
</script>

<template>
  <form class="box" @submit.prevent="submit" @reset="reset">
    <h1 class="title">맞춤법 검사기</h1>
    <div class="field">
      <label class="label">검사 내용</label>
      <div class="control">
        <textarea class="input" id="content" style="height: 30em;" v-model="content"
          v-bind:disabled="!auth.authenticated || loading != LOADING.DEFAULT && loading != LOADING.RESULT"
          v-bind:placeholder="!auth.authenticated ? '로그인 후 작성할 수 있습니다.' : '교정할 내용을 작성해주세요.'"
        ></textarea>
      </div>
    </div>
    <input type="submit" class="button is-primary" value="검사하기" v-bind:disabled="!auth.authenticated || loading != LOADING.DEFAULT && loading != LOADING.RESULT" />
    <span>&nbsp; </span>
    <button type="button" class="button is-success" v-bind:disabled="!auth.authenticated || loading != LOADING.DONE  && loading != LOADING.RESULT" @click="showResult()">결과보기</button>
    <span>&nbsp; </span>
    <input type="reset" class="button is-delete" value="리셋" v-bind:disabled="!auth.authenticated || loading != LOADING.DONE && loading != LOADING.RESULT" />
    <hr>
    <progress class="progress is-primary" v-if="loading == LOADING.DONE" style="margin-top: 20px;" value="100" max="100"/>
    <progress class="progress is-primary" v-else-if="loading != LOADING.DEFAULT && loading != LOADING.RESULT" style="margin-top: 20px;"/>
    <span v-if="loading == LOADING.PHRASED">문장 분석중입니다.</span>
    <span v-else-if="loading == LOADING.PHRASE_DONE">문장 분석 작업이 끝났습니다. 문장 교정까지 최대 5분 소요됩니다.</span>
    <span v-else-if="loading == LOADING.DONE">분석이 완료되었습니다.</span>
    <span v-else-if="loading == LOADING.ERROR">분석 중 오류가 발생했습니다.</span>
    <span v-else-if="loading == LOADING.RESULT">맞춤법 검사가 완료되었습니다.</span>
    <span v-else>검사할 문장을 입력해주세요!</span>
  </form>

  <CorrectedDiff v-for="(item, idx) in phrases"
      v-bind:origin="phrases[idx]" v-bind:updated="correction[idx]" v-bind:key="`diff-${idx}`" id="diff"
      v-bind:nth="idx" v-bind:is-last-element="idx == phrases.length - 1"
      @update="updateResult" @post="modalResult"
  />

  <div class="modal" v-bind:class="postModal ? 'is-active' : ''">
    <div class="modal-background"></div>
    <form class="modal-card" @submit.prevent="postResult">
      <div class="modal-card-head">
        <p class="modal-card-title">규칙 제안하기</p>
        <button class="delete" type="button" aria-label="close" @click="postModal = false"></button>
      </div>
      <section class="modal-card-body">
        <p class="title">제안할 내용을 확인해주세요!</p>
        <table class="table is-fullwidth is-striped">
          <thead>
            <tr>
              <th style="width: 4em;">구분</th>
              <th>내용</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>원본</td>
              <td>{{ originText }}</td>
            </tr>
            <tr>
              <td>수정</td>
              <td>{{ fixedText }}</td>
            </tr>
            <tr>
              <td>메모</td>
              <td><input class="input" type="text" v-model="memo" maxlength="250"></td>
            </tr>
          </tbody>
        </table>
        <div class="notification is-success" v-if="postLoading == LOADING.DONE">
          규칙 제공에 성공했습니다.
        </div>
        <div class="notification is-warning" v-else-if="postLoading == LOADING.ERROR">
          규칙 제공에 실패했습니다.
        </div>
      </section>
      <footer class="modal-card-foot">
        <div class="buttons">
          <button class="button is-success" type="submit" :disabled="postLoading == LOADING.LOADING">제안하기</button>
          <button class="button" @click="postModal=false" type="button" :disabled="postLoading == LOADING.LOADING">취소</button>
        </div>
      </footer>
    </form>
  </div>

</template>

<style scoped>
  #content {
    scroll-margin-top: 20vh;
  }
</style>
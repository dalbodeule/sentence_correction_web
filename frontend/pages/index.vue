<script setup lang="ts">
import {useAuthStore} from "~/stores/auth";
import type {Ref} from "vue";

enum LOADING {
  DEFAULT = 0,
  PHRASED = 1,
  PHRASE_DONE = 2,
  DONE = 3,
  RESULT = 4,
  ERROR = 9,
}

const content = ref("")
const loading = ref(LOADING.DEFAULT)

const phrases: Ref<string[]> = ref([])
const correction: Ref<string[]> = ref([])
const result: Ref<string[]> = ref([])
const auth = useAuthStore()
const config = useRuntimeConfig()

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
    <button type="button" class="button is-success" v-bind:disabled="!auth.authenticated || loading != LOADING.DONE" @click="showResult()">결과보기</button>
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
      @update="updateResult"
  />

</template>

<style scoped>
  #content {
    scroll-margin-top: 20vh;
  }
</style>
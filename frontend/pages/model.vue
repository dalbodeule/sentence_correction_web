<script setup lang="ts">
useHead({
  title: '맞춤법 검사기 :: AI 모델',
  meta: [
    { name: 'description', content: '맞춤법 검사기 - 사용중인 AI 모델 설명입니다.'}
  ],
  htmlAttrs: {
    lang: 'ko'
  }
})
useSeoMeta({
  ogTitle: '맞춤법 검사기 :: AI 모델',
  ogType: 'website',
  ogSiteName: '맞춤법 검사기',
  ogDescription: '맞춤법 검사기 - 사용중인 AI 모델 설명입니다.',
  ogImage: '/favicon.png',
})
</script>

<template>
  <div class="box">
    <div class="content">
      <h1>사용 AI 모델</h1>
      <p>맞춤법 검사기는 <a href="https://github.com/SKT-AI/KoBART" target="_blank">SKT-AI의 KoBART</a>를 파인튜닝한 모델입니다.<br />
      SKT-AI에서 Modified MIT License로 학습 모델을 제공하고 있습니다.</p>

      <h3>Modified MIT License</h3>
      <p>Software Copyright (c) 2020 SK telecom</p>

      <p>Permission is hereby granted, free of charge, to any person obtaining a copy of this software and<br />
      associated documentation files (the "Software"), to deal in the Software without restriction,<br />
      including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,<br />
      and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so,<br />
      subject to the following conditions:</p>
      <br>
      <p>The above copyright notice and this permission notice shall be included<br />
      in all copies or substantial portions of the Software.<br />
      The above copyright notice and this permission notice need not be included<br />
      with content created by the Software.</p>
      <br>
      <p>THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,<br />
      INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,<br />
      FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS<br />
      BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,<br />
      TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE<br />
      OR OTHER DEALINGS IN THE SOFTWARE.</p>
    </div>
  </div>
</template>

<style scoped>

</style>
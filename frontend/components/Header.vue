<script setup lang="ts">
import { useAuthStore, UserRole } from "~/stores/auth";

const show = ref(false)

const auth = useAuthStore()
</script>

<template>
  <nav class="navbar" role="navigation" aria-label="main navigation">
    <div class="navbar-brand">
      <NuxtLink class="navbar-item" to="/">
        <img src="~/public/favicon.png" alt="맞춤법 검사기"/>&nbsp; 맞춤법 검사기
      </NuxtLink>
    </div>
    <a role="button" class="navbar-burger" aria-label="menu" aria-expanded="false" @click="show = !show">
      <span aria-hidden="true"></span>
      <span aria-hidden="true"></span>
      <span aria-hidden="true"></span>
      <span aria-hidden="true"></span>
    </a>
    <div class="navbar-menu" v-bind:class="show ? 'is-active' : ''">
      <div class="navbar-start">
        <NuxtLink class="navbar-item" to="/model">AI 모델</NuxtLink>
        <NuxtLink class="navbar-item" to="/privacy">개인정보 처리방침</NuxtLink>
      </div>
      <div class="navbar-end" v-if="auth.authenticated">
        <div class="navbar-item">
          <img v-bind:src="auth.userInfo.profile" alt="user profile"/>
          <span>&nbsp; {{ auth.userInfo.name }}</span>
        </div>
        <NuxtLink class="navbar-item" to="/modrate"
          v-if="auth.userInfo.role == UserRole.ADMIN || auth.userInfo.role == UserRole.MODERATOR">관리자 페이지</NuxtLink>
        <NuxtLink class="navbar-item" to="/logout">로그아웃</NuxtLink>
      </div>
      <div class="navbar-end" v-else>
        <NuxtLink class="navbar-item" to="/login">로그인</NuxtLink>
      </div>
    </div>
  </nav>
</template>

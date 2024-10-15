<template>
  <div class="unauthorized-container">
    <h1 class="title">未授权访问</h1>
    <p class="message">您没有权限访问此页面。</p>
    <t-button class="back-button" @click="$router.push('/login')"
      >返回登录</t-button
    >
  </div>
</template>

<script setup lang="ts"></script>

<style scoped>
.unauthorized-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background-color: #f5f5f5;
  text-align: center;
}

.title {
  font-size: 2rem;
  color: #ff4d4f;
  margin-bottom: 20px;
}

.message {
  font-size: 1.2rem;
  color: #555;
  margin-bottom: 30px;
}

.back-button {
  background-color: #4caf50;
  color: white;
  font-size: 1rem;
}
</style>

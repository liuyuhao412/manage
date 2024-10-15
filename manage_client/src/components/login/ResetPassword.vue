<template>
  <div class="content">
    <div class="reset-password">
      <h1 class="title">修改密码</h1>
      <ForgotAccount />
    </div>
  </div>
</template>

<script setup lang="ts">
import ForgotAccount from "./ForgotAccount.vue";
</script>

<style scoped>
.content {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}
.reset-password {
  margin-top: 100px;
  background-color: #ffffff; /* 修改背景颜色为白色 */
  padding: 50px; /* 增加内边距 */
  border-radius: 15px; /* 增加圆角 */
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.2); /* 增加阴影效果 */
}

.title {
  font-size: 2.8rem; /* 增大字体大小 */
  color: #00796b; /* 修改字体颜色 */
  margin-bottom: 40px; /* 增加下边距 */
  text-align: center;
  font-weight: bold; /* 加粗字体 */
  text-transform: uppercase; /* 字体大写 */
}
</style>

<template>
  <div class="login-wrapper">
    <div class="login-container">
      <div>
        <h1 class="title">
          {{
            type === "login"
              ? "登录"
              : type === "register"
              ? "注册"
              : "找回密码"
          }}
        </h1>
        <div>
          <p class="tip">
            {{ type === "login" ? "没有账号吗？" : "已有账号？" }}
          </p>
          <p
            v-if="type === 'login'"
            class="tip switch"
            @click="switchType('register')"
          >
            注册新账号 | 忘记密码？
          </p>
          <p
            v-if="type === 'register' || type === 'forgot'"
            class="tip switch"
            @click="switchType('login')"
          >
            返回登陆
          </p>
        </div>
      </div>
      <login v-if="type === 'login'" />
      <register
        v-else-if="type === 'register'"
        @register-success="switchType('login')"
      />
      <forgot-account
        v-if="type === 'forgot'"
        @recover-success="switchType('login')"
      />
    </div>
  </div>
</template>
<script setup lang="ts">
import { ref } from "vue";
import Login from "@/components/login/Login.vue";
import Register from "@/components/login/Register.vue";
import ForgotAccount from "@/components/login/ForgotAccount.vue";

const type = ref("login");

const switchType = (val: string) => {
  type.value = val;
};
</script>

<style scoped>
.login-wrapper {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-image: url("@/assets/images/login-bg.jpeg");
  background-color: white;
  background-size: cover;
  background-position: center;
  position: relative;
}

.login-container {
  width: 400px;
  background-color: rgba(255, 255, 255, 0.9);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  border-radius: 10px;
  padding: 30px;
  text-align: center;
}

.title {
  color: #333333;
  margin-top: 10px;
}

.tip {
  display: inline-block;
  margin-right: 2px;
  font: 14px Arial, sans-serif;
}
.tip {
  color: #6252be;
  cursor: pointer;
}

.tip:first-child {
  color: #777;
}
</style>

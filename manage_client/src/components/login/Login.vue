<template>
  <t-form
    ref="form"
    :data="LoginForm"
    :class="['item-container']"
    label-width="0"
  >
    <t-form-item name="account">
      <t-input
        v-model="LoginForm.account"
        size="large"
        placeholder="请输入账号"
      >
        <template #prefix-icon>
          <t-icon name="user" />
        </template>
      </t-input>
    </t-form-item>

    <t-form-item name="password">
      <t-input
        v-model="LoginForm.password"
        size="large"
        type="password"
        clearable
        autocomplete="current-password"
        placeholder="请输入密码"
      >
        <template #prefix-icon>
          <t-icon name="lock-on" />
        </template>
      </t-input>
    </t-form-item>

    <div class="check-container remember-pwd">
      <t-checkbox v-model="LoginForm.remember">记住账号</t-checkbox>
    </div>

    <t-form-item>
      <t-button block size="large" type="submit" @click="handleLogin"
        >登录</t-button
      >
    </t-form-item>
  </t-form>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { login } from "@/api/login";
import { ElMessage } from "element-plus";
import { useStore } from "vuex";
import { fetchUserRole } from "@/api/login";

const router = useRouter();
const store = useStore();

interface LoginFormType {
  account: string;
  password: string;
  remember: boolean;
}

const LoginForm = ref<LoginFormType>({
  account: localStorage.getItem("remember") || "",
  password: "",
  remember: false,
});
const form = ref();

const validateLoginForm = () => {
  const account = LoginForm.value.account.trim();
  const password = LoginForm.value.password.trim();

  if (!account) {
    ElMessage.error("账号不能为空");
    return false;
  } else if (!/^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/.test(account)) {
    ElMessage.error("请输入有效的邮箱地址");
    return false;
  }

  if (!password) {
    ElMessage.error("密码不能为空");
    return false;
  } else if (password.length < 6) {
    ElMessage.error("密码长度应至少为6个字符");
    return false;
  } else if (!/^(?=.*[a-zA-Z])(?=.*\d).+$/.test(password)) {
    ElMessage.error("密码应由数字和字母组成");
    return false;
  }

  return true;
};

onMounted(() => {
  if (localStorage.getItem("remember")) {
    LoginForm.value.account = localStorage.getItem("remember")!;
  }
});

const handleLogin = async () => {
  try {
    if (!validateLoginForm()) return;

    if (LoginForm.value.remember) {
      localStorage.setItem("remember", LoginForm.value.account);
    } else {
      localStorage.removeItem("remember");
    }

    const response = await login(
      LoginForm.value.account,
      LoginForm.value.password
    );

    if (response.data.token) {
      localStorage.setItem("token", response.data.token);
      store.commit("setToken", response.data.token);
      const roleResponse = await fetchUserRole(response.data.token);
      store.commit("setUserRole", roleResponse.data.role);

      ElMessage({
        message: response.data.message,
        type: "success",
        duration: 1000,
      });
      setTimeout(() => {
        router.push("/index");
      }, 1000);
    }
  } catch (error: any) {
    if (error.response) {
      ElMessage.error(error.response.data.message || "登录失败，请重新尝试");
    } else {
      ElMessage.error("网络错误，请检查您的连接");
    }
  }
};
</script>

<style scoped>
.item-container {
  width: 340px;
  margin-top: 20px;
}

.check-container {
  display: flex;
  align-items: center;
}

.remember-pwd {
  margin-bottom: 20px;
  justify-content: space-between;
}

.error-message {
  color: red; /* 错误信息的颜色 */
  margin-top: 10px; /* 上边距 */
}
</style>

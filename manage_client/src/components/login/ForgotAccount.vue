<template>
  <div class="forgot-account-container">
    <t-form ref="form" :data="ForgetForm" label-width="0">
      <t-form-item name="email">
        <t-input
          v-model="ForgetForm.email"
          size="large"
          placeholder="请输入邮箱"
        >
          <template #prefix-icon>
            <t-icon name="user" />
          </template>
        </t-input>
      </t-form-item>
      <t-form-item class="verification-code" name="verificationCode">
        <t-input
          v-model="ForgetForm.verificationCode"
          size="large"
          placeholder="请输入验证码"
        >
        </t-input>
        <t-button
          variant="outline"
          size="large"
          @click="handleVerificationCode"
          :disabled="isCountingDown"
        >
          {{ isCountingDown ? countdown + "秒" : "发送验证码" }}
        </t-button>
      </t-form-item>
      <t-form-item name="newPassword">
        <t-input
          v-model="ForgetForm.newPassword"
          size="large"
          type="password"
          placeholder="请输入新密码"
        >
          <template #prefix-icon>
            <t-icon name="lock-on" />
          </template>
        </t-input>
      </t-form-item>
      <t-form-item>
        <t-button block size="large" type="submit" @click="handleRecoverAccount"
          >确认</t-button
        >
      </t-form-item>
    </t-form>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { ElMessage } from "element-plus";
import {
  sendVerificationCode,
  recoverAccount,
  checkEmailRegistered,
} from "@/api/login";

const emit = defineEmits();

interface ForgetFormType {
  email: string;
  verificationCode: string;
  sentVerificationCode: string;
  newPassword: string;
}

const ForgetForm = ref<ForgetFormType>({
  email: "",
  verificationCode: "",
  sentVerificationCode: "",
  newPassword: "",
});

const isCountingDown = ref(false);
const countdown = ref(60);

const handleVerificationCode = async () => {
  const email = ForgetForm.value.email.trim();
  if (!email) {
    ElMessage.error("邮箱不能为空");
    return;
  } else if (!/^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/.test(email)) {
    ElMessage.error("请输入有效的邮箱地址");
    return;
  }

  const response = await checkEmailRegistered(email);
  if (!response.data.registered) {
    ElMessage.error("该邮箱未注册");
    return;
  }

  try {
    const sendResponse = await sendVerificationCode(email);
    ElMessage({
      message: sendResponse.data.message,
      type: "success",
      duration: 1000,
    });
    ForgetForm.value.sentVerificationCode = sendResponse.data.verification_code;
    alert(sendResponse.data.verification_code);
    // 开始倒计时
    isCountingDown.value = true;
    countdown.value = 60;
    const timer = setInterval(() => {
      countdown.value--;
      if (countdown.value <= 0) {
        clearInterval(timer);
        isCountingDown.value = false;
      }
    }, 1000);
  } catch (error: any) {
    if (error.response) {
      ElMessage.error(error.response.data.message || "验证码发送失败，请重试");
    } else {
      ElMessage.error("验证码发送失败，请检查您的网络连接");
    }
  }
};

const validateRecoverForm = () => {
  const { email, verificationCode, sentVerificationCode, newPassword } =
    ForgetForm.value;

  if (!email) {
    ElMessage.error("邮箱不能为空");
    return false;
  } else if (!/^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/.test(email)) {
    ElMessage.error("请输入有效的邮箱地址");
    return false;
  }

  if (!verificationCode) {
    ElMessage.error("验证码不能为空");
    return false;
  }

  if (verificationCode !== sentVerificationCode) {
    ElMessage.error("验证码不正确");
    return false;
  }

  if (!newPassword) {
    ElMessage.error("新密码不能为空");
    return false;
  } else if (newPassword.length < 6) {
    ElMessage.error("新密码长度应至少为6个字符");
    return false;
  } else if (!/^(?=.*[a-zA-Z])(?=.*\d).+$/.test(newPassword)) {
    ElMessage.error("新密码应由数字和字母组成");
    return false;
  }

  return true;
};

// 找回账号处理函数
const handleRecoverAccount = async () => {
  const { email, verificationCode, newPassword } = ForgetForm.value;

  if (!email || !verificationCode || !newPassword) {
    ElMessage.error("请填写所有字段");
    return;
  }

  if (!validateRecoverForm()) return;

  try {
    const response = await recoverAccount(ForgetForm.value);
    ElMessage({
      message: response.data.message,
      type: "success",
      duration: 1000,
    });
    setTimeout(() => {
      emit("recover-success");
    }, 1000);
  } catch (error: any) {
    if (error.response) {
      ElMessage.error(error.response.data.message || "密码找回失败，请重试");
    } else {
      ElMessage.error("网络错误，请检查您的连接");
    }
  }
};
</script>

<style scoped>
.forgot-account-container {
  width: 340px;
  margin-top: 20px;
}

.verification-code {
  display: flex;
  align-items: center;
}

.verification-code button {
  flex-shrink: 0;
  margin-left: 10px;
  width: 128px;
  height: 40px;
}
</style>

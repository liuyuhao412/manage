<template>
  <t-form
    ref="form"
    :class="['item-container']"
    :data="RegisterForm"
    label-width="0"
  >
    <t-form-item name="email">
      <t-input
        v-model="RegisterForm.email"
        size="large"
        placeholder="请输入您的邮箱"
        @blur="clearVerificationCodeIfEmailRegistered"
      >
        <template #prefix-icon>
          <t-icon name="user" />
        </template>
      </t-input>
    </t-form-item>

    <t-form-item class="verification-code" name="verifyCode">
      <t-input
        v-model="RegisterForm.verifyCode"
        size="large"
        placeholder="请输入验证码"
      />
      <t-button
        variant="outline"
        size="large"
        @click="handleVerificationCode"
        :disabled="isCountingDown"
      >
        {{ isCountingDown ? countdown + "秒" : "发送验证码" }}
      </t-button>
    </t-form-item>

    <t-form-item name="password">
      <t-input
        v-model="RegisterForm.password"
        size="large"
        clearable
        placeholder="请输入登录密码"
        type="password"
      >
        <template #prefix-icon>
          <t-icon name="lock-on" />
        </template>
        <template #suffix-icon>
          <t-icon />
        </template>
      </t-input>
    </t-form-item>

    <t-form-item class="check-container" name="checked">
      <t-checkbox v-model="RegisterForm.checked">我已阅读并同意 </t-checkbox>
      <span>服务协议</span> 和
      <span>隐私声明</span>
    </t-form-item>

    <t-form-item>
      <t-button block size="large" type="submit" @click="handleRegister"
        >注册</t-button
      >
    </t-form-item>
  </t-form>
</template>

<script setup lang="ts">
import { ref } from "vue";
import {
  register,
  sendVerificationCode,
  checkEmailRegistered,
} from "@/api/login";
import { ElMessage } from "element-plus";

const emit = defineEmits();

interface RegisterFormType {
  email: string;
  password: string;
  verifyCode: string;
  sentVerificationCode: string;
  checked: boolean;
}

const RegisterForm = ref<RegisterFormType>({
  email: "",
  password: "",
  verifyCode: "",
  sentVerificationCode: "",
  checked: false,
});

const form = ref();
const isCountingDown = ref(false);
const countdown = ref(60);

const clearVerificationCodeIfEmailRegistered = async () => {
  const email = RegisterForm.value.email.trim();
  if (email) {
    const response = await checkEmailRegistered(email);
    if (response.data.registered) {
      RegisterForm.value.verifyCode = "";
      RegisterForm.value.sentVerificationCode = "";
    }
  }
};

const handleVerificationCode = async () => {
  const email = RegisterForm.value.email.trim();

  if (!email) {
    ElMessage.error("邮箱不能为空");
    return;
  } else if (!/^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/.test(email)) {
    ElMessage.error("请输入有效的邮箱地址");
    return;
  }

  const response = await checkEmailRegistered(email);
  if (response.data.registered) {
    ElMessage.error("该邮箱已注册，无法进行注册");
    return;
  }

  try {
    const sendResponse = await sendVerificationCode(email);
    ElMessage({
      message: sendResponse.data.message,
      type: "success",
      duration: 1000,
    });
    RegisterForm.value.sentVerificationCode =
      sendResponse.data.verification_code;
    alert(sendResponse.data.verification_code);
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
      ElMessage.error(error.response.data.message || "验证码发送失败，请重新尝试");
    } else {
      ElMessage.error("发送验证码失败，请检查您的网络连接");
    }
  }
};

const validateRegisterForm = () => {
  const { email, password, verifyCode, sentVerificationCode } =
    RegisterForm.value;

  if (!email) {
    ElMessage.error("邮箱不能为空");
    return false;
  } else if (!/^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/.test(email)) {
    ElMessage.error("请输入有效的邮箱地址");
    return false;
  }
  if (!verifyCode) {
    ElMessage.error("验证码不能为空");
    return false;
  }

  if (verifyCode !== sentVerificationCode) {
    ElMessage.error("验证码不正确");
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

const handleRegister = async () => {
  if (!RegisterForm.value.checked) {
    ElMessage.error("请同意服务协议和隐私声明");
    return;
  }

  if (!validateRegisterForm()) return;

  try {
    const response = await register(RegisterForm.value);
    ElMessage({
      message: response.data.message,
      type: "success",
      duration: 1000,
    });
    setTimeout(() => {
      emit("register-success"); 
    }, 1000);
  } catch (error: any) {
    if (error.response) {
      ElMessage.error(error.response.data.message || "账号注册失败，请重试");
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

.check-container {
  display: flex;
  align-items: center;
}

.check-container .tip {
  color: #6252be;
}

.check-container span {
  color: #6252be;
}
</style>

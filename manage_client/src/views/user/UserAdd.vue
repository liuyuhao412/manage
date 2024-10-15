<template>
  <div>
    <t-breadcrumb>
      <t-breadcrumb-item to="/index">首页</t-breadcrumb-item>
      <t-breadcrumb-item to="/index/users">用户列表</t-breadcrumb-item>
      <t-breadcrumb-item>{{
        isEdit ? "编辑用户" : "添加用户"
      }}</t-breadcrumb-item>
    </t-breadcrumb>
    <t-card class="user-detail-card" bordered>
      <t-form :model="userForm" :rules="rules" ref="userFormRef">
        <t-form-item label="用户名" prop="username">
          <t-input
            class="input-short"
            v-model="userForm.username"
            placeholder="请输入用户名（邮箱格式）"
            clearable
          />
        </t-form-item>
        <t-form-item label="姓名" prop="name">
          <t-input
            class="input-short"
            v-model="userForm.name"
            placeholder="请输入姓名"
            clearable
          />
        </t-form-item>
        <t-form-item label="性别" prop="gender">
          <t-radio-group v-model="userForm.gender" :options="genderOptions" />
        </t-form-item>
        <t-form-item label="出生日期" prop="birthday">
          <t-date-picker v-model="userForm.birthday" placeholder="请选择生日" />
        </t-form-item>
        <t-form-item label="角色" prop="role">
          <t-select
            v-model="userForm.role"
            :options="roleOptions"
            placeholder="请选择角色"
            class="role-select"
            clearable
          />
        </t-form-item>
        <div class="button-container">
          <t-button
            type="primary"
            class="submit-button"
            @click="submitForm"
            size="large"
          >
            {{ isEdit ? "保存" : "添加" }}
          </t-button>
          <t-button @click="goBack" size="large" class="back-button"
            >返回</t-button
          >
        </div>
      </t-form>
    </t-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { ElMessage } from "element-plus";
import { addUser, fetchUserById, updateUserInfo } from "@/api/user";
import { checkEmailRegistered } from "@/api/login";

const router = useRouter();
const route = useRoute();
const isEdit = route.name === "UserEdit"; // 判断是否为编辑模式
const userId = Number(route.params.id);

const userForm = ref({
  username: "",
  name: "",
  gender: "",
  birthday: "",
  role: "USER",
});

const rules = {
  username: [{ required: true, message: "请输入用户名（邮箱格式）" }],
  name: [{ required: false, message: "请输入姓名" }],
  gender: [{ required: false, message: "请选择性别" }],
  birthday: [{ required: false, message: "请选择生日" }],
  role: [{ required: true, message: "请选择角色" }],
};

const genderOptions = [
  { label: "男", value: "男" },
  { label: "女", value: "女" },
];

const roleOptions = [
  { label: "管理员", value: "ADMIN" },
  { label: "经理", value: "MANAGER" },
  { label: "成员", value: "MEMBER" },
  { label: "用户", value: "USER" },
];

const fetchUserData = async (id: number) => {
  const response = await fetchUserById(id);
  userForm.value.username = response.data.username;
  userForm.value.name = response.data.name;
  userForm.value.gender = response.data.gender;
  userForm.value.birthday = response.data.birthday;
  const role = response.data.role;
  if (role === "管理员") {
    userForm.value.role = "ADMIN";
  } else if (role === "经理") {
    userForm.value.role = "MANAGER";
  } else if (role === "成员") {
    userForm.value.role = "MEMBER";
  } else if (role === "用户") {
    userForm.value.role = "USER";
  }
};
const checkEmailExists = async () => {
  const email = userForm.value.username.trim();
  if (email) {
    const response = await checkEmailRegistered(email);
    if (response.data.registered) {
      ElMessage.error("该邮箱已存在，请使用其他邮箱");
      return false;
    }
  }
  return true;
};

const submitForm = async () => {
  if (!userForm.value.username) {
    ElMessage.error("邮箱不能为空");
    return;
  } else if (
    !/^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/.test(userForm.value.username)
  ) {
    ElMessage.error("请输入有效的邮箱地址");
    return;
  }

  try {
    if (isEdit) {
      const response = await updateUserInfo(userId, userForm.value);
      ElMessage({
        message: response.data.message,
        type: "success",
        duration: 1000,
      });
      setTimeout(() => {
        router.push({ name: "UserList" });
      }, 1000);
    } else {
      // 添加用户逻辑
      // 等待检查邮箱是否存在
      const emailExists = await checkEmailExists();
      if (!emailExists) {
        return;
      }
      const response = await addUser({
        username: userForm.value.username,
        name: userForm.value.name,
        gender: userForm.value.gender,
        birthday: userForm.value.birthday,
        role: userForm.value.role,
      });
      ElMessage({
        message: response.data.message,
        type: "success",
        duration: 1000,
      });
      setTimeout(() => {
        router.push({ name: "UserList" });
      }, 1000);
    }
  } catch (error) {
    ElMessage.error("操作失败，请重试");
  }
};
const goBack = () => {
  router.push({ name: "UserList" });
};

onMounted(() => {
  if (isEdit) {
    fetchUserData(userId);
  }
});
</script>

<style scoped>
.user-detail-card {
  margin-top: 20px;
  width: 500px;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2); /* 增加阴影效果 */
  background-color: #ffffff; /* 设置背景颜色为白色 */
  border: 1px solid #e0e0e0; /* 添加边框 */
}

.input-short {
  width: 100%; /* 调整输入框宽度为100% */
  max-width: 250px; /* 最大宽度 */
}

.role-select {
  width: 100%; /* 角色选择框样式 */
  max-width: 250px; /* 最大宽度 */
}

.button-container {
  display: flex;
  justify-content: center; /* 按钮右对齐 */
  margin-top: 30px;
}

.submit-button {
  margin-right: 20px;
}
</style>

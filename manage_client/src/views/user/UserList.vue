<template>
  <div class="container">
    <t-breadcrumb>
      <t-breadcrumb-item to="/index">首页</t-breadcrumb-item>
      <t-breadcrumb-item to="/index/users">用户列表</t-breadcrumb-item>
    </t-breadcrumb>
    <t-card class="list-card-container" :bordered="false">
      <t-row justify="space-between">
        <div class="left-operation-container">
          <t-button @click="addUser">添加用户</t-button>
          <t-button
            variant="base"
            theme="default"
            :disabled="!selectedRowKeys.length"
            @click="exportUsersFile"
            >导出用户</t-button
          >
          <p v-if="selectedRowKeys.length" class="selected-count">
            已选{{ selectedRowKeys.length }}项
          </p>
        </div>
        <div class="search-input">
          <t-input v-model="searchValue" clearable @input="filterUsers">
            <template #suffix-icon>
              <search-icon size="16px" />
            </template>
          </t-input>
        </div>
      </t-row>
      <div class="table-container">
        <t-table
          :data="filtered_user_list"
          :columns="COLUMNS"
          :row-key="rowKey"
          vertical-align="top"
          :hover="true"
          :pagination="pagination"
          :selected-row-keys="selectedRowKeys"
          @page-change="rehandlePageChange"
          @select-change="(value: string[]) => rehandleSelectChange(value)"
        >
          <template #role="{ row }">
            <t-tag v-if="row.role === '管理员'" theme="danger">管理员</t-tag>
            <t-tag v-else-if="row.role === '经理'" theme="warning">
              经理
            </t-tag>
            <t-tag v-else-if="row.role === '成员'" theme="success">
              成员
            </t-tag>
            <t-tag v-else-if="row.role === '用户'" theme="primary">
              用户
            </t-tag>
          </template>

          <template #account_status="{ row }">
            <t-switch
              v-model="row.account_status"
              :options="[
                { label: '正常', value: true },
                { label: '禁用', value: false },
              ]"
              @change="(value: boolean) => handleStatusChange(row.id, value)"
            />
          </template>

          <template #op="{ row }">
            <t-space>
              <t-link theme="primary" @click="handleDetails(row.id)">
                编辑</t-link
              >
              <t-link theme="danger" @click="() => handleDelete(row.id)">
                删除</t-link
              >
            </t-space>
          </template>
        </t-table>
      </div>
    </t-card>
  </div>
</template>

<script setup lang="ts">
import { SearchIcon } from "tdesign-icons-vue-next";
import { PrimaryTableCol, TableRowData } from "tdesign-vue-next";
import { ElMessage, ElMessageBox } from "element-plus";
import { ref, onMounted } from "vue";
import type { Ref } from "vue";
import {
  fetchUsers,
  updateUserStatus,
  deleteUser,
  exportUsers,
} from "@/api/user";
import { useRouter } from "vue-router";

const router = useRouter();

const COLUMNS: PrimaryTableCol<TableRowData>[] = [
  {
    type: "multiple",
    width: 30,
    colKey: "row-select",
    fixed: "left",
  },
  {
    title: "用户名",
    align: "center",
    width: 130,
    colKey: "username",
    fixed: "left",
  },
  {
    title: "姓名",
    align: "center",
    width: 70,
    colKey: "name",
    fixed: "left",
  },
  {
    title: "性别",
    align: "center",
    width: 50,
    colKey: "gender",
    fixed: "left",
  },
  {
    title: "出生日期",
    align: "center",
    width: 100,
    colKey: "birthday",
    fixed: "left",
  },
  {
    title: "角色",
    align: "center",
    width: 80,
    colKey: "role",
    fixed: "left",
  },
  {
    title: "创建时间",
    align: "center",
    width: 120,
    colKey: "created_at",
    fixed: "left",
  },
  {
    title: "上次登录时间",
    align: "center",
    width: 120,
    colKey: "last_login_at",
    fixed: "left",
  },
  {
    title: "上次登录IP",
    align: "center",
    width: 80,
    colKey: "last_login_ip",
    fixed: "left",
  },
  {
    title: "账户状态",
    align: "center",
    width: 70,
    colKey: "account_status",
    fixed: "left",
  },
  {
    title: "操作",
    align: "center",
    fixed: "right",
    width: 120,
    colKey: "op",
  },
];
interface User {
  id: number;
  username: string;
  name: string;
  gender: string;
  birthday: string;
  role: string;
  account_status: boolean;
  created_at: string;
  last_login_at: string;
  last_login_ip: string;
}

const user_list: Ref<Array<User>> = ref([]);
const filtered_user_list: Ref<Array<User>> = ref([]);

const pagination = ref({
  defaultPageSize: 5,
  total: 0,
  defaultCurrent: 1,
});

const searchValue = ref("");

const selectedRowKeys = ref<string[]>([]);

const rowKey = "id";

const rehandlePageChange = (curr: {
  current: number;
  previous: number;
  pageSize: number;
}) => {
  console.log(
    `当前页: ${curr.current}, 上一页: ${curr.previous}, 每页大小: ${curr.pageSize}`
  );
};

const rehandleSelectChange = (val: string[]) => {
  selectedRowKeys.value = val;
};

const fetchUsersData = async () => {
  const response = await fetchUsers();
  user_list.value = response.data.users;
  filtered_user_list.value = user_list.value;
  pagination.value.total = response.data.total;
};

const filterUsers = () => {
  if (searchValue.value.trim() === "") {
    filtered_user_list.value = user_list.value;
  } else {
    filtered_user_list.value = user_list.value.filter((user) => {
      return (
        (user.username && user.username.includes(searchValue.value)) ||
        (user.name && user.name.includes(searchValue.value))
      );
    });
  }
};

const handleStatusChange = async (id: number, status: boolean) => {
  try {
    const response = await updateUserStatus(id, status);
    if (response) {
      const user = user_list.value.find((user) => user.id === id);
      if (user) {
        user.account_status = status;
      } else {
        console.warn(`未找到用户 ID: ${id}`);
      }
    }
  } catch (error) {
    console.error("更新用户状态失败:", error);
    ElMessage.error("更新用户状态失败，请重试。");
  }
};

const addUser = () => {
  router.push({ name: "UserAdd" });
};

const handleDetails = (id: number) => {
  router.push({ name: "UserEdit", params: { id } });
};

const handleDelete = async (id: number) => {
  try {
    await ElMessageBox.confirm("此操作将永久删除该用户，是否继续？", "警告", {
      confirmButtonText: "确定",
      cancelButtonText: "取消",
      type: "warning",
      center: true,
    });

    const response = await deleteUser(id);
    if (response.data.result) {
      ElMessage({
        type: "success",
        message: response.data.message,
        duration: 1000,
      });
      user_list.value = user_list.value.filter((user) => user.id !== id);
      filtered_user_list.value = filtered_user_list.value.filter(
        (user) => user.id !== id
      );
    }
  } catch (error) {
    ElMessage({
      message: "删除失败，请重试",
    });
  }
};

const exportUsersFile = async () => {
  try {
    const response = await exportUsers(selectedRowKeys.value);
    const blob = new Blob([response.data], {
      type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "用户列表.xlsx";
    document.body.appendChild(a);
    a.click();
    a.remove();
  } catch (error) {
    ElMessage.error("导出用户失败，请重试。");
  }
};

onMounted(async () => {
  fetchUsersData();
});
</script>

<style scoped>
.container {
  width: 100%;
}
.table-container {
  max-width: 100%;
}
.payment-col {
  display: flex;
}

.trend-container {
  display: flex;
  align-items: center;
  margin-left: 10px;
}

.list-card-container {
  padding: 10px;
}

.left-operation-container {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.selected-count {
  display: inline-block;
  margin-left: 20px;
}

.search-input {
  width: 360px;
}
</style>

<template>
  <div class="container">
    <t-breadcrumb>
      <t-breadcrumb-item to="/index">首页</t-breadcrumb-item>
      <t-breadcrumb-item to="/index/tasks">任务列表</t-breadcrumb-item>
    </t-breadcrumb>
    <t-card class="list-card-container" :bordered="false">
      <t-row justify="space-between">
        <div class="left-operation-container">
          <t-button
            v-if="userRole === '管理员' || userRole === '经理'"
            @click="addTask"
            >添加任务</t-button
          >
        </div>
        <div class="search-input">
          <t-input v-model="searchValue" clearable @input="filterTasks">
            <template #suffix-icon>
              <search-icon size="16px" />
            </template>
          </t-input>
        </div>
      </t-row>
      <t-table
        :data="filtered_task_list"
        :columns="taskColumns"
        :row-key="rowKey"
        vertical-align="top"
        :hover="true"
        :pagination="pagination"
        :selected-row-keys="selectedRowKeys"
        @page-change="rehandlePageChange"
        @select-change="(value: string[]) => rehandleSelectChange(value)"
      >
        <template #status="{ row }">
          <t-tag v-if="row.status === '进行中'" theme="warning">进行中</t-tag>
          <t-tag v-else-if="row.status === '已完成'" theme="success"
            >已完成</t-tag
          >
        </template>

        <template
          #op="{ row }"
          v-if="userRole === '管理员' || userRole === '经理'"
        >
          <t-space>
            <t-link theme="primary" @click="handleEdit(row.id)">编辑</t-link>
            <t-link theme="warning" @click="handleDetail(row.id)"
              >查看详情</t-link
            >
            <t-link theme="danger" @click="handleDelete(row.id)">删除</t-link>
          </t-space>
        </template>
        <template #op="{ row }" v-else>
          <t-space>
            <t-link theme="primary" @click="handleDetail(row.id)"
              >查看详情</t-link
            >
          </t-space>
        </template>
      </t-table>
    </t-card>
  </div>
</template>

<script setup lang="ts">
import { SearchIcon } from "tdesign-icons-vue-next";
import { ref, onMounted, computed } from "vue";
import { fetchTasks, deleteTask, fetchMemberTasks } from "@/api/tasks";
import { useRouter } from "vue-router";
import { ElMessage, ElMessageBox } from "element-plus";
import { useStore } from "vuex";

const router = useRouter();
const store = useStore();
const userRole = computed(() => store.getters.getUserRole);

interface Task {
  id: number;
  title: string;
  project_name: string;
  assignee_name: string;
  project_manager_name: string;
  status: string;
  due_date: string;
}

const taskList = ref<Array<Task>>([]);
const filtered_task_list = ref<Array<Task>>([]);

const taskColumns = [
  {
    title: "项目ID",
    colKey: "id",
    width: 80,
    align: "center",
    fixed: "left",
  },
  {
    title: "任务名称",
    colKey: "title",
    width: 120,
    align: "center",
    fixed: "left",
  },
  {
    title: "项目名称",
    colKey: "project_name",
    width: 120,
    align: "center",
    fixed: "left",
  },
  {
    title: "任务指派人",
    colKey: "assignee_name",
    width: 120,
    align: "center",
    fixed: "left",
  },
  {
    title: "项目负责人",
    colKey: "project_manager_name",
    width: 120,
    align: "center",
    fixed: "left",
  },
  {
    title: "状态",
    colKey: "status",
    width: 120,
    align: "center",
    fixed: "left",
  },
  {
    title: "截止时间",
    colKey: "due_date",
    width: 140,
    align: "center",
    fixed: "left",
  },
  { title: "操作", align: "center", width: 130, colKey: "op", fixed: "right" },
];

const rowKey = "id";

const pagination = ref({ defaultPageSize: 5, total: 0, defaultCurrent: 1 });

const searchValue = ref("");
const selectedRowKeys = ref<string[]>([]);

const rehandlePageChange = (curr: {
  current: number;
  previous: number;
  pageSize: number;
}) => {
  console.log(
    `当前页: ${curr.current}, 上一页: ${curr.previous}, 每页大小: ${curr.pageSize}`
  );
};

const filterTasks = () => {
  if (searchValue.value.trim() === "") {
    filtered_task_list.value = taskList.value;
  } else {
    filtered_task_list.value = taskList.value.filter((task) => {
      return task.title && task.title.includes(searchValue.value);
    });
  }
};

const rehandleSelectChange = (val: string[]) => {
  selectedRowKeys.value = val;
};

const fetchTasksData = async () => {
  const response = await fetchTasks();
  taskList.value = response.data.tasks;
  filtered_task_list.value = taskList.value;
  pagination.value.total = response.data.total;
};

const fetchMemberTasksData = async () => {
  const response = await fetchMemberTasks();
  taskList.value = response.data.tasks;
  filtered_task_list.value = taskList.value;
  pagination.value.total = response.data.total;
};

const addTask = () => {
  router.push({ name: "TaskAdd" });
};

const handleEdit = (id: number) => {
  router.push({ name: "TaskEdit", params: { id } });
};

const handleDelete = async (id: number) => {
  try {
    await ElMessageBox.confirm("此操作将永久删除该项目，是否继续？", "警告", {
      confirmButtonText: "确定",
      cancelButtonText: "取消",
      type: "warning",
      center: true,
    });
    try {
      const response = await deleteTask(id);
      if (response.data.result) {
        ElMessage({
          type: "success",
          message: response.data.message,
          duration: 1000,
        });
        taskList.value = taskList.value.filter((task) => task.id !== id);
        filtered_task_list.value = filtered_task_list.value.filter(
          (task) => task.id !== id
        );
      }
    } catch (error: any) {
      console.log(error);
      ElMessage.error(error.response?.data?.error || "任务删除失败，请重试");
    }
  } catch (error) {
    ElMessage({ message: "删除失败，请重试" });
  }
};

const handleDetail = (id: number) => {
  router.push({ name: "TaskDetail", params: { id } });
};

onMounted(() => {
  if (userRole.value === "管理员" || userRole.value === "经理") {
    fetchTasksData();
  } else {
    fetchMemberTasksData();
  }
});
</script>

<style scoped>
.container {
  width: 100%;
}
</style>

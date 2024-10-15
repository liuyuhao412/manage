<template>
  <div>
    <t-breadcrumb>
      <t-breadcrumb-item to="/index">首页</t-breadcrumb-item>
      <t-breadcrumb-item to="/index/tasks">任务列表</t-breadcrumb-item>
      <t-breadcrumb-item>{{
        isEdit ? "编辑任务" : "添加任务"
      }}</t-breadcrumb-item>
    </t-breadcrumb>
    <t-card class="detail-card" bordered>
      <t-form :model="taskForm" ref="taskFormRef">
        <t-form-item label="任务名称" prop="title">
          <t-input
            v-model="taskForm.title"
            placeholder="请输入任务名称"
            clearable
          />
        </t-form-item>
        <t-form-item label="描述" prop="description">
          <t-textarea
            v-model="taskForm.description"
            placeholder="请输入任务描述"
            clearable
            rows="4"
          />
        </t-form-item>
        <t-form-item label="截止时间" prop="due_date">
          <t-date-picker
            v-model="taskForm.due_date"
            placeholder="请选择截止时间"
            enable-time-picker
            allow-input
            clearable
          />
        </t-form-item>
        <t-form-item label="指派人" prop="assignee_id">
          <t-select
            v-model="taskForm.assignee_id"
            :options="assigneeOptions"
            placeholder="请选择指派人"
          />
        </t-form-item>
        <t-form-item label="项目" prop="project_id">
          <t-select
            v-model="taskForm.project_id"
            :options="projectOptions"
            placeholder="请选择项目"
          />
        </t-form-item>
        <t-form-item label="状态" prop="status">
          <t-select
            v-model="taskForm.status"
            :options="statusOptions"
            placeholder="请选择状态"
            class="select-field"
          />
        </t-form-item>

        <div class="button-container">
          <t-button
            type="primary"
            size="large"
            class="submit-button"
            @click="submitForm"
            >{{ isEdit ? "保存" : "添加" }}</t-button
          >
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
import { createTask, updateTask, fetchTaskById } from "@/api/tasks";
import { fetchMembers } from "@/api/user";
import { fetchProjects } from "@/api/projects";

const route = useRoute();
const router = useRouter();
const isEdit = route.name === "TaskEdit";
const taskId = Number(route.params.id);

interface TaskForm {
  title: string;
  description: string;
  due_date: string;
  assignee_id: number | null;
  project_id: number | null;
  status: string;
}

const taskForm = ref<TaskForm>({
  title: "",
  description: "",
  due_date: "",
  assignee_id: null,
  project_id: null,
  status: "IN_PROGRESS",
});

const statusOptions = [
  { label: "进行中", value: "IN_PROGRESS" },
  { label: "已完成", value: "COMPLETED" },
];

const assigneeOptions = ref([]);
const projectOptions = ref([]);

const fetchAssignees = async () => {
  try {
    const response = await fetchMembers();
    assigneeOptions.value = response.data.members.map((member: any) => ({
      label: member.name,
      value: member.id,
    }));
  } catch (error) {
    ElMessage.error("获取成员失败，请重试");
  }
};

const fetchProjectsData = async () => {
  const response = await fetchProjects();
  projectOptions.value = response.data.projects.map((project: any) => ({
    label: project.name,
    value: project.id,
  }));
};

const fetchTaskData = async (id: number) => {
  const response = await fetchTaskById(id);
  taskForm.value.title = response.data.title;
  taskForm.value.description = response.data.description;
  taskForm.value.due_date = response.data.due_date;
  taskForm.value.assignee_id = response.data.assignee_id;
  taskForm.value.project_id = response.data.project_id;
  if (response.data.status === "进行中") {
    taskForm.value.status = "IN_PROGRESS";
  } else if (response.data.status === "已完成") {
    taskForm.value.status = "COMPLETED";
  }
};

const submitForm = async () => {
  if (!taskForm.value.title) {
    ElMessage.error("任务名称不能为空");
    return;
  }
  if (!taskForm.value.due_date) {
    ElMessage.error("截止时间不能为空");
    return;
  }
  if (taskForm.value.project_id === null) {
    ElMessage.error("请先选择项目");
    return;
  }

  if (isEdit) {
    try {
      const response = await updateTask(taskId, taskForm.value);
      ElMessage({
        message: response.data.message,
        type: "success",
        duration: 1000,
      });
      setTimeout(() => {
        router.push({ name: "TaskList" });
      }, 1000);
    } catch (error: any) {
      ElMessage.error(error.response?.data?.error || "任务更新失败，请重试");
    }
  } else {
    try {
      const response = await createTask(taskForm.value);
      ElMessage({
        message: response.data.message,
        type: "success",
        duration: 1000,
      });
      setTimeout(() => {
        router.push({ name: "TaskList" });
      }, 1000);
    } catch (error: any) {
      ElMessage.error(error.response?.data?.error || "任务创建失败，请重试");
    }
  }
};
const goBack = () => {
  router.push({ name: "TaskList" });
};

onMounted(() => {
  fetchAssignees();
  fetchProjectsData();
  if (isEdit) {
    fetchTaskData(taskId);
  }
});
</script>

<style scoped>
.button-container {
  margin-top: 20px;
}
.detail-card {
  margin-top: 20px;
  width: 500px;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2); /* 增加阴影效果 */
  background-color: #ffffff; /* 设置背景颜色为白色 */
  border: 1px solid #e0e0e0; /* 添加边框 */
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

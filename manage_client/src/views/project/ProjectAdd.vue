<template>
  <div>
    <t-breadcrumb>
      <t-breadcrumb-item to="/index">首页</t-breadcrumb-item>
      <t-breadcrumb-item to="/index/projects">项目列表</t-breadcrumb-item>
      <t-breadcrumb-item>{{
        isEdit ? "编辑项目" : "添加项目"
      }}</t-breadcrumb-item>
    </t-breadcrumb>
    <t-card class="project-detail-card" bordered>
      <t-form :model="projectForm" ref="projectFormRef">
        <t-form-item label="项目名称" prop="name">
          <t-input
            v-model="projectForm.name"
            placeholder="请输入项目名称"
            clearable
            class="input-field"
          />
        </t-form-item>
        <t-form-item label="描述" prop="description">
          <t-textarea
            v-model="projectForm.description"
            placeholder="请输入项目描述"
            clearable
            class="input-field"
            rows="4"
          />
        </t-form-item>
        <t-form-item label="开始时间" prop="start_date">
          <t-date-picker
            v-model="projectForm.start_date"
            placeholder="请选择开始时间"
            enable-time-picker
            allow-input
            clearable
            class="date-picker"
          />
        </t-form-item>
        <t-form-item label="结束时间" prop="end_date">
          <t-date-picker
            v-model="projectForm.end_date"
            placeholder="请选择结束时间"
            enable-time-picker
            allow-input
            clearable
            class="date-picker"
          />
        </t-form-item>
        <t-form-item label="状态" prop="status">
          <t-select
            v-model="projectForm.status"
            :options="statusOptions"
            placeholder="请选择状态"
            class="select-field"
          />
        </t-form-item>
        <t-form-item label="优先级" prop="priority">
          <t-select
            v-model="projectForm.priority"
            :options="priorityOptions"
            placeholder="请选择优先级"
            class="select-field"
          />
        </t-form-item>
        <div class="button-container">
          <t-button
            type="primary"
            size="large"
            @click="submitForm"
            class="submit-button"
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
import { createProject, updateProject, fetchProjectById } from "@/api/projects";

const route = useRoute();
const router = useRouter();
const isEdit = route.name === "ProjectEdit"; // 判断是否为编辑模式
const userId = Number(route.params.id);

interface ProjectForm {
  name: string;
  description: string;
  start_date: string;
  end_date: string;
  status: string;
  priority: string;
}
const projectForm = ref<ProjectForm>({
  name: "",
  description: "",
  start_date: "",
  end_date: "",
  status: "IN_PROGRESS",
  priority: "NORMAL",
});

const statusOptions = [
  { label: "进行中", value: "IN_PROGRESS" },
  { label: "已完成", value: "COMPLETED" },
  { label: "已归档", value: "ARCHIVED" },
];

const priorityOptions = [
  { label: "低", value: "LOW" },
  { label: "正常", value: "NORMAL" },
  { label: "高", value: "HIGH" },
];

const fetchProjectData = async (id: number) => {
  const response = await fetchProjectById(id);
  projectForm.value = response.data;
  if (response.data.status === "进行中") {
    projectForm.value.status = "IN_PROGRESS";
  } else if (response.data.status === "已完成") {
    projectForm.value.status = "COMPLETED";
  } else if (response.data.status === "已归档") {
    projectForm.value.status = "ARCHIVED";
  }
  if (response.data.priority === "低") {
    projectForm.value.priority = "LOW";
  } else if (response.data.priority === "正常") {
    projectForm.value.priority = "NORMAL";
  } else if (response.data.priority === "高") {
    projectForm.value.priority = "HIGH";
  }
};
const submitForm = async () => {
  if (!projectForm.value.name) {
    ElMessage.error("项目名称不能为空");
    return;
  }
  if (!projectForm.value.start_date) {
    ElMessage.error("开始时间不能为空");
    return;
  }

  if (!projectForm.value.end_date) {
    ElMessage.error("结束时间不能为空");
    return;
  }

  if (isEdit) {
    try {
      const response = await updateProject(userId, projectForm.value);
      ElMessage({
        message: response.data.message,
        type: "success",
        duration: 1000,
      });
      setTimeout(() => {
        router.push({ name: "ProjectList" });
      }, 1000);
    } catch (error: any) {
      ElMessage.error(error.response?.data?.error || "项目更新失败，请重试");
    }
  } else {
    try {
      const response = await createProject(projectForm.value);
      ElMessage({
        message: response.data.message,
        type: "success",
        duration: 1000,
      });
      setTimeout(() => {
        router.push({ name: "ProjectList" });
      }, 1000);
    } catch (error: any) {
      ElMessage.error(error.response?.data?.error || "项目创建失败，请重试");
    }
  }
};
const goBack = () => {
  router.push({ name: "ProjectList" });
};

onMounted(() => {
  if (isEdit) {
    fetchProjectData(userId);
  }
});
</script>

<style scoped>
.project-detail-card {
  margin-top: 20px;
  width: 600px; /* 调整宽度 */
  padding: 40px; /* 调整内边距 */
  border-radius: 16px; /* 调整圆角 */
  box-shadow: 0 6px 30px rgba(0, 0, 0, 0.2); /* 增加阴影效果 */
  background-color: #f9f9f9; /* 设置背景颜色为浅灰色 */
  border: 1px solid #d0d0d0; /* 调整边框颜色 */
}

.input-field,
.date-picker,
.select-field {
  margin-bottom: 15px; /* 增加输入框之间的间距 */
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

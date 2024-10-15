<template>
  <div class="task-detail-container">
    <t-breadcrumb>
      <t-breadcrumb-item to="/index">首页</t-breadcrumb-item>
      <t-breadcrumb-item to="/index/tasks">任务列表</t-breadcrumb-item>
      <t-breadcrumb-item>任务详情</t-breadcrumb-item>
    </t-breadcrumb>

    <t-card class="task-card">
      <h2 class="task-title">{{ taskDetail.title }}</h2>
      <p class="task-description">
        <span class="label">描述:</span>{{ taskDetail.description }}
      </p>
      <p class="task-due-date">
        <span class="label">截止日期:</span>
        {{ formatDate(taskDetail.due_date) }}
      </p>
      <p class="task-assignee">
        <span class="label">负责人:</span>
        {{ taskDetail.assignee_name }}
      </p>
      <p class="task-status">
        <span class="label">状态:</span>
        <t-tag
          :theme="taskDetail.status === '已完成' ? 'success' : 'warning'"
          >{{ taskDetail.status }}</t-tag
        >
      </p>

      <div class="attachment-section">
        <span class="label">附件:</span>
        <div v-if="userRole === '成员'" class="file-section">
          <div v-if="taskDetail.status !== '已完成'">
            <t-upload
              :action="UPLOAD_URL"
              :data="{ task_id: taskDetail.id }"
              :multiple="false"
              @success="handleUploadSuccess"
              @error="handleUploadError"
              class="upload-file-button"
            >
              <t-button theme="default">上传文件</t-button>
            </t-upload>
          </div>
          <div v-if="taskDetail.attachmentUrl" class="view-file-section">
            <t-button theme="default" @click="downloadFile">
              查看附件
            </t-button>
          </div>
          <div v-else>
            <p>没有上传的附件</p>
          </div>
        </div>
        <div v-else-if="userRole === '管理员' || userRole === '经理'">
          <div v-if="taskDetail.attachmentUrl" class="view-file-section">
            <t-button theme="default" @click="downloadFile">
              查看附件
            </t-button>
          </div>
          <div v-else>
            <p>没有上传的附件</p>
          </div>
        </div>
      </div>

      <div class="comments-section">
        <p><span class="label">评论:</span></p>
        <div class="comment-input-section">
          <t-input
            v-model="newComment"
            placeholder="输入评论"
            maxlength="200"
            show-limit-hint
            class="comment-input"
          />
          <t-button @click="submitComment" theme="primary" class="submit-button"
            >提交评论</t-button
          >
        </div>
        <div class="comments-list">
          <div
            v-for="comment in taskComments"
            :key="comment.id"
            class="comment-item"
          >
            <p>
              <span style="font-weight: bold">{{ comment.author_name }}</span
              >: {{ comment.content }}
            </p>
            <p class="comment-time">{{ formatDate(comment.created_at) }}</p>
          </div>
        </div>
      </div>
      <div class="task-actions">
        <div v-if="userRole === '成员'">
          <t-button
            :disabled="taskDetail.status === '已完成'"
            theme="primary"
            size="large"
            @click="markAsComplete"
          >
            标记为完成
          </t-button>
        </div>
        <t-button @click="goBack" size="large" class="back-button"
          >返回</t-button
        >
      </div>
    </t-card>
  </div>
</template>

<script lang="ts" setup>
import { ref, computed, onMounted } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useStore } from "vuex";
import { ElMessage } from "element-plus";
import {
  fetchTaskById,
  downloadTaskFile,
  updateTaskStatus,
  getTaskComments,
  submitTaskComment,
} from "@/api/tasks";
import { UPLOAD_URL } from "@/constants/constants";

const store = useStore();
const route = useRoute();
const router = useRouter();

const taskId = Number(route.params.id);
const userRole = computed(() => store.getters.getUserRole);

interface TaskDetail {
  id: number;
  title: string;
  description: string;
  due_date: string;
  assignee_name: string;
  status: string;
  attachmentUrl: string;
}

const taskDetail = ref<TaskDetail>({} as TaskDetail);

interface Comment {
  id: number;
  author_name: string;
  content: string;
  created_at: string;
}

const taskComments = ref<Comment[]>([]);
const newComment = ref("");

const getTaskDetail = async () => {
  const response = await fetchTaskById(taskId);
  taskDetail.value = response.data;
};

const formatDate = (date: string) => {
  return new Date(date).toLocaleString();
};

const handleUploadSuccess = (response: any) => {
  taskDetail.value.attachmentUrl = response.response.file_path;
  ElMessage({
    message: response.response.message,
    type: "success",
    duration: 1000,
  });
};

const handleUploadError = (error: any) => {
  ElMessage({
    message: error.response ? error.response.message : "文件上传失败，请重试。",
    type: "error",
    duration: 1000,
  });
};

const downloadFile = async () => {
  try {
    const response = await downloadTaskFile(taskDetail.value.attachmentUrl);
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement("a");
    link.href = url;
    const filename = taskDetail.value.attachmentUrl.substring(
      taskDetail.value.attachmentUrl.lastIndexOf("/") + 1
    );
    link.setAttribute("download", filename);
    document.body.appendChild(link);
    link.click();
    link.remove();
  } catch (error) {
    ElMessage({
      message: "下载失败，请重试。",
      type: "error",
      duration: 1000,
    });
  }
};

const markAsComplete = async () => {
  try {
    const response = await updateTaskStatus(taskDetail.value.id, "COMPLETED");
    if (response.status === 200) {
      taskDetail.value.status = "已完成";
      ElMessage({
        message: response.data.message,
        type: "success",
        duration: 1000,
      });
    }
  } catch (error) {
    ElMessage({
      message: "标记完成失败，请重试。",
      type: "error",
      duration: 1000,
    });
  }
};

const goBack = () => {
  router.push({ name: "TaskList" });
};

const getComments = async () => {
  const response = await getTaskComments(taskId);
  taskComments.value = response.data.comments;
};
const submitComment = async () => {
  if (newComment.value.trim()) {
    try {
      const response = await submitTaskComment(taskId, {
        content: newComment.value,
      });
      taskComments.value.push(response.data.comment);
      newComment.value = "";
    } catch (error) {
      ElMessage({
        message: "评论提交失败，请重试。",
        type: "error",
        duration: 1000,
      });
    }
  } else {
    ElMessage({
      message: "评论内容不能为空。",
      type: "warning",
      duration: 1000,
    });
  }
};

onMounted(async () => {
  await getTaskDetail();
  await getComments();
});
</script>

<style scoped>
.task-detail-container {
  padding-bottom: 40px;
}
.task-detail-page {
  background-color: #f9f9f9;
  border-radius: 8px;
}
.task-card {
  background-color: #ffffff;
  border-radius: 10px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  padding: 20px;
  margin-top: 15px;
  max-width: 1200px;
  margin-left: auto;
  margin-right: auto;
}
.task-title {
  margin-bottom: 20px;
  font-size: 28px;
  font-weight: bold;
  color: #333;
}
.task-description,
.task-due-date,
.task-assignee,
.task-status,
.task-priority,
.task-project {
  margin: 10px 0;
  font-size: 16px;
  color: #555;
}

.label {
  font-weight: bold;
  margin-right: 5px;
}

.attachment-section {
  margin-top: 20px;
  display: flex;
}

.upload-attachment {
  margin-right: 10px;
}

.file-section {
  display: flex;
}

.upload-file-button {
  margin-right: 20px;
}

.attachment-link {
  margin-top: 10px;
  font-size: 16px;
}
.comments-section {
  margin-top: 20px;
}
.comment-input-section {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 10px;
}
.submit-button {
  margin-left: 10px;
}
.comment-item {
  margin-bottom: 10px;
  border-bottom: 1px solid #e0e0e0;
  padding-bottom: 10px;
}
.comment-time {
  color: #999;
  font-size: 12px;
}
.task-actions {
  display: flex;
  gap: 10px;
  justify-content: center;
}
</style>

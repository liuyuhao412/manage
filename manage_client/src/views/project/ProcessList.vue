<template>
  <div>
    <t-breadcrumb>
      <t-breadcrumb-item to="/index">首页</t-breadcrumb-item>
      <t-breadcrumb-item to="/index/processes">进度列表</t-breadcrumb-item>
    </t-breadcrumb>
    <t-card class="list-card-container" :bordered="false">
      <t-row justify="end">
        <div class="search-input" style="width: 300px">
          <t-input v-model="searchValue" clearable @input="filterProcesses">
            <template #suffix-icon>
              <search-icon size="16px" />
            </template>
          </t-input>
        </div>
      </t-row>
      <div class="table-container">
        <t-table
          :data="filtered_process_list"
          :columns="COLUMNS"
          :row-key="rowKey"
          vertical-align="top"
          :hover="true"
          :pagination="pagination"
          @page-change="rehandlePageChange"
          @select-change="(value: string[]) => rehandleSelectChange(value)"
        >
          <template #id="{ row }">
            <span>{{ row.id }}</span>
          </template>
          <template #name="{ row }">
            <span>{{ row.project_name }}</span>
          </template>
          <template #completion_rate="{ row }">
            <div>
              <t-progress theme="line" :percentage="row.completion_rate" />
            </div>
          </template>
          <template #update_time="{ row }">
            <span>{{ row.update_time }}</span>
          </template>
          <template #op="{ row }">
            <t-space>
              <t-link theme="primary" @click="() => openEditModal(row.id)"
                >编辑</t-link
              >
            </t-space>
          </template>
        </t-table>
      </div>
    </t-card>

    <t-dialog v-model:visible="isEditModalVisible" @confirm="updateProcess">
      <div class="dialog-content">
        <label class="dialog-label">项目名称: </label>
        <span class="project-name">{{ processForm.project_name }}</span>
        <div class="separator">
          <!-- 使用类来分隔 -->
          <label for="completion-rate" class="dialog-label"
            >完成率 (0% - 100%):
          </label>
          <t-slider
            v-model="processForm.completion_rate"
            :min="0"
            :max="100"
            id="completion-rate"
            class="dialog-slider"
          />
        </div>
      </div>
    </t-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { ElMessage } from "element-plus";
import { SearchIcon } from "tdesign-icons-vue-next";
import {
  fetchProcesses,
  fetchProcessById,
  updateProcessAPI,
} from "@/api/processes";

const COLUMNS = [
  { title: "项目进度ID", align: "center", colKey: "id", width: 60 },
  { title: "项目ID", align: "center", colKey: "project_id", width: 60 },
  { title: "项目名称", align: "center", colKey: "project_name", width: 130 },
  { title: "完成率", align: "center", colKey: "completion_rate", width: 130 },
  { title: "更新时间", align: "center", colKey: "update_time", width: 130 },
  { title: "操作", align: "center", colKey: "op", fixed: "right", width: 130 },
];

interface Process {
  id: number;
  project_id: number;
  project_name: string;
  completion_rate: number;
  update_time: string;
}

const process_list = ref<Array<Process>>([]);
const filtered_process_list = ref<Array<Process>>([]);
const rowKey = "id";
const searchValue = ref("");
const pagination = ref({ defaultPageSize: 5, total: 0, defaultCurrent: 1 });
const selectedRowKeys = ref<string[]>([]);
const isEditModalVisible = ref(false);

const processForm = ref<Process>({
  id: 0,
  project_id: 0,
  project_name: "",
  completion_rate: 0,
  update_time: "",
});

const rehandlePageChange = (curr: {
  current: number;
  previous: number;
  pageSize: number;
}) => {
  console.log(
    `当前页: ${curr.current}, 上一页: ${curr.previous}, 每页大小: ${curr.pageSize}`
  );
};

const filterProcesses = () => {
  if (searchValue.value.trim() === "") {
    filtered_process_list.value = process_list.value;
  } else {
    filtered_process_list.value = process_list.value.filter((project) => {
      return (
        project.project_name && project.project_name.includes(searchValue.value)
      );
    });
  }
};

const rehandleSelectChange = (val: string[]) => {
  selectedRowKeys.value = val;
};

const fetchProcessesData = async () => {
  const response = await fetchProcesses();
  process_list.value = response.data.processes;
  pagination.value.total = response.data.total;
  filtered_process_list.value = process_list.value;
};

const openEditModal = async (id: number) => {
  const response = await fetchProcessById(id);
  processForm.value = response.data;
  isEditModalVisible.value = true;
};

const updateProcess = async () => {
  try {
    const response = await updateProcessAPI(
      processForm.value.id,
      processForm.value.completion_rate
    );
    ElMessage({
      type: "success",
      message: response.data.message,
      duration: 1000,
    });
    setTimeout(async () => {
      isEditModalVisible.value = false;
      await fetchProcessesData();
    }, 1000);
  } catch (error: any) {
    ElMessage.error(error.response?.data?.error || "进度修改失败");
  }
};

onMounted(async () => {
  await fetchProcessesData();
});
</script>

<style scoped>
.table-container {
  max-width: 100%;
}
.list-card-container {
  padding: 10px;
}
.dialog-content {
  text-align: left;
  padding: 20px;
}
.dialog-label {
  color: #333;
}
.project-name {
  font-size: 16px;
  font-weight: bold;
}
.dialog-slider {
  margin-top: 10px;
  width: 100%;
}
.separator {
  margin-top: 10px; /* 新增的样式类 */
}
</style>

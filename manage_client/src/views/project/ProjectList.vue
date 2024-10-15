<template>
  <div class="container">
    <t-breadcrumb>
      <t-breadcrumb-item to="/index">首页</t-breadcrumb-item>
      <t-breadcrumb-item to="/index/projects">项目列表</t-breadcrumb-item>
    </t-breadcrumb>
    <t-card class="list-card-container" :bordered="false">
      <t-row justify="space-between">
        <div class="left-operation-container">
          <t-button @click="addProject">添加项目</t-button>
          <p v-if="selectedRowKeys.length" class="selected-count">
            已选{{ selectedRowKeys.length }}项
          </p>
        </div>
        <div class="search-input">
          <t-input v-model="searchValue" clearable @input="filterProjects">
            <template #suffix-icon>
              <search-icon size="16px" />
            </template>
          </t-input>
        </div>
      </t-row>
      <div class="table-container">
        <t-table
          :data="filtered_project_list"
          :columns="COLUMNS"
          :row-key="rowKey"
          vertical-align="top"
          :hover="true"
          :pagination="pagination"
          :selected-row-keys="selectedRowKeys"
          @page-change="rehandlePageChange"
          @select-change="(value: string[]) => rehandleSelectChange(value)"
        >
          <template #id="{ row }">
            <span>{{ row.id }}</span>
          </template>
          <template #name="{ row }">
            <span>{{ row.name }}</span>
          </template>
          <template #status="{ row }">
            <t-tag v-if="row.status === '进行中'" theme="warning">进行中</t-tag>
            <t-tag v-else-if="row.status === '已完成'" theme="success"
              >已完成</t-tag
            >
            <t-tag v-else-if="row.status === '已归档'" theme="default"
              >已归档</t-tag
            >
          </template>

          <template #priority="{ row }">
            <t-tag v-if="row.priority === '高'" theme="danger">高</t-tag>
            <t-tag v-else-if="row.priority === '正常'" theme="warning"
              >正常</t-tag
            >
            <t-tag v-else-if="row.priority === '低'" theme="success">低</t-tag>
          </template>

          <template #op="{ row }">
            <t-space>
              <t-link theme="primary" @click="handleEdit(row.id)">编辑</t-link>
              <t-link theme="danger" @click="() => handleDelete(row.id)"
                >删除</t-link
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
import { ref, onMounted } from "vue";
import { fetchProjects, deleteProject } from "@/api/projects";
import { useRouter } from "vue-router";
import { ElMessage, ElMessageBox } from "element-plus";

const router = useRouter();

const COLUMNS = [
  { title: "项目ID", align: "center", colKey: "id", width: 60 },
  {
    title: "项目名称",
    align: "center",
    width: 100,
    colKey: "name",
    fixed: "left",
  },
  {
    title: "开始时间",
    align: "center",
    width: 120,
    colKey: "start_date",
    fixed: "left",
  },
  {
    title: "结束时间",
    align: "center",
    width: 120,
    colKey: "end_date",
    fixed: "left",
  },
  {
    title: "项目状态",
    align: "center",
    width: 80,
    colKey: "status",
    fixed: "left",
  },
  {
    title: "项目优先级",
    align: "center",
    width: 80,
    colKey: "priority",
    fixed: "left",
  },
  {
    title: "项目经理",
    align: "center",
    width: 80,
    colKey: "manager_name",
    fixed: "left",
  },
  { title: "操作", align: "center", width: 130, colKey: "op", fixed: "right" },
];

interface Project {
  id: number;
  name: string;
  start_date: string;
  end_date: string;
  status: string;
  priority: string;
  manager_name: string;
}

const project_list = ref<Array<Project>>([]);
const filtered_project_list = ref<Array<Project>>([]);
const pagination = ref({ defaultPageSize: 5, total: 0, defaultCurrent: 1 });
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

const fetchProjectsData = async () => {
  const response = await fetchProjects();
  project_list.value = response.data.projects;
  filtered_project_list.value = project_list.value;
  pagination.value.total = response.data.total;
};

const filterProjects = () => {
  if (searchValue.value.trim() === "") {
    filtered_project_list.value = project_list.value;
  } else {
    filtered_project_list.value = project_list.value.filter((project) => {
      return project.name && project.name.includes(searchValue.value);
    });
  }
};

const addProject = () => {
  router.push({ name: "ProjectAdd" });
};

const handleEdit = (id: number) => {
  router.push({ name: "ProjectEdit", params: { id } });
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
      const response = await deleteProject(id);
      if (response.data.result) {
        ElMessage({
          type: "success",
          message: response.data.message,
          duration: 1000,
        });
        project_list.value = project_list.value.filter(
          (project) => project.id !== id
        );
        filtered_project_list.value = filtered_project_list.value.filter(
          (project) => project.id !== id
        );
      }
    } catch (error: any) {
      ElMessage({
        message: error.response?.data?.error || "项目删除失败，请重试",
      });
    }
  } catch (error) {
    ElMessage({ message: "删除失败，请重试" });
  }
};

onMounted(async () => {
  await fetchProjectsData();
});
</script>

<style scoped>
.container {
  width: 100%;
}
.table-container {
  max-width: 100%;
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

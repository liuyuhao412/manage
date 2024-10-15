<template>
  <div>
    <t-breadcrumb>
      <t-breadcrumb-item to="/index">首页</t-breadcrumb-item>
      <t-breadcrumb-item to="/index/archived-projects"
        >归档项目列表</t-breadcrumb-item
      >
    </t-breadcrumb>
    <t-card class="list-card-container" :bordered="false">
      <div class="table-container">
        <t-table :data="archived_projects" :columns="COLUMNS" :row-key="rowKey">
          <template #id="{ row }">
            <span>{{ row.id }}</span>
          </template>
          <template #project_name="{ row }">
            <span>{{ row.project_name }}</span>
          </template>
          <template #archived_date="{ row }">
            <span>{{ row.archived_date }}</span>
          </template>
        </t-table>
      </div>
    </t-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { fetchArchivedProjects } from "@/api/projects";

const COLUMNS = [
  { title: "归档项目ID", align: "center", colKey: "id" },
  { title: "项目ID", align: "center", colKey: "project_id" },
  { title: "项目名称", align: "center", colKey: "project_name" },
  { title: "项目经理", align: "center", colKey: "manager_name" },
  { title: "归档日期", align: "center", colKey: "archived_date" },
];

interface ArchivedProject {
  id: number;
  project_id: number;
  project_name: string;
  archived_date: string;
}

const archived_projects = ref<Array<ArchivedProject>>([]);
const rowKey = "id";

const fetchArchivedProjectsData = async () => {
  const response = await fetchArchivedProjects();
  archived_projects.value = response.data.projects;
};

onMounted(async () => {
  await fetchArchivedProjectsData();
});
</script>

<style scoped>
.table-container {
  max-width: 100%;
}
.list-card-container {
  padding: 10px;
}
</style>

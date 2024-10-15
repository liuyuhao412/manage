<template>
  <t-layout class="layout-container">
    <t-header class="header">
      <div class="header-left">
        <t-button
          class="header-sidebar"
          theme="default"
          variant="text"
          shape="square"
          :collapsed="isCollapsed"
          @click="toggleSidebar"
        >
          <t-icon name="view-list" />
        </t-button>

        <img
          src="@/assets/images/logo.webp"
          alt="管理系统 Logo"
          class="header-logo"
        />
        <span class="header-name">管理系统</span>
      </div>
      <div class="header-right">
        <!-- <t-button theme="default" variant="text" shape="square">
          <t-icon name="setting" />
        </t-button>
        <t-button theme="default" variant="text" shape="square">
          <t-icon name="notification" />
        </t-button> -->
        <t-dropdown
          :options="[{ content: '退出登录', value: 'logout' }]"
          @click="handleDropdownClick"
        >
          <div class="username-container">
            {{ currentUserName }}
          </div>
        </t-dropdown>
      </div>
    </t-header>
    <t-layout class="main-layout">
      <t-aside
        class="sidebar"
        :width="isCollapsed ? '64px' : '232px'"
        :transition="true"
      >
        <t-menu
          theme="dark"
          :collapsed="isCollapsed"
          :default-value="$route.path"
        >
          <template v-if="userRole === '管理员'">
            <t-menu-item value="/index/users" to="/index/users">
              <template #icon><t-icon name="user-list" /></template>
              用户管理
            </t-menu-item>
            <t-submenu value="2" title="项目管理">
              <template #icon>
                <t-icon name="folder" />
              </template>
              <t-menu-item value="/index/projects" to="/index/projects"
                >项目管理</t-menu-item
              >
              <t-menu-item value="/index/processes" to="/index/processes"
                >进度管理</t-menu-item
              >
              <t-menu-item
                value="/index/archived-projects"
                to="/index/archived-projects"
                >归档管理</t-menu-item
              >
            </t-submenu>
            <t-menu-item value="/index/tasks" to="/index/tasks">
              <template #icon><t-icon name="task" /></template>
              任务管理
            </t-menu-item>
            <t-submenu value="4" title="个人设置">
              <template #icon><t-icon name="setting" /></template>
              <t-menu-item
                value="/index/reset-password"
                to="/index/reset-password"
                >重置密码</t-menu-item
              >
            </t-submenu>
          </template>
          <template v-else-if="userRole === '经理'">
            <t-submenu value="2" title="项目管理">
              <template #icon><t-icon name="folder" /></template>
              <t-menu-item value="/index/projects" to="/index/projects"
                >项目管理</t-menu-item
              >
              <t-menu-item value="/index/processes" to="/index/processes"
                >进度管理</t-menu-item
              >
              <t-menu-item
                value="/index/archived-projects"
                to="/index/archived-projects"
                >归档管理</t-menu-item
              >
            </t-submenu>
            <t-menu-item value="/index/tasks" to="/index/tasks">
              <template #icon><t-icon name="task" /></template>
              任务管理
            </t-menu-item>
            <t-submenu value="4" title="个人管理">
              <template #icon><t-icon name="setting" /></template>
              <t-menu-item
                value="/index/reset-password"
                to="/index/reset-password"
                >重置密码</t-menu-item
              >
            </t-submenu>
          </template>
          <template v-else-if="userRole === '成员'">
            <t-menu-item value="/index/tasks" to="/index/tasks">
              <template #icon><t-icon name="task" /></template>
              任务管理
            </t-menu-item>
            <t-submenu value="4" title="个人管理">
              <template #icon><t-icon name="setting" /></template>
              <t-menu-item
                value="/index/reset-password"
                to="/index/reset-password"
                >重置密码</t-menu-item
              >
            </t-submenu>
          </template>
          <template v-else-if="userRole === '用户'">
            <t-menu-item value="" to="">
              <template #icon><t-icon name="folder" /></template>
              项目查看
            </t-menu-item>
            <t-menu-item value="" to="">
              <template #icon><t-icon name="task" /></template>
              任务查看
            </t-menu-item>
            <t-submenu value="4" title="个人管理">
              <template #icon><t-icon name="setting" /></template>
              <t-menu-item
                value="/index/reset-password"
                to="/index/reset-password"
                >重置密码</t-menu-item
              >
            </t-submenu>
          </template>
          <template v-else>
            <t-menu-item value="/index/unauthorized" to="/index/unauthorized">
              <template #icon><t-icon name="warning" /></template>
              未授权访问
            </t-menu-item>
          </template>
        </t-menu>
      </t-aside>

      <t-content
        class="content-layout"
        :style="{ marginLeft: isCollapsed ? '64px' : '232px' }"
      >
        <div class="router-view-container">
          <router-view></router-view>
        </div>
      </t-content>
    </t-layout>
    <t-footer class="footer">
      <p>版权信息 &copy; 2024 个人项目。保留所有权利。</p>
    </t-footer>
  </t-layout>
</template>

<script lang="ts" setup>
import { useRouter } from "vue-router";
import { ref, computed, onMounted } from "vue";
import { ElMessageBox, ElMessage } from "element-plus";
import { useStore } from "vuex";
import { fetchCurrentUserName } from "@/api/login";

const router = useRouter();
const store = useStore();
const userRole = computed(() => store.getters.getUserRole);

const isCollapsed = ref(false);
const currentUserName = ref("");

const toggleSidebar = () => {
  isCollapsed.value = !isCollapsed.value;
};

const handleDropdownClick = (option: { value: string }) => {
  if (option.value === "logout") {
    ElMessageBox.confirm("您确定要退出登录吗？", "确认退出", {
      confirmButtonText: "确定",
      cancelButtonText: "取消",
      type: "warning",
    })
      .then(() => {
        ElMessage({
          message: "成功退出",
          type: "success",
          duration: 1000,
        });
        localStorage.removeItem("token");
        store.commit("setUserRole", null);
        store.commit("setToken", null);

        router.push("/login");
      })
      .catch(() => {
        ElMessage({
          message: "取消退出",
          type: "info",
          duration: 1000,
        });
      });
  }
};

onMounted(async () => {
  const response = await fetchCurrentUserName();
  currentUserName.value = response.data.username;
});
</script>

<style scoped>
.layout-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 50px;
  padding: 0 20px;
  background-color: #4caf50;
  /* 修改为绿色 */
  color: #ffffff;
  text-align: center;
  font-size: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.header-left {
  display: flex;
  align-items: center;
}

.header-sidebar {
  margin-right: 15px;
  color: #ffffff;
}

.header-logo {
  height: 40px;
  width: auto;
  margin-right: 10px;
}

.header-name {
  font-size: 18px;
  font-weight: bold;
  color: #ffffff;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.username-container {
  color: #ffffff; /* 修改字体颜色为白色 */
  font-size: 16px; /* 调整字体大小 */
  font-weight: normal; /* 设置字体为正常 */
  padding: 6px; /* 调整内边距 */
  border-radius: 8px; /* 增加圆角 */
  background-color: rgba(0, 0, 0, 0.5); /* 调整背景的透明度 */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2); /* 调整阴影效果 */
  transition: background-color 0.3s, box-shadow 0.3s; /* 添加过渡效果 */
}

.username-container:hover {
  background-color: rgba(0, 0, 0, 0.7); /* 悬浮时背景颜色变深 */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3); /* 悬浮时阴影效果增强 */
}

.main-layout {
  flex: 1;
  display: flex;
}

.sidebar {
  position: fixed;
  top: 50px;
  bottom: 40px;
  height: calc(100vh - 90px);
  width: 232px;
  background-color: #1f1f1f;
  transition: width 0.3s;
}

.content-layout {
  flex: 1;
  background-color: #ffffff;
  /* 修改为白色 */
  margin-top: 50px;
  overflow-y: scroll; /* 允许内容滚动 */
  padding-top: 10px;
  height: calc(100vh - 90px);
  transition: margin-left 0.3s;
}

.breadcrumb {
  margin-top: 5px;
  margin-left: 20px;
  margin-bottom: 5px;
}

.router-view-container {
  margin-left: 20px;
}

.footer {
  background-color: #4caf50;
  /* 修改为绿色 */
  color: #ffffff;
  text-align: center;
  height: 40px;
  padding: 10px;
  position: fixed;
  bottom: 0;
  left: 0;
  /* 确保页脚在侧边栏右侧 */
  right: 0;
}

/* 隐藏滚动条 */
.content-layout::-webkit-scrollbar {
  display: none; /* 隐藏滚动条 */
}
</style>

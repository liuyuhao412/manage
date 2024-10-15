import { createRouter, createWebHistory } from 'vue-router';
import { useStore } from 'vuex';
import { computed } from 'vue';
const routes = [
    {
        path: '/',
        redirect: '/login',
    },
    {
        path: '/index',
        name: 'Layout',
        component: () => import('@/components/Layout.vue'),
        meta: { title: '首页' }, // 添加鉴权
        children: [
            {
                path: 'users',
                name: 'UserList',
                component: () => import('@/views/user/UserList.vue'),
                meta: { title: '用户列表', requiresAuth: true, role: '管理员' },
            },
            {
                path: 'users/add',
                name: 'UserAdd',
                component: () => import('@/views/user/UserAdd.vue'),
                meta: { title: '添加用户', requiresAuth: true, role: ['管理员'] },
            },
            {
                path: 'users/edit/:id',
                name: 'UserEdit',
                component: () => import('@/views/user/UserAdd.vue'),
                meta: { title: '编辑用户', requiresAuth: true, role: ['管理员'] },
            },
            {
                path: 'projects',
                name: 'ProjectList',
                component: () => import('@/views/project/ProjectList.vue'),
                meta: { title: '项目列表', requiresAuth: true, role: ['管理员', '经理'] },
            },
            {
                path: 'projects/add',
                name: 'ProjectAdd',
                component: () => import('@/views/project/ProjectAdd.vue'),
                meta: { title: '添加项目', requiresAuth: true, role: ['管理员', '经理'] },
            },
            {
                path: 'projects/edit/:id',
                name: 'ProjectEdit',
                component: () => import('@/views/project/ProjectAdd.vue'),
                meta: { title: '编辑项目', requiresAuth: true, role: ['管理员', '经理'] },
            },
            {
                path: 'processes',
                name: 'ProcessList',
                component: () => import('@/views/project/ProcessList.vue'),
                meta: { title: '进度列表', requiresAuth: true, role: ['管理员', '经理'] },
            },
            {
                path: 'archived-projects',
                name: 'ArchivedProject',
                component: () => import('@/views/project/ArchivedProject.vue'),
                meta: { title: '项目归档列表', requiresAuth: true, role: ['管理员', '经理'] },

            },
            {
                path: 'tasks',
                name: 'TaskList',
                component: () => import('@/views/task/TaskList.vue'),
                meta: { title: '任务列表', requiresAuth: true, role: ['管理员', '经理', '成员'] },
            },
            {
                path: 'tasks/add',
                name: 'TaskAdd',
                component: () => import('@/views/task/TaskAdd.vue'),
                meta: { title: '添加任务', requiresAuth: true, role: ['管理员', '经理', '成员'] },
            },
            {
                path: 'tasks/edit/:id',
                name: 'TaskEdit',
                component: () => import('@/views/task/TaskAdd.vue'),
                meta: { title: '编辑任务', requiresAuth: true, role: ['管理员', '经理', '成员'] },
            },
            {
                path: 'tasks/detail/:id',
                name: 'TaskDetail',
                component: () => import('@/views/task/TaskDetail.vue'),
                meta: { title: '查看任务', requiresAuth: true, role: ['管理员', '经理', '成员'] },
            },
            {
                path: 'reset-password',
                name: 'ResetPassword',
                component: () => import('@/components/login/ResetPassword.vue'),
                meta: { title: '找回密码', requiresAuth: true, role: ['管理员', '经理', '成员', '用户'] },
            },
        ],
    },
    {
        path: '/login',
        name: 'Index',
        component: () => import('@/views/Index.vue'),
    },
    {
        path: '/:catchAll(.*)',
        redirect: '/unauthorized',
    },
    {
        path: '/unauthorized',
        name: 'Unauthorized',
        component: () => import('@/components/Unauthorized.vue'),
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

// 路由守卫
router.beforeEach((to, from, next) => {
    const store = useStore();
    const userRole = store.getters.getUserRole;
    const token = computed(() => store.getters.getToken);
    const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
    const requiredRoles = to.meta.role as string[];

    if (requiresAuth && !token.value) {
        next({ path: '/login' });
    } else if (requiresAuth && requiredRoles) {
        if (requiredRoles.includes(userRole as string)) {
            next();
        } else {
            localStorage.removeItem("token");
            store.commit("setUserRole", null);
            store.commit("setToken", null);
            next({ path: '/unauthorized' });
        }
    } else {
        next(); // 允许访问
    }
});

export default router;

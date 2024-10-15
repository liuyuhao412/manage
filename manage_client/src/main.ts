import { createApp } from 'vue'
import TDesign from 'tdesign-vue-next';
import ElementPlus from 'element-plus'
import store from './store/store';
import './style.css'
import 'tdesign-vue-next/es/style/index.css';
import 'element-plus/dist/index.css'
import App from './App.vue'
import router from './router'; // 导入 router
import { fetchUserRole } from './api/login';

const app = createApp(App)


const initApp = async () => {
    try {
        const token = localStorage.getItem('token') || '';
        if (token) {
            store.commit('setToken', token);
            const roleResponse = await fetchUserRole(token);

            if (roleResponse.data && roleResponse.data.role) {
                store.commit('setUserRole', roleResponse.data.role);
            } else {
                // 如果获取角色失败，跳转到登录页面
                router.push('/login');
            }
        } else {
            // 没有 token 的情况也跳转到登录页面
            router.push('/login');
        }
    } catch (error) {
        console.error('Error fetching user role:', error);
        // 处理错误情况，如网络错误或 API 返回错误，跳转到登录页面
        router.push('/login');
    }
    app.use(TDesign);
    app.use(router);
    app.use(ElementPlus)
    app.use(store);
    app.mount('#app');
}


initApp();


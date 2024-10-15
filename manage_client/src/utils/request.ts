import axios from 'axios';
import { DEFAULT_API_URL } from '@/constants/constants';

const instance = axios.create({
  baseURL: DEFAULT_API_URL,
  timeout: 1000,
});

// 添加请求拦截器
instance.interceptors.request.use(config => {
  // 在请求发送之前做些什么
  const token = localStorage.getItem('token') || '';
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, error => {
  // 对请求错误做些什么
  return Promise.reject(error);
});

// 添加响应拦截器
instance.interceptors.response.use(response => {
  // 对响应数据做些什么
  return response;
}, error => {
  // 对响应错误做些什么
  return Promise.reject(error);
});

export default instance;
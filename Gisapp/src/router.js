import { createRouter, createWebHistory } from 'vue-router';
import Map from '@/MapPage.vue';

// 定义路由
const routes = [
//   {
//     path: '/',
//     name: 'Home',
//     component: Home,
//   },
  {
    path: '/',
    name: 'Map',
    component: Map,
  },
  // 更多路由...
];

// 创建 router 实例
const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes,
  });

export default router;

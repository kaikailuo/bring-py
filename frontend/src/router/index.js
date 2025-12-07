import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'

const routes = [
  {
    path: '/',
    redirect: '/home'
  },
  {
    path: '/home',
    name: 'Home',
    component: () => import('@/views/Home.vue'),
    meta: { title: '首页' }
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { title: '登录', hideForAuth: true }
  },
  {
    path: '/contact',
    name: 'Contact',
    component: () => import('@/views/Contact.vue'),
    meta: { title: '联系我们' }
  },
  {
    path: '/about-us',
    name: 'AboutUs',
    component: () => import('@/views/AboutUs.vue'),
    meta: { title: '关于我们' }
  },
  {
    path: '/feedback',
    name: 'Feedback',
    component: () => import('@/views/Feedback.vue'),
    meta: { title: '问题反馈' }
  },
  {
    path: '/student',
    name: 'Student',
    component: () => import('@/views/student/Layout.vue'),
    meta: { title: '学生端', requiresAuth: true, role: 'student' },
    children: [
      {
        path: '',
        name: 'StudentRedirect',
        redirect: '/student/dashboard'
      },
      {
        path: 'dashboard',
        name: 'StudentDashboard',
        component: () => import('@/views/student/Dashboard.vue'),
        meta: { title: '学习仪表盘' }
      },
      {
        path: 'course/:id',
        name: 'StudentCourse',
        component: () => import('@/views/student/CourseDetail.vue'),
        meta: { title: '课程详情' }
      },
      {
        path: 'practice',
        name: 'StudentPractice',
        component: () => import('@/views/student/Practice.vue'),
        meta: { title: '编程练习' }
      },
      {
        path: 'resources',
        name: 'StudentResources',
        component: () => import('@/views/student/Resources.vue'),
        meta: { title: '教学资源' }
      },
      {
        path: 'forum',
        name: 'StudentForum',
        component: () => import('@/views/student/Forum.vue'),
        meta: { title: '互动交流' }
      },
      {
        path: 'badges',
        name: 'StudentBadges',
        component: () => import('@/views/student/Badges.vue'),
        meta: { title: '徽章墙' }
      }
      ,
      {
        path: 'homework/:id',
        name: 'HomeworkDetail',
        component: () => import('@/views/student/HomeworkDetail.vue'),
        meta: { title: '作业详情' }
      }
    ]
  },
  {
    path: '/teacher',
    name: 'Teacher',
    component: () => import('@/views/teacher/Layout.vue'),
    meta: { title: '教师端', requiresAuth: true, role: 'teacher' },
    children: [
      {
        path: '',
        name: 'TeacherRedirect',
        redirect: '/teacher/dashboard'
      },
      {
        path: 'dashboard',
        name: 'TeacherDashboard',
        component: () => import('@/views/teacher/Dashboard.vue'),
        meta: { title: '教师仪表盘' }
      },
      {
        path: 'class-management',
        name: 'ClassManagement',
        component: () => import('@/views/teacher/ClassManagement.vue'),
        meta: { title: '班级管理' }
      },
      {
        path: 'resource-management',
        name: 'ResourceManagement',
        component: () => import('@/views/teacher/ResourceManagement.vue'),
        meta: { title: '资源管理' }
      },
      {
        path: 'analytics',
        name: 'Analytics',
        component: () => import('@/views/teacher/Analytics.vue'),
        meta: { title: '学情分析' }
      },
      {
        path: 'question-monitor',
        name: 'QuestionMonitor',
        component: () => import('@/views/teacher/QuestionMonitor.vue'),
        meta: { title: '问题监控' }
      }
    ]
  },
  // {
  //   path: '/admin',
  //   name: 'Admin',
  //   component: () => import('@/views/admin/Layout.vue'),
  //   meta: { title: '管理员', requiresAuth: true, role: 'admin' },
  //   children: [
  //     {
  //       path: '',
  //       redirect: '/admin/dashboard'
  //     },
  //     {
  //       path: 'dashboard',
  //       name: 'AdminDashboard',
  //       component: () => import('@/views/admin/Dashboard.vue'),
  //       meta: { title: '管理仪表盘' }
  //     },
  //     {
  //       path: 'user-management',
  //       name: 'UserManagement',
  //       component: () => import('@/views/admin/UserManagement.vue'),
  //       meta: { title: '用户管理' }
  //     },
  //     {
  //       path: 'system-settings',
  //       name: 'SystemSettings',
  //       component: () => import('@/views/admin/SystemSettings.vue'),
  //       meta: { title: '系统设置' }
  //     }
  //   ]
  // },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/NotFound.vue'),
    meta: { title: '页面未找到' }
  }
]

// 系统设置页
routes.splice(routes.length - 1, 0, {
  path: '/settings',
  name: 'SystemSettings',
  component: () => import('@/views/settings/SystemSettings.vue'),
  meta: { title: '系统设置' }
})

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  
  // 设置页面标题
  document.title = to.meta.title ? `${to.meta.title} - 高中信息技术教学平台` : '高中信息技术教学平台'
  
  // 检查是否需要登录
  if (to.meta.requiresAuth && !userStore.isLoggedIn) {
    next('/login')
    return
  }
  
  // 检查角色权限
  if (to.meta.role && userStore.user?.role !== to.meta.role) {
    // 根据用户角色重定向到对应页面
    if (userStore.user?.role === 'student') {
      next('/student')
    } else if (userStore.user?.role === 'teacher') {
      next('/teacher')
    } else if (userStore.user?.role === 'admin') {
      next('/admin')
    } else {
      next('/home')
    }
    return
  }
  
  // 已登录用户访问登录页面时重定向
  if (to.meta.hideForAuth && userStore.isLoggedIn) {
    if (userStore.user?.role === 'student') {
      next('/student')
    } else if (userStore.user?.role === 'teacher') {
      next('/teacher')
    } else {
      next('/home')
    }
    return
  }
  
  next()
})

export default router

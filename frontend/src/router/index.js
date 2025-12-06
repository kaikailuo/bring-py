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
        path: 'profile',
        name: 'StudentProfile',
        component: () => import('@/views/Profile.vue'),
        meta: { title: '个人主页' }
      },
      {
        path: 'user/:userId',
        name: 'StudentUserProfile',
        component: () => import('@/views/Profile.vue'),
        meta: { title: '用户主页' }
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
      },
      {
        path: 'profile',
        name: 'TeacherProfile',
        component: () => import('@/views/Profile.vue'),
        meta: { title: '个人主页' }
      },
      {
        path: 'user/:userId',
        name: 'TeacherUserProfile',
        component: () => import('@/views/Profile.vue'),
        meta: { title: '用户主页' }
      }
      ,
      {
        path: 'assignment-management',
        name: 'AssignmentManagement',
        component: () => import('@/views/teacher/AssignmentManager.vue'),
        meta: { title: '作业管理' }
      },
      {
        path: 'create-assignment',
        name: 'CreateAssignment',
        component: () => import('@/views/teacher/CreateAssignmentWizard.vue'),
        meta: { title: '布置作业向导' }
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

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  
  // 设置页面标题
  document.title = to.meta.title ? `${to.meta.title} - 高中信息技术教学平台` : '高中信息技术教学平台'
  
  // 获取用户角色（确保是字符串并转为小写）
  const userRole = userStore.user?.role ? String(userStore.user.role).toLowerCase() : null
  const requiredRole = to.meta.role ? String(to.meta.role).toLowerCase() : null
  
  console.log('路由守卫:', {
    to: to.path,
    from: from.path,
    isLoggedIn: userStore.isLoggedIn,
    userRole,
    requiredRole,
    requiresAuth: to.meta.requiresAuth
  })
  
  // 检查是否需要登录
  if (to.meta.requiresAuth && !userStore.isLoggedIn) {
    console.log('需要登录，重定向到登录页')
    next('/login')
    return
  }
  
  // 检查角色权限
  if (requiredRole && userRole !== requiredRole) {
    console.log('角色不匹配，重定向到对应页面')
    // 根据用户角色重定向到对应页面
    if (userRole === 'student') {
      next('/student')
    } else if (userRole === 'teacher') {
      next('/teacher')
    } else if (userRole === 'admin') {
      next('/admin')
    } else {
      next('/home')
    }
    return
  }
  
  // 已登录用户访问登录页面时重定向
  if (to.meta.hideForAuth && userStore.isLoggedIn) {
    console.log('已登录，从登录页重定向')
    if (userRole === 'student') {
      next('/student')
    } else if (userRole === 'teacher') {
      next('/teacher')
    } else {
      next('/home')
    }
    return
  }
  
  next()
})

export default router

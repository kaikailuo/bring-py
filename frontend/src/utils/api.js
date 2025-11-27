/**
 * API请求工具
 */

// API基础配置
const API_BASE_URL = 'http://localhost:8000/api'
export { API_BASE_URL }

// 请求拦截器
const request = async (url, options = {}) => {
  const token = localStorage.getItem('token')
  
  const defaultOptions = {
    headers: {
      'Content-Type': 'application/json',
      ...(token && { 'Authorization': `Bearer ${token}` })
    }
  }
  
  const config = {
    ...defaultOptions,
    ...options,
    headers: {
      ...defaultOptions.headers,
      ...options.headers
    }
  }
  
  try {
    const response = await fetch(`${API_BASE_URL}${url}`, config)
    const data = await response.json()
    
    if (!response.ok) {
      throw new Error(data.message || '请求失败')
    }
    
    return data
  } catch (error) {
    console.error('API请求错误:', error)
    throw error
  }
}

// 认证相关API
export const authAPI = {
  // 用户注册
  register: (userData) => {
    return request('/auth/register', {
      method: 'POST',
      body: JSON.stringify(userData)
    })
  },
  
  // 用户登录
  login: (loginData) => {
    return request('/auth/login', {
      method: 'POST',
      body: JSON.stringify(loginData)
    })
  },
  
  // 用户登出
  logout: () => {
    return request('/auth/logout', {
      method: 'POST'
    })
  },
  
  // 获取当前用户信息
  getCurrentUser: () => {
    return request('/auth/me', {
      method: 'GET'
    })
  },
  
  // 更新用户信息
  updateUser: (userData) => {
    return request('/auth/me', {
      method: 'PUT',
      body: JSON.stringify(userData)
    })
  },
  
  // 修改密码
  changePassword: (passwordData) => {
    return request('/auth/change-password', {
      method: 'POST',
      body: JSON.stringify(passwordData)
    })
  }
}

// 管理员API
export const adminAPI = {
  // 获取用户列表
  getUsers: (params = {}) => {
    const queryString = new URLSearchParams(params).toString()
    return request(`/auth/users?${queryString}`, {
      method: 'GET'
    })
  },
  
  // 激活用户
  activateUser: (userId) => {
    return request(`/auth/users/${userId}/activate`, {
      method: 'PUT'
    })
  },
  
  // 停用用户
  deactivateUser: (userId) => {
    return request(`/auth/users/${userId}/deactivate`, {
      method: 'PUT'
    })
  }
}

// 题目相关 API
export const problemsAPI = {
  getCourses: () => request('/problems/courses', { method: 'GET' }),
  getCourseProblems: (courseId) => request(`/problems/courses/${courseId}/problems`, { method: 'GET' }),
  // 获取题目 Markdown（需要以 text 返回）
  getProblemMarkdown: async (lesson, problem) => {
    const res = await fetch(`${API_BASE_URL}/problems/${lesson}/${problem}/problem`)
    if (!res.ok) {
      const text = await res.text()
      throw new Error(text || '获取题目失败')
    }
    return res.text()
  },
  run: (lesson, problem, code) => request(`/problems/${lesson}/${problem}/run`, { method: 'POST', body: JSON.stringify({ code }) }),
  submit: (lesson, problem, code) => request(`/problems/${lesson}/${problem}/submit`, { method: 'POST', body: JSON.stringify({ code }) }),
  // 教师端：创建题目（布置作业）
  createProblem: (courseId, payload) => request(`/problems/courses/${courseId}/problems`, { method: 'POST', body: JSON.stringify(payload) }),
  // 教师端：删除题目
  deleteProblem: (lesson, problem) => request(`/problems/${lesson}/${problem}`, { method: 'DELETE' })
}

export default {
  authAPI,
  adminAPI
  ,problemsAPI
}


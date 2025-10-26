/**
 * API请求工具
 */

// API基础配置
const API_BASE_URL = 'http://localhost:8000/api'

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

// 添加在文件末尾，adminAPI模块定义之后

// 资源管理API
export const resourceAPI = {
  // 获取资源列表
  getResources: (params = {}) => {
    const queryString = new URLSearchParams(params).toString();
    return request(`/resources?${queryString}`, {
      method: 'GET'
    });
  },

  // 获取资源详情
  getResourceDetail: (resourceId) => {
    return request(`/resources/${resourceId}`, {
      method: 'GET'
    });
  },

  // 上传资源
  uploadResource: (formData) => {
    return request('/resources', {
      method: 'POST',
      body: formData,
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
  },

  // 更新资源
  updateResource: (resourceId, resourceData) => {
    return request(`/resources/${resourceId}`, {
      method: 'PUT',
      body: JSON.stringify(resourceData)
    });
  },

  // 删除资源
  deleteResource: (resourceId) => {
    return request(`/resources/${resourceId}`, {
      method: 'DELETE'
    });
  },

  // 下载资源
  downloadResource: (resourceId) => {
    const token = localStorage.getItem('token');
    window.open(`${API_BASE_URL}/resources/${resourceId}/download?token=${token}`, '_blank');
  }
};

// 同时更新默认导出
export default {
  authAPI,
  adminAPI,
  resourceAPI
};
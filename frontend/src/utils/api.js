/**
 * API请求工具
 */

// API基础配置
const API_BASE_URL = 'http://localhost:8000/api'

// 请求拦截器
const request = async (url, options = {}) => {
  const token = localStorage.getItem('token')
  
  // 检测是否为 FormData 请求
  const isFormData = options.body instanceof FormData;
  
  const defaultOptions = {
    headers: {
      ...(!isFormData && { 'Content-Type': 'application/json' }), // 只有非 FormData 才设置默认 Content-Type
      ...(token && { 'Authorization': `Bearer ${token}` })
    }
  }
  
  const config = {
    ...defaultOptions,
    ...options,
    headers: {
      ...defaultOptions.headers,
      ...options.headers
    },
    credentials: 'include' // 始终包含凭证
  }
  
  try {
    const response = await fetch(`${API_BASE_URL}${url}`, config)
    
    // 对下载请求特殊处理
    if (options.isDownload) {
      if (!response.ok) {
        throw new Error('下载请求失败')
      }
      return response;
    }
    
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
    // 从FormData中提取元数据字段
    const title = formData.get('title');
    const description = formData.get('description');
    const type = formData.get('type');
    const category = formData.get('category');
    const courseId = formData.get('course_id');
    const courseName = formData.get('course_name'); // 添加course_name参数
    const file = formData.get('file');
    
    // 构建查询参数字符串
    const queryParams = new URLSearchParams({
      title,
      description: description || '',
      type,
      category
    });
    
    // 如果有课程ID，也添加到查询参数中
    if (courseId) {
      queryParams.append('course_id', courseId);
    }
    
    // 添加课程名称参数（如果有）
    if (courseName) {
      queryParams.append('course_name', courseName);
    }
    
    // 创建只包含文件的新FormData
    const fileFormData = new FormData();
    fileFormData.append('file', file);
    
    // 发送请求，不手动设置Content-Type，让浏览器自动处理
    return request(`/resources?${queryParams.toString()}`, {
      method: 'POST',
      body: fileFormData
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

  // 下载资源 - 使用Blob方式下载
  downloadResource: async (resourceId) => {
    try {
      // 使用request函数发送带认证的下载请求
      const response = await request(`/resources/${resourceId}/download`, {
        method: 'GET',
        isDownload: true
      });
      
      if (response.ok) {
        // 获取文件名（从响应头或使用默认名）
        const contentDisposition = response.headers.get('content-disposition');
        let filename = 'resource_file';
        if (contentDisposition) {
          const match = contentDisposition.match(/filename="([^"]+)"/);
          if (match) {
            filename = match[1];
          }
        }
        
        // 创建Blob并触发下载
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        
        // 清理
        setTimeout(() => {
          document.body.removeChild(link);
          window.URL.revokeObjectURL(url);
        }, 0);
      } else {
        console.error('下载失败');
        throw new Error('下载失败');
      }
    } catch (error) {
      console.error('下载错误:', error);
      throw error;
    }
  }
};

// 默认导出
export default {
  authAPI,
  adminAPI,
  resourceAPI
};
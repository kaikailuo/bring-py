/**
 * API请求工具
 */

// API基础配置
// 使用 127.0.0.1 避免在某些环境下 localhost 解析为 IPv6 (::1) 导致连接问题
const API_BASE_URL = 'http://127.0.0.1:8000/api'
export { API_BASE_URL }

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
    
    // 后端使用ApiResponse格式，即使HTTP状态码是200，也可能返回错误
    if (!response.ok || (data.code && data.code !== 200)) {
      const errorMessage = data.message || data.detail || '请求失败'
      const error = new Error(errorMessage)
      error.response = data
      throw error
    }
    
    return data
  } catch (error) {
    console.error('API请求错误:', error)
    throw error
  }
}

// 公开请求函数（不包含认证头）- 用于资源API
const publicRequest = async (url, options = {}) => {
  // 检测是否为 FormData 请求
  const isFormData = options.body instanceof FormData;
  
  const defaultOptions = {
    headers: {
      ...(!isFormData && { 'Content-Type': 'application/json' })
      // 不包含Authorization头
    }
  }
  
  const config = {
    ...defaultOptions,
    ...options,
    headers: {
      ...defaultOptions.headers,
      ...options.headers
    },
    credentials: 'include'
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
    
    // 后端使用ApiResponse格式，即使HTTP状态码是200，也可能返回错误
    if (!response.ok || (data.code && data.code !== 200)) {
      const errorMessage = data.message || data.detail || '请求失败'
      const error = new Error(errorMessage)
      error.response = data
      throw error
    }
    
    return data
  } catch (error) {
    console.error('公开API请求错误:', error)
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
  },
  
  // 获取当前用户个人资料
  getProfile: () => {
    return request('/auth/me/profile', {
      method: 'GET'
    })
  },
  
  // 更新当前用户个人资料
  updateProfile: (profileData) => {
    return request('/auth/me/profile', {
      method: 'PUT',
      body: JSON.stringify(profileData)
    })
  },
  
  // 获取指定用户个人资料
  getUserProfile: (userId) => {
    return request(`/auth/users/${userId}/profile`, {
      method: 'GET'
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


// 资源管理API 需要后期更改，先保留
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
  ,
  // 向导用：检查测评集（在后端运行给定 solution 与 tests）
  checkTests: (code, tests) => request('/problems/check_tests', { method: 'POST', body: JSON.stringify({ code, tests }) }),
  // 教师端：课程管理
  createCourse: (payload) => request('/problems/courses', { method: 'POST', body: JSON.stringify(payload) }),
  deleteCourse: (courseId) => request(`/problems/courses/${courseId}`, { method: 'DELETE' })
}



// 资源管理API - 公开访问，无需认证
export const resourceAPI = {
  // 获取资源列表（公开访问）
  getResources: (params = {}) => {
    // 过滤掉undefined、null和空字符串的参数，避免URLSearchParams将其转为字符串
    const validParams = {};
    Object.keys(params).forEach(key => {
      const value = params[key];
      if (value !== undefined && value !== null && value !== '') {
        validParams[key] = value;
      }
    });
    
    const queryString = new URLSearchParams(validParams).toString();
    const url = queryString ? `/resources?${queryString}` : '/resources';
    
    // 使用公开请求函数，不包含认证头
    return publicRequest(url, {
      method: 'GET'
    });
  },

  // 获取资源详情（公开访问）
  getResourceDetail: (resourceId) => {
    // 使用公开请求函数，不包含认证头
    return publicRequest(`/resources/${resourceId}`, {
      method: 'GET'
    });
  },

  // 上传资源
  // 上传资源
  uploadResource: (formData) => {
    // 直接使用传入的FormData，不需要重新创建
    // 从FormData中提取元数据字段用于构建查询参数
    // 注意：后端期望的字段名：title, description, type, category, course_id, course_name, file
    const title = formData.get('title') || '';
    const description = formData.get('description') || '';
    const type = formData.get('type') || 'other';
    // 使用后端支持的ResourceCategory枚举值：courseware, reference, assignment, other
    const category = formData.get('category') || 'courseware';
    const courseId = formData.get('course_id') || '';
    const courseName = formData.get('course_name') || '';
    
    // 构建查询参数字符串（后端通过Query参数接收元数据）
    const queryParams = new URLSearchParams({
      title: title,
      type: type,
      category: category
    });
    
    // 可选参数
    if (description) {
      queryParams.append('description', description);
    }
    if (courseId) {
      queryParams.append('course_id', courseId);
    }
    if (courseName) {
      queryParams.append('course_name', courseName);
    }
    
    // 直接使用原始的formData（包含文件）作为body
    // 后端通过File参数接收文件，字段名必须为'file'
    return request(`/resources?${queryParams.toString()}`, {
      method: 'POST',
      body: formData  // 直接使用传入的formData，包含file字段
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

  // 下载资源 - 使用Blob方式下载（公开访问）
  // resourceId: 资源ID
  // filename: 可选的文件名，如果提供则优先使用（从资源对象中获取）
  downloadResource: async (resourceId, filename = null) => {
    try {
      // 如果未提供文件名，先获取资源详情以获取文件名
      if (!filename) {
        try {
          const resourceDetail = await resourceAPI.getResourceDetail(resourceId);
          if (resourceDetail && resourceDetail.code === 200 && resourceDetail.data && resourceDetail.data.resource) {
            // 使用后端返回的file_name，确保包含扩展名
            filename = resourceDetail.data.resource.file_name || resourceDetail.data.resource.title || null;
          }
        } catch (e) {
          console.warn('获取资源详情失败，将尝试从响应头解析文件名:', e);
        }
      }
      
      // 使用公开请求函数发送下载请求（不包含认证头）
      const response = await publicRequest(`/resources/${resourceId}/download`, {
        method: 'GET',
        isDownload: true
      });
      
      if (!response.ok) {
        throw new Error('下载失败');
      }

      // 如果还未获取到文件名，尝试从Content-Disposition头中提取
      if (!filename) {
        const contentDisposition = response.headers.get('content-disposition');
        
        if (contentDisposition) {
          // 优先尝试RFC 5987格式（UTF-8编码）- 用于中文文件名
          const utf8Match = contentDisposition.match(/filename\*=UTF-8''([^;]+)/i);
          if (utf8Match) {
            try {
              filename = decodeURIComponent(utf8Match[1]);
            } catch (e) {
              console.warn('UTF-8文件名解码失败:', e);
            }
          }
          
          // 如果UTF-8格式未找到或解码失败，尝试标准格式
          if (!filename) {
            // 尝试带引号的格式：filename="filename.ext"
            const quotedMatch = contentDisposition.match(/filename="([^"]+)"/);
            if (quotedMatch) {
              filename = quotedMatch[1];
            } else {
              // 尝试不带引号的格式：filename=filename.ext
              const unquotedMatch = contentDisposition.match(/filename=([^;]+)/);
              if (unquotedMatch) {
                filename = unquotedMatch[1].trim();
                // 移除可能的引号
                filename = filename.replace(/^["']|["']$/g, '');
              }
            }
          }
        }
      }
      
      // 如果仍然没有文件名，使用默认值（包含扩展名）
      if (!filename || filename === 'download') {
        filename = `resource_${resourceId}.bin`;
        console.warn('无法获取文件名，使用默认名称:', filename);
      }
      
      // 创建Blob并触发下载
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = filename; // 使用获取到的文件名，确保包含扩展名
      document.body.appendChild(link);
      link.click();
      
      // 清理
      setTimeout(() => {
        document.body.removeChild(link);
        window.URL.revokeObjectURL(url);
      }, 0);
    } catch (error) {
      console.error('下载错误:', error);
      throw error;
    }
  }
};

// AI 相关 API
export const aiAPI = {
  // 请求后端对指定帖子进行 AI 总结
  summarize: (postId) => request('/ai/summarize', { method: 'POST', body: JSON.stringify({ post_id: postId }) })
}

// 通用 http 方法，放在默认导出之前以避免暂时性死区（TDZ）错误
export const http = {
  get: (url) => request(url, { method: 'GET' }),
  post: (url, body) => request(url, { method: 'POST', body: JSON.stringify(body) }),
  put: (url, body) => request(url, { method: 'PUT', body: JSON.stringify(body) }),
  del: (url) => request(url, { method: 'DELETE' })
}

// 默认导出（包含通用 http）
export default {
  authAPI,
  adminAPI,
  problemsAPI,
  resourceAPI,
  aiAPI,
  http
};


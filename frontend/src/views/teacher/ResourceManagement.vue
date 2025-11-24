<template>
  <div class="resource-management-container">
    <!-- 页面标题栏 -->
    <div class="page-header">
      <h2>资源管理中心</h2>
      <p>管理课程讲义、课件、作业模板等教学资源</p>
    </div>

    <!-- 操作工具栏 -->
    <div class="toolbar">
      <!-- 搜索框 -->
      <div class="search-bar">
        <input 
          type="text" 
          v-model="searchQuery" 
          placeholder="搜索资源名称..." 
          class="search-input"
        >
        <button class="search-btn">
          <i class="icon-search"></i> 搜索
        </button>
      </div>

      <!-- 筛选器 -->
      <div class="filter-group">
        <select v-model="typeFilter" class="filter-select">
          <option value="">全部资源类型</option>
          <option value="ppt">PPT 课件</option>
          <option value="pdf">PDF 讲义</option>
          <option value="doc">文档作业</option>
          <option value="video">教学视频</option>
        </select>
        
        <select v-model="sortBy" class="filter-select">
          <option value="date-desc">最新上传</option>
          <option value="date-asc">最早上传</option>
          <option value="size-desc">文件大小 (大→小)</option>
          <option value="size-asc">文件大小 (小→大)</option>
        </select>
      </div>

      <!-- 上传按钮 -->
      <button class="primary-btn upload-btn" @click="openUploadModal">
        <i class="icon-upload"></i> 上传新资源
      </button>
    </div>

    <!-- 资源列表区域 -->
<div class="resource-list">
      <!-- 无资源状态 -->
      <div v-if="filteredResources.length === 0" class="empty-state">
        <img src="@/assets/icons/empty-resource.svg" alt="暂无资源" class="empty-icon">
        <p>暂无资源，点击"上传新资源"添加教学材料</p>
      </div>

      <!-- 资源卡片列表 -->
      <div class="resource-cards" v-else>
        <div class="resource-card" v-for="resource in filteredResources" :key="resource.id">
          <!-- 资源图标 -->
          <div class="resource-icon" :class="`type-${resource.type}`">
<i :class="getResourceIcon(resource.type)"></i>
</div>
          
          <!-- 资源信息 -->
          <div class="resource-info">
            <h3 class="resource-name">{{ resource.name }}</h3>
            <div class="resource-meta">
              <span class="meta-item">{{ formatFileSize(resource.size) }}</span>
              <span class="meta-item">{{ formatDate(resource.uploadDate) }}</span>
              <span class="meta-tag">{{ getResourceTypeName(resource.type) }}</span>
            </div>
          </div>

          <!-- 操作按钮组 -->
         <div class="resource-actions">
  <button class="action-btn" @click="downloadResource(resource)" title="下载">
    <el-icon><Download /></el-icon>
  </button>

  <button class="action-btn danger" @click="confirmDelete(resource)" title="删除">
    <el-icon><Delete /></el-icon>
  </button>
</div>
        </div>
      </div>
    </div>

    <!-- 分页控件 -->
    <div class="pagination" v-if="filteredResources.length > 0">
      <button class="page-btn" :disabled="currentPage === 1">上一页</button>
<span class="page-info">第 {{ currentPage }} 页 / 共 {{ totalPages }} 页</span>
      <button class="page-btn" :disabled="currentPage === totalPages">下一页</button>
    </div>
<!-- 上传资源模态框 -->
    <el-dialog 
      title="上传新资源" 
      v-model="uploadModalVisible" 
width="500px"
      :close-on-click-modal="false"
    >
      <div class="upload-modal-content">
        <!-- 文件选择区域 -->
        <div class="file-upload-area" :class="{ 'has-file': selectedFile }" @click="triggerFileSelect">
          <input 
            type="file" 
            ref="fileInput" 
            class="file-input" 
@change="handleFileSelect"
            accept=".ppt,.pptx,.pdf,.doc,.docx,.mp4,.mp3,.zip,.rar"
          >
          <div class="upload-placeholder" v-if="!selectedFile">
            <i class="icon-cloud-upload"></i>
            <p>点击或拖拽文件到此处上传</p>
            <p class="hint">支持 PPT/PDF/文档/视频等格式，单个文件不超过 200MB</p>
          </div>
          <div class="selected-file-info" v-else>
            <i :class="getResourceIcon(selectedFile.type)"></i>
            <div class="file-details">
              <p class="file-name">{{ selectedFile.name }}</p>
              <p class="file-size">{{ formatFileSize(selectedFile.size) }}</p>
            </div>
            <button class="remove-file-btn" @click="clearSelectedFile">
              <i class="icon-close"></i>
            </button>
          </div>
        </div>

        <!-- 资源元信息填写 -->
        <div class="resource-meta-form">
          <el-form :model="resourceMeta" label-width="100px">
            <el-form-item label="资源名称">
              <el-input 
                v-model="resourceMeta.name" 
                placeholder="默认为文件名"
              ></el-input>
            </el-form-item>
            <el-form-item label="资源类型">
              <el-select v-model="resourceMeta.type" placeholder="选择资源类型">
                <el-option label="PPT 课件" value="ppt" />
                <el-option label="PDF 讲义" value="pdf" />
                <el-option label="文档作业" value="doc" />
                <el-option label="教学视频" value="video" />
                <el-option label="其他资源" value="other" />
              </el-select>
            </el-form-item>
            <el-form-item label="资源分类">
              <el-select v-model="resourceMeta.category" placeholder="选择分类">
                <el-option label="课件" value="courseware" />
                <el-option label="参考资料" value="reference" />
                <el-option label="作业" value="assignment" />
                <el-option label="其他" value="other" />
              </el-select>
            </el-form-item>
            <el-form-item label="课程关联">
              <el-select v-model="resourceMeta.courseId" placeholder="选择课程（可选）" clearable>
                <el-option label="不关联课程" value="" />
                <el-option label="全部" value="all" />
                <el-option label="第一课" value="lesson1" />
                <el-option label="高等数学（上）" value="101" />
                <el-option label="线性代数" value="102" />
                <el-option label="大学物理实验" value="103" />
              </el-select>
            </el-form-item>
            <el-form-item label="资源描述">
              <el-input 
                type="textarea" 
                v-model="resourceMeta.description" 
                rows="3"
                placeholder="简要描述资源内容（选填）"
              ></el-input>
            </el-form-item>
          </el-form>
        </div>
      </div>

      <template #footer>
        <button class="cancel-btn" @click="closeUploadModal">取消</button>
        <button 
          class="primary-btn upload-confirm-btn" 
          @click="handleUpload" 
          :disabled="!selectedFile || uploading"
        >
          <i class="icon-loading" v-if="uploading"></i>
          {{ uploading ? '上传中...' : '确认上传' }}
        </button>
      </template>
    </el-dialog>

    <!-- 删除确认对话框 -->
    <el-dialog 
      title="确认删除" 
      v-model="deleteConfirmVisible" 
      width="300px"
      :close-on-click-modal="false"
    >
      <p>确定要删除资源 "{{ currentResource?.name }}" 吗？此操作不可恢复。</p>
      <template #footer>
        <button class="cancel-btn" @click="deleteConfirmVisible = false">取消</button>
        <button class="danger-btn" @click="deleteResource">确认删除</button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
// 将import语句移到script标签顶部
import { resourceAPI } from '@/utils/api'

export default {
  
  data() {
    return {
      
      // 将模拟数据替换为空数组，从后端获取
      resources: [],
      searchQuery: '',
      typeFilter: '',
      sortBy: 'date-desc',
      currentPage: 1,
      pageSize: 10,

      // 上传相关状态
      uploadModalVisible: false,
      selectedFile: null,
      uploading: false,
      resourceMeta: {
        name: '',
        type: '',
        category: 'courseware', // 使用后端支持的枚举值，默认为courseware
        courseId: '',
        courseName: '',
        description: ''
      },

      // 删除相关状态
      deleteConfirmVisible: false,
      currentResource: null,
      totalPages: 0
    };
  },
  created() {
    // 组件创建时获取资源列表
    this.fetchResources()
  },
  computed: {
    // 筛选后的资源列表（保留原有的前端筛选逻辑）
    filteredResources() {
      let result = [...this.resources];
      
      // 搜索筛选
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        result = result.filter(res => 
          res.name.toLowerCase().includes(query)
        );
      }
      
      // 类型筛选
      if (this.typeFilter) {
        result = result.filter(res => res.type === this.typeFilter);
      }
      
      // 排序
      result.sort((a, b) => {
        if (this.sortBy === 'date-desc') {
          const dateA = a.uploadDate ? new Date(a.uploadDate).getTime() : 0;
          const dateB = b.uploadDate ? new Date(b.uploadDate).getTime() : 0;
          return dateB - dateA; // 降序：最新的在前
        } else if (this.sortBy === 'date-asc') {
          const dateA = a.uploadDate ? new Date(a.uploadDate).getTime() : 0;
          const dateB = b.uploadDate ? new Date(b.uploadDate).getTime() : 0;
          return dateA - dateB; // 升序：最旧的在前
        } else if (this.sortBy === 'size-desc') {
          return (b.size || 0) - (a.size || 0);
        } else if (this.sortBy === 'size-asc') {
          return (a.size || 0) - (b.size || 0);
        }
        return 0;
      });
      
      return result;
    }
  },
  methods: {
    // 获取资源列表的方法
    async fetchResources() {
      try {
        const params = {
          page: this.currentPage,
          page_size: this.pageSize
        }
        
        // 只添加非空的参数
        if (this.searchQuery && this.searchQuery.trim()) {
          params.search = this.searchQuery.trim()
        }
        if (this.typeFilter && this.typeFilter.trim()) {
          params.type_filter = this.typeFilter.trim()
        }
        
        const response = await resourceAPI.getResources(params)
        
        // 检查响应格式
        if (response && response.code === 200) {
          // 进行字段映射转换：将后端返回的字段映射为前端期望的字段
          const items = ((response.data && response.data.items) || []).map(item => ({
            ...item,
            // 将后端的 title 映射为前端的 name
            name: item.title || item.file_name || '未命名资源',
            // 将后端的 created_at 映射为前端的 uploadDate
            uploadDate: item.created_at || item.updated_at || new Date().toISOString()
          }))
          this.resources = items
          this.totalPages = Math.ceil((response.data?.total || 0) / this.pageSize)
        } else {
          // 响应格式错误或请求失败
          this.resources = []
          this.totalPages = 0
          const errorMessage = response?.message || '响应格式错误'
          console.error('获取资源列表失败:', errorMessage, response)
          throw new Error(errorMessage)
        }
      } catch (error) {
        this.resources = []
        this.totalPages = 0
        const errorMessage = error.message || '获取资源列表失败'
        this.$message.error(errorMessage)
        console.error('获取资源列表错误:', error)
      }
    },
    
    // 处理搜索和筛选变化
    handleSearch() {
      this.currentPage = 1
      this.fetchResources()
    },
  
    // 打开上传模态框
    openUploadModal() {
      this.uploadModalVisible = true;
      this.selectedFile = null;
      this.resourceMeta = { name: '', type: '', category: 'courseware', courseId: '', courseName: '', description: '' };
    },
  
    // 关闭上传模态框
    closeUploadModal() {
      this.uploadModalVisible = false;
      this.clearSelectedFile();
    },
  
    // 触发文件选择
    triggerFileSelect() {
      this.$refs.fileInput.click();
    },
  
    // 处理文件选择
    handleFileSelect(e) {
      const file = e.target.files[0];
      if (!file) return;
      
      // 提取文件类型
      const fileExt = file.name.split('.').pop().toLowerCase();
      const typeMap = {
        'ppt': 'ppt', 'pptx': 'ppt',
        'pdf': 'pdf',
        'doc': 'doc', 'docx': 'doc',
        'mp4': 'video', 'mp3': 'video'
      };
      
      this.selectedFile = {
        raw: file,
        name: file.name,
        size: file.size,
        type: typeMap[fileExt] || 'other'
      };
      
      // 自动填充资源名称和类型
      this.resourceMeta.name = file.name.replace(/\.[^/.]+$/, '');
      this.resourceMeta.type = this.selectedFile.type;
    },
  
    // 清除选中文件
    clearSelectedFile() {
      this.selectedFile = null;
      if (this.$refs.fileInput) {
        this.$refs.fileInput.value = '';
      }
    },
  
   async handleUpload() {
  if (!this.selectedFile) return
  
  this.uploading = true
  try {
    // 创建FormData对象，包含文件和所有元数据
    const formData = new FormData()
    // 文件字段名必须为 'file'，与后端期望一致
    formData.append('file', this.selectedFile.raw)
    // 元数据字段：title, description, type, category, course_id, course_name
    formData.append('title', this.resourceMeta.name || this.selectedFile.name)
    formData.append('description', this.resourceMeta.description || '')
    formData.append('type', this.resourceMeta.type || 'other')
    // 使用后端定义的ResourceCategory枚举值：courseware, reference, assignment, other
    formData.append('category', this.resourceMeta.category || 'courseware')
    
    // 课程关联信息
    if (this.resourceMeta.courseId) {
      formData.append('course_id', this.resourceMeta.courseId)
      // 根据课程ID自动设置课程名称
      const courseMap = {
        'all': '全部',
        'lesson1': '第一课',
        '101': '高等数学（上）',
        '102': '线性代数',
        '103': '大学物理实验'
      }
      const courseName = courseMap[this.resourceMeta.courseId] || this.resourceMeta.courseName
      if (courseName) {
        formData.append('course_name', courseName)
      }
    }
    
    // 调用API方法，直接使用传入的formData
    const response = await resourceAPI.uploadResource(formData)
    
    // 简化响应处理
    if (response && response.code === 200) {
      this.$message.success('资源上传成功')
      this.closeUploadModal()
      this.fetchResources() // 重新获取资源列表
    } else {
      this.$message.error('上传失败：' + (response?.message || '未知错误'))
    }
  } catch (error) {
    this.$message.error('上传出错，请重试')
    console.error('资源上传错误:', error)
  } finally {
    this.uploading = false
  }
},

    
    // 下载资源方法
    async downloadResource(resource) {
      try {
        // 使用resource对象中的file_name作为文件名（如果存在）
        // 优先使用file_name，因为它包含完整的文件名和扩展名
        const filename = resource.file_name || resource.title || null;
        // 调用API方法，传递resourceId和文件名
        await resourceAPI.downloadResource(resource.id, filename)
        this.$message.success('下载开始')
      } catch (error) {
        this.$message.error('下载失败，请重试')
        console.error('资源下载错误:', error)
      }
    },
    
    // 确认删除
    confirmDelete(resource) {
      this.currentResource = resource
      this.deleteConfirmVisible = true
    },
    
    // 删除资源
    async deleteResource() {
      if (!this.currentResource) return
      
      try {
        const response = await resourceAPI.deleteResource(this.currentResource.id)
        // 修复响应检查逻辑，将0改为200
        if (response && response.code === 200) {
          this.$message.success('资源删除成功')
          this.deleteConfirmVisible = false
          this.fetchResources() // 重新获取资源列表
        } else {
          this.$message.error('删除失败：' + (response?.message || '未知错误'))
        }
      } catch (error) {
        this.$message.error('删除出错，请重试')
        console.error('资源删除错误:', error)
      }
    },
    
    // 获取资源图标
    getResourceIcon(type) {
      const iconMap = {
        'ppt': 'icon-ppt',
        'pdf': 'icon-pdf',
        'doc': 'icon-doc',
        'video': 'icon-video',
        'other': 'icon-file'
      };
      return iconMap[type] || 'icon-file';
    },
    
    // 获取资源类型名称
    getResourceTypeName(type) {
      const typeMap = {
        'ppt': 'PPT 课件',
        'pdf': 'PDF 讲义',
        'doc': '文档作业',
        'video': '教学视频',
        'other': '其他资源'
      };
      return typeMap[type] || '其他资源';
    },
    
    // 格式化文件大小
    formatFileSize(bytes) {
      if (bytes < 1024) return bytes + ' B';
      else if (bytes < 1048576) return (bytes / 1024).toFixed(1) + ' KB';
      else return (bytes / 1048576).toFixed(1) + ' MB';
    },
    
    // 格式化日期
    formatDate(dateStr) {
      if (!dateStr) {
        return '未知日期'
      }
      
      // 处理ISO格式日期字符串（后端返回的created_at格式）
      const date = new Date(dateStr);
      
      // 检查日期是否有效
      if (isNaN(date.getTime())) {
        console.warn('Invalid date:', dateStr);
        return '日期格式错误'
      }
      
      return date.toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      });
    }
  }
}
</script>

<style scoped>
.resource-management-container {
  padding: 20px;
  max-width: 1400px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 24px;
  color: #333;
  
  h2 {
    font-size: 24px;
    margin-bottom: 8px;
  }
  
  p {
    color: #666;
    font-size: 14px;
  }
}

.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  flex-wrap: wrap;
  gap: 16px;
  
  .search-bar {
    display: flex;
    gap: 8px;
    
    .search-input {
      padding: 8px 12px;
      border: 1px solid #ddd;
      border-radius: 4px;
      width: 280px;
    }
    
    .search-btn {
      padding: 8px 16px;
      background: #409eff;
      color: white;
      border: none;
      border-radius: 4px;
      cursor: pointer;
    }
  }
  
  .filter-group {
    display: flex;
    gap: 12px;
    
    .filter-select {
      padding: 8px 12px;
      border: 1px solid #ddd;
      border-radius: 4px;
      background-color: white;
    }
  }
  
  .upload-btn {
    padding: 8px 20px;
    background: #67c23a;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 6px;
  }
}

.resource-list {
  margin: 20px 0;
  
  .empty-state {
    text-align: center;
    padding: 60px 0;
    color: #909399;
    background: #fafafa;
    border-radius: 8px;
    
    .empty-icon {
      width: 80px;
      height: 80px;
      margin-bottom: 16px;
      opacity: 0.5;
    }
    
    p {
      margin: 4px 0;
    }
  }
  
  .resource-cards {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
    gap: 16px;
  }
  
  .resource-card {
    display: flex;
    align-items: center;
    padding: 16px;
    border: 1px solid #eee;
    border-radius: 8px;
    transition: box-shadow 0.2s;
    
    &:hover {
      box-shadow: 0 2px 12px rgba(0,0,0,0.08);
    }
    
    .resource-icon {
      width: 48px;
      height: 48px;
      border-radius: 4px;
      display: flex;
      align-items: center;
      justify-content: center;
      margin-right: 16px;
      color: white;
      
      &.type-ppt { background: #f37021; }
      &.type-pdf { background: #e53e3e; }
      &.type-doc { background: #2563eb; }
      &.type-video { background: #7c3aed; }
      &.type-other { background: #6b7280; }
      
      i { font-size: 24px; }
    }
    
    .resource-info {
      flex: 1;
      min-width: 0;
      
      .resource-name {
        font-size: 16px;
        margin-bottom: 8px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
      }
      
      .resource-meta {
        display: flex;
        align-items: center;
        flex-wrap: wrap;
        gap: 12px;
        font-size: 12px;
        color: #666;
        
        .meta-tag {
          padding: 2px 8px;
          background: #f0f9ff;
          color: #165dff;
          border-radius: 12px;
          font-size: 11px;
        }
      }
    }
    
    .resource-actions {
      display: flex;
      gap: 8px;
      
      .action-btn {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        border: none;
        background: #f5f5f5;
        color: #666;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        
        &:hover {
          background: #e9e9e9;
        }
        
        &.danger {
          color: #f56c6c;
          &:hover {
            background: #fef0f0;
          }
        }
      }
    }
  }
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 30px;
  gap: 16px;
  color: #666;
  .page-btn {
    padding: 6px 12px;
    border: 1px solid #ddd;
    background: white;
    border-radius: 4px;
    cursor: pointer;
    
    &:disabled {
      color: #ccc;
      cursor: not-allowed;
      background: #f5f5f5;
    }
  }
}

.upload-modal-content {
  .file-upload-area {
    border: 2px dashed #ddd;
    border-radius: 6px;
    padding: 30px;
    text-align: center;
    cursor: pointer;
    transition: border-color 0.2s;
    margin-bottom: 20px;
    
    &.has-file {
      border-color: #409eff;
      background: #f0f9ff;
      padding: 16px;
      display: flex;
      align-items: center;
      text-align: left;
    }
    
    .upload-placeholder {
      color: #666;
      
      i {
        font-size: 48px;
        color: #999;
        margin-bottom: 12px;
      }
      
      .hint {
        font-size: 12px;
        color: #999;
        margin-top: 8px;
      }
    }
    
    .selected-file-info {
      flex: 1;
      
      .file-details {
        margin-left: 12px;
        display: inline-block;
        
        .file-name {
          font-weight: 500;
          margin-bottom: 4px;
        }
        
        .file-size {
          font-size: 12px;
          color: #666;
        }
      }
      
      .remove-file-btn {
        color: #f56c6c;
        background: transparent;
        border: none;
        cursor: pointer;
        padding: 4px;
        margin-left: auto;
      }
    }
  }
  
  .resource-meta-form {
    .el-form-item {
      margin-bottom: 16px;
    }
  }
}

/* 按钮样式统一 */
.primary-btn {
  background: #409eff;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 8px 16px;
  cursor: pointer;
  
  &:disabled {
    background: #a0cfff;
    cursor: not-allowed;
  }
}

.cancel-btn {
  background: white;
  color: #666;
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 8px 16px;
  cursor: pointer;
  margin-right: 8px;
}

.danger-btn {
  background: #f56c6c;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 8px 16px;
  cursor: pointer;
}

/* 图标字体占位（实际项目中需引入 iconfont 或使用 el-icon） */
.iconfont {
  font-family: "iconfont" !important;
  font-size: 16px;
  font-style: normal;
  -webkit-font-smoothing: antialiased;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .toolbar {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .search-bar .search-input {
    width: 200px;
  }
  
  .resource-cards {
    grid-template-columns: 1fr;
  }
}
</style>
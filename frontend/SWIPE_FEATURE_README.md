<!-- # 滑动功能实现说明

## 概述

本项目实现了完整的页面滑动功能，支持触摸滑动、鼠标拖拽、键盘控制等多种交互方式。滑动功能已集成到首页和仪表盘页面中。

## 功能特性

### 🎯 核心功能
- ✅ 触摸滑动支持（移动端）
- ✅ 鼠标拖拽支持（桌面端）
- ✅ 键盘左右箭头键控制
- ✅ 自动播放功能
- ✅ 循环播放
- ✅ 多种指示器样式
- ✅ 进度条显示
- ✅ 响应式设计

### 🎨 指示器样式
- **点状指示器** (`dots`): 经典圆点样式
- **条形指示器** (`bars`): 横向条形样式
- **数字指示器** (`numbers`): 数字序号样式
- **缩略图指示器** (`thumbnails`): 缩略图样式

### 📱 响应式支持
- 桌面端：显示网格布局
- 移动端：自动切换为滑动布局
- 平板端：自适应显示

## 组件结构

```
frontend/src/components/
├── SwipeContainer.vue      # 主滑动容器组件
└── SwipeIndicators.vue    # 滑动指示器组件

frontend/src/components/dashboard/
├── OverviewView.vue       # 概览视图
├── DetailedView.vue       # 详细视图
└── ProgressView.vue       # 进度视图
```

## 使用方法

### 基础用法

```vue
<template>
  <SwipeContainer
    :items="items"
    :items-per-view="1"
    :autoplay="true"
    :autoplay-delay="3000"
    :show-indicators="true"
    :show-navigation="true"
    :loop="true"
    @slide-change="onSlideChange"
  >
    <template #default="{ item }">
      <div class="slide-content">
        {{ item.content }}
      </div>
    </template>
  </SwipeContainer>
</template>
```

### 高级配置

```vue
<template>
  <SwipeContainer
    :items="items"
    :items-per-view="3"
    :autoplay="true"
    :autoplay-delay="4000"
    :show-indicators="true"
    :show-navigation="true"
    :loop="true"
    :indicator-type="'bars'"
    :show-progress="true"
    :indicator-color="'#667eea'"
    :indicator-size="'medium'"
    @slide-change="onSlideChange"
  >
    <!-- 内容模板 -->
  </SwipeContainer>
</template>
```

## 组件属性

### SwipeContainer 属性

| 属性名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `items` | Array | `[]` | 滑动项目数组 |
| `itemsPerView` | Number | `1` | 每页显示项目数量 |
| `autoplay` | Boolean | `false` | 是否自动播放 |
| `autoplayDelay` | Number | `3000` | 自动播放间隔（毫秒） |
| `loop` | Boolean | `true` | 是否循环播放 |
| `showIndicators` | Boolean | `true` | 是否显示指示器 |
| `showNavigation` | Boolean | `true` | 是否显示导航按钮 |
| `indicatorType` | String | `'dots'` | 指示器类型 |
| `showProgress` | Boolean | `false` | 是否显示进度条 |
| `indicatorColor` | String | `'#1890ff'` | 指示器颜色 |
| `indicatorSize` | String | `'medium'` | 指示器大小 |

### SwipeIndicators 属性

| 属性名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `items` | Array | `[]` | 指示器项目数组 |
| `currentIndex` | Number | `0` | 当前激活索引 |
| `type` | String | `'dots'` | 指示器类型 |
| `showProgress` | Boolean | `false` | 是否显示进度条 |
| `autoplay` | Boolean | `false` | 是否自动播放 |
| `autoplayDelay` | Number | `3000` | 自动播放间隔 |
| `color` | String | `'#1890ff'` | 指示器颜色 |
| `size` | String | `'medium'` | 指示器大小 |

## 事件

### SwipeContainer 事件

| 事件名 | 参数 | 说明 |
|--------|------|------|
| `slide-change` | `index` | 滑动索引改变时触发 |
| `touch-start` | `event` | 触摸开始时触发 |
| `touch-end` | - | 触摸结束时触发 |

## 应用场景

### 1. 首页功能特色展示
- **位置**: `/home` 页面功能特色部分
- **功能**: 移动端自动滑动展示四大核心功能
- **配置**: 条形指示器 + 进度条 + 自动播放

### 2. 仪表盘视图切换
- **位置**: `/student/dashboard` 页面
- **功能**: 三种数据视图的滑动切换
- **配置**: 按钮切换 + 无指示器 + 无自动播放

### 3. 测试页面
- **位置**: `/swipe-test` 页面
- **功能**: 展示所有滑动功能和配置选项
- **配置**: 多种指示器样式和配置组合

## 测试方法

### 1. 访问测试页面
```
http://localhost:3000/swipe-test
```

### 2. 测试功能
- 触摸滑动（移动设备）
- 鼠标拖拽（桌面设备）
- 键盘控制（左右箭头键）
- 自动播放
- 指示器点击
- 导航按钮

### 3. 响应式测试
- 调整浏览器窗口大小
- 使用开发者工具模拟移动设备
- 测试不同屏幕尺寸下的显示效果

## 浏览器兼容性

- ✅ Chrome 60+
- ✅ Firefox 55+
- ✅ Safari 12+
- ✅ Edge 79+
- ✅ 移动端浏览器

## 性能优化

1. **懒加载**: 组件按需加载
2. **防抖处理**: 触摸事件防抖
3. **动画优化**: 使用 CSS3 硬件加速
4. **内存管理**: 组件销毁时清理定时器

## 未来扩展

- [ ] 支持垂直滑动
- [ ] 添加更多动画效果
- [ ] 支持缩略图导航
- [ ] 添加手势识别
- [ ] 支持无限滚动

## 注意事项

1. 确保数据格式正确
2. 合理设置自动播放间隔
3. 注意移动端的触摸体验
4. 考虑无障碍访问支持

---

**开发团队**: 高中信息技术教学平台团队  
**最后更新**: 2024年12月 -->


import MarkdownIt from 'markdown-it'
import hljs from 'highlight.js'
import DOMPurify from 'dompurify'
// 引入 highlight.js 的样式（可根据喜好替换为其他主题）
import 'highlight.js/styles/github.css'

const md = new MarkdownIt({
  html: true,
  linkify: true,
  typographer: true,
  breaks: true,
  highlight: function (str, lang) {
    if (lang && hljs.getLanguage(lang)) {
      try {
        return '<pre class="hljs"><code>' + hljs.highlight(str, { language: lang }).value + '</code></pre>'
      } catch (__) {}
    }

    try {
      return '<pre class="hljs"><code>' + hljs.highlightAuto(str).value + '</code></pre>'
    } catch (__) {}

    return '<pre class="hljs"><code>' + md.utils.escapeHtml(str) + '</code></pre>'
  }
})

/**
 * 将 Markdown 文本渲染为安全的 HTML 字符串。
 * 会对生成的 HTML 做 DOMPurify 清理，防止 XSS。
 * @param {string} markdown
 * @returns {string} 安全的 HTML
 */
/**
 * 将 Markdown 文本渲染为安全的 HTML 字符串。
 * 可传入 options.assetBase 用来把相对图片路径替换为完整的后端访问路径。
 * @param {string} markdown
 * @param {{assetBase?: string}} options
 * @returns {string} 安全的 HTML
 */
export function renderMarkdown(markdown, options = {}) {
  if (!markdown) return ''

  let src = markdown

  // 如果传入 assetBase（例如 http://localhost:8000/api/problems/lesson_01/problem_01/assets），
  // 将 Markdown 中的相对图片路径替换为该基准路径下的完整 URL。
  if (options.assetBase) {
    // 匹配 Markdown 图片语法： ![alt](path) ，也处理内联 HTML 中的 <img src="...">
    // 先替换 Markdown 图片语法
    src = src.replace(/!\[([^\]]*)\]\(([^)]+)\)/g, (match, alt, url) => {
      const trimmed = url.trim().replace(/^"|"$/g, '')
      // 如果已经是绝对 URL 或 data URL，则不改写
      if (/^(https?:\/\/|data:|\/)/i.test(trimmed)) {
        return match
      }
      // 否则拼接 assetBase（确保没有重复斜杠）
      const cleanUrl = options.assetBase.replace(/\/$/, '') + '/' + trimmed.replace(/^\.\//, '')
      return `![${alt}](${cleanUrl})`
    })

    // 再替换 HTML img 标签中的 src
    src = src.replace(/<img\s+([^>]*?)src=("|')([^"']+)("|')([^>]*?)>/gi, (m, before, q1, url, q2, after) => {
      const trimmed = url.trim()
      if (/^(https?:\/\/|data:|\/)/i.test(trimmed)) {
        return m
      }
      const cleanUrl = options.assetBase.replace(/\/$/, '') + '/' + trimmed.replace(/^\.\//, '')
      return `<img ${before}src="${cleanUrl}"${after}>`
    })
  }

  // 将 markdown 转为 html
  const raw = md.render(src)
  // 使用 DOMPurify 清理（保留 class 等以便高亮生效）
  const clean = DOMPurify.sanitize(raw, { USE_PROFILES: { html: true } })
  return clean
}

export default renderMarkdown

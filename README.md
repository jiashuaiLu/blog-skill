# Tech Blog Writer Skill

专业技术博客写作助手，**完全交互式引导**，8 步工作流覆盖从选题到发布的全流程。

## 核心特性

- **7 种文章风格**：知乎专栏 / 论文 / 深度科普 / Newsletter / 教程实战 / 安全分析 / 工具推荐
- **4 套配色方案**：经典蓝橙（默认）/ 深空暗夜 / 薄荷清新 / 莫兰迪
- **3 种配图方式**：AI 生图（头图）/ 主 Agent 绘制 SVG / Mermaid 图表
- **URL 内容抓取**：trafilatura 解析任意网页为 LLM 可读 markdown
- **模型分层**：路由用轻量模型，写作用 GLM-5.1（40000 tokens）

## 8 步工作流

| 步骤 | 内容 | 说明 |
|------|------|------|
| 1 | 选择工作模式 | 自动（网络获取候选）/ 手动（指定 URL 或主题） |
| 2 | 获取原始内容 | URL → WebFetch → trafilatura 解析 → 原始素材 |
| 3 | 选择文章风格 | 7 种风格 + 模型选择（GLM-5.1 / 主 Agent） |
| 4 | 生成初稿 | 按风格硬规则生成，禁止虚构（论文风） |
| 5 | 人工审阅修改 | 用户确认，可反复迭代 |
| 6 | 配图与可视化 | 6a 配色 → 6b 配图方式（AI生图/SVG/Mermaid） |
| 7 | 选择发布渠道 | 掘金 / 知乎 / 微信公众号 / 个人博客 / GitHub |
| 8 | 发布文章 | 保存 post.md + 按渠道提供发布指导 |

## 配色方案

步骤 6a 会询问用户选择配色，所有图片/SVG/Mermaid 统一使用所选方案：

| 方案 | 主色 | 辅色 | 成功 | 背景 |
|------|------|------|------|------|
| **经典蓝橙**（默认） | `#3B6FE0` | `#F2A65A` | `#5BB47A` | `#FAFAF7` |
| **深空暗夜** | `#6C5CE7` | `#FDCB6E` | `#00B894` | `#2D3436` |
| **薄荷清新** | `#00B4D8` | `#FF6B6B` | `#2EC4B6` | `#F8F9FA` |
| **莫兰迪** | `#8D9DB6` | `#D4A373` | `#A3B18A` | `#FFFCF2` |

## 配图能力

### A. AI 头图生成

使用 `scripts/lib/image_gen.py` 调用生图 API（Gemini 3-Pro / gpt-image-2）：

```python
from scripts.lib.image_gen import build_prompt, generate_image
from pathlib import Path

prompt = build_prompt("文章标题", "核心视觉概念", style="hero")
result = generate_image(prompt, Path("pipeline/2026-05-20"), filename="hero.png")
```

- 输出 16:9 flat vector 风格头图
- 配色自动匹配步骤 6a 所选方案
- 不含文字、logo、人脸

### B. SVG 技术图表

主 Agent 直接编写 SVG 代码，适用于精确控制的技术图表：

- 三栏对比图、时间线图、柱状对比图、架构图、流程图
- 配色使用步骤 6a 选定的方案色值
- 字体：`PingFang SC` + `JetBrains Mono`
- 保存路径：`pipeline/{date}/fig-{序号}-{类型}.svg`

### C. Mermaid 图表

流程图 / 时序图 / 甘特图，自动注入配色主题：

```
%%{init: {"theme": "base", "themeVariables": {
  "primaryColor": "#FAFAF7",
  "primaryBorderColor": "#3B6FE0",
  "secondaryColor": "#F2A65A"
}}}%%
```

### 配图决策树

```
流程/时序?        → Mermaid
状态/关系?        → Mermaid 或 SVG 架构图
数据对比?         → SVG 柱状对比图
抽象概念/头图?    → AI 生图
多方案对比?       → SVG 三栏对比图
都不像?           → 别配图
```

## URL 内容抓取

新增 `fetch` / `fetch-html` 子命令，用 trafilatura 将任意网页解析为 LLM 可读的 markdown：

```bash
# 普通网页直接抓取
python3 tech-blog-writer.py fetch https://example.com -o article.md

# 微信公众号（需先用 Chrome DevTools 获取 HTML）
python3 tech-blog-writer.py fetch-html /tmp/page.json "https://mp.weixin.qq.com/s/xxx" -o article.md
```

微信公众号完整流程：
1. Chrome DevTools 打开页面 → `evaluate_script: document.documentElement.outerHTML`
2. 保存 HTML 到文件
3. `fetch-html` 解析 → 干净的 markdown + 元数据

## 模型配置

配置文件：`config/models.yaml`

| 阶段 | 模型 | 说明 |
|------|------|------|
| 粗筛 | Doubao-Seed-2-0-lite | 标题打分，低成本 |
| 推理 | DeepSeek-V4-Flash | 大纲/事实/评分 |
| 写作 | GLM-5.1 | 正文生成（40000 tokens） |
| 生图 | Gemini 3-Pro-Image-Preview | 头图生成，gpt-image-2 兜底 |

## 安装

```bash
cd skill
./install.sh
```

依赖：
- Python >= 3.10
- trafilatura >= 2.0（URL 抓取）
- httpx >= 0.27（HTTP 客户端）
- pyyaml >= 6.0（配置解析）
- python-dotenv（环境变量）
- rich（可选，美化界面）

## 文件结构

```
pipeline/{日期}/
├── brief.yaml           # 选题配置
├── facts.json           # 事实原料
├── outline.json         # 大纲
├── skeleton.json        # 骨架
├── draft.md             # 初稿
├── post.md              # 最终文章
├── hero.png             # 头图（AI 生图）
├── fig-01-arch.svg      # 架构图（SVG）
├── fig-02-compare.svg   # 对比图（SVG）
└── fig-03-flow.png      # 流程图（Mermaid 渲染）
```

## 相关文档

- [INSTALL.md](INSTALL.md) - 完整安装指南
- [docs/14-文章风格指南.md](docs/14-文章风格指南.md) - 7 种风格详解
- [docs/15-论文风格示例.md](docs/15-论文风格示例.md) - 论文风格完整示例
- [docs/17-发布渠道配置.md](docs/17-发布渠道配置.md) - 发布渠道配置
- [docs/18-模型配置说明.md](docs/18-模型配置说明.md) - 模型配置说明

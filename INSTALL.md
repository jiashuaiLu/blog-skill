# Tech Blog Writer Skill - 完整安装指南

## 🎯 支持的 IDE

- ✅ **Claude Code**
- ✅ **Trae IDE**（字节跳动）
- ✅ **其他支持 Python 的 IDE**

## 📦 安装方法

### 方法1：自动检测安装（推荐）

```bash
cd skill
./install.sh
```

脚本会自动检测已安装的 IDE，并让你选择安装目标。

### 方法2：安装到 Claude Code

```bash
cd skill
./install.sh  # 选择 1. Claude Code
```

安装后使用：
```
/tech-blog-writer
```

### 方法3：安装到 Trae IDE

```bash
cd skill
./install-trae.sh
```

安装后使用：
```bash
# 方法1：直接运行
~/agents/skills/tech-blog-writer/run.sh

# 方法2：创建别名
echo "alias blog-writer='~/agents/skills/tech-blog-writer/run.sh'" >> ~/.zshrc
source ~/.zshrc

# 然后运行
blog-writer
```

### 方法4：手动安装

```bash
# Claude Code
mkdir -p ~/.claude/skills/tech-blog-writer
cp -r skill/* ~/.claude/skills/tech-blog-writer/
chmod +x ~/.claude/skills/tech-blog-writer/tech-blog-writer.py

# Trae IDE
mkdir -p ~/agents/skills/tech-blog-writer
cp -r skill/* ~/agents/skills/tech-blog-writer/
chmod +x ~/agents/skills/tech-blog-writer/tech-blog-writer.py
```

## 📊 安装位置

| IDE | 安装位置 | 使用命令 |
|-----|----------|----------|
| **Claude Code** | `~/.claude/skills/tech-blog-writer/` | `/tech-blog-writer` |
| **Trae IDE** | `~/agents/skills/tech-blog-writer/` | `~/agents/skills/tech-blog-writer/run.sh` |

## 🤖 模型配置

### 选项1：使用专用写作模型（推荐）

**优点**：
- 成本可控（~$0.15-0.20/篇）
- 质量稳定
- 支持多模型协作

**配置方法**：

编辑 `config/models.yaml`：

```yaml
# 写作模型配置
llm_by_stage:
  draft: writer      # Claude-Sonnet-4.6
  outline: reasoner  # DeepSeek-V4-Flash
  facts: reasoner
  polish: writer

# 高配选项（可选）
models:
  writer_pro:
    provider: jd_anthropic
    name: Claude-Opus-4.7
```

**成本估算**：
- DeepSeek-V4-Flash: ~$0.02/篇
- Claude-Sonnet-4.6: ~$0.15/篇
- **总计**: ~$0.17/篇

### 选项2：使用主 Agent 模型

**优点**：
- 无需额外配置
- 使用当前会话的模型
- 简单直接

**使用方法**：

在步骤3选择"使用主 Agent 模型"，或在 `brief.yaml` 中设置：

```yaml
chosen:
  use_agent_model: true  # 使用主 Agent 模型
```

**注意**：
- 成本取决于当前 Agent 配置
- 可能无法使用多模型协作优势
- 建议在配置了高质量 Agent 的环境下使用

## 🎨 工作流程

### 8步交互式流程

```
步骤1: 选择工作模式
  ├─ 自动模式：从网络获取候选文章
  └─ 手动模式：手动输入主题

步骤2: 选择文章或主题
  ├─ 自动：从列表选择
  └─ 手动：输入标题、链接、简介

步骤3: 选择风格和模型配置 ⭐
  ├─ 文章风格：知乎风 / 论文风
  └─ 模型配置：专用模型 / 主 Agent 模型

步骤4: 生成初稿
  └─ 自动执行（提取事实→大纲→骨架→正文）

步骤5: 审阅和修改
  ├─ 满意：继续
  ├─ 手动编辑
  └─ 重新生成

步骤6: 添加图表（可选）
  ├─ 流程图
  ├─ 时序图
  ├─ 甘特图
  └─ 跳过

步骤7: 选择发布渠道
  └─ 多选（掘金、知乎、公众号等）

步骤8: 发布文章
  └─ 按渠道要求发布
```

## 📊 安装位置

| IDE | 安装位置 | 使用命令 |
|-----|----------|----------|
| **Claude Code** | `~/.claude/skills/tech-blog-writer/` | `/tech-blog-writer` |
| **Trae IDE** | `~/Library/Application Support/Trae/User/globalStorage/tech-blog-writer/` | `./run.sh` |

## 🔧 配置文件

### brief.yaml（文章配置）

```yaml
chosen:
  title: "文章标题"
  style: "paper"  # zhihu 或 paper
  use_agent_model: true  # 是否使用主 Agent 模型
  angle: "文章角度说明"
```

### models.yaml（模型配置）

```yaml
llm_by_stage:
  draft: writer      # 正文生成
  outline: reasoner  # 大纲生成

models:
  writer:
    provider: jd_anthropic
    name: Claude-Sonnet-4.6
```

## 🚀 快速开始

### Claude Code

```bash
# 1. 安装
cd skill && ./install.sh

# 2. 使用
/tech-blog-writer

# 3. 跟随引导完成 8 步流程
```

### Trae IDE

```bash
# 1. 安装
cd skill && ./install-trae.sh

# 2. 使用
~/Library/Application\ Support/Trae/User/globalStorage/tech-blog-writer/run.sh

# 3. 跟随引导完成 8 步流程
```

## ❓ 常见问题

### Q1: 不配置 models.yaml 可以用吗？

**A**: 可以！在步骤3选择"使用主 Agent 模型"，无需配置 models.yaml。

### Q2: 哪种模型配置更好？

**A**: 对比：

| 方案 | 优点 | 缺点 | 推荐场景 |
|------|------|------|----------|
| 专用模型 | 成本可控、质量稳定 | 需要配置 | 日常写作、批量生产 |
| 主 Agent 模型 | 无需配置、简单直接 | 成本不可控 | 偶尔使用、高质量要求 |

### Q3: 安装到 Trae IDE 后找不到命令？

**A**: Trae IDE 不像 Claude Code 有斜杠命令，需要：
```bash
# 方法1：直接运行
~/agents/skills/tech-blog-writer/run.sh

# 方法2：创建别名
alias blog-writer='~/agents/skills/tech-blog-writer/run.sh'
```

### Q4: 如何切换模型配置？

**A**: 修改 `brief.yaml`：
```yaml
chosen:
  use_agent_model: false  # 使用专用模型
  # 或
  use_agent_model: true   # 使用主 Agent 模型
```

### Q5: 如何卸载？

**A**:
```bash
# Claude Code
rm -rf ~/.claude/skills/tech-blog-writer

# Trae IDE
rm -rf ~/agents/skills/tech-blog-writer
```

## 📚 相关文档

- [README.md](README.md) - 完整功能说明
- [QUICKSTART.md](QUICKSTART.md) - 快速开始
- [docs/14-文章风格指南.md](docs/14-文章风格指南.md) - 风格选择
- [docs/15-论文风格示例.md](docs/15-论文风格示例.md) - 论文风格示例

## 🎉 总结

| 项目 | 说明 |
|------|------|
| **安装目标** | Claude Code ✅ / Trae IDE ✅ |
| **模型选择** | 专用模型 ✅ / 主 Agent 模型 ✅ |
| **使用方式** | 交互式 8 步引导 |
| **配置要求** | 可选（使用主 Agent 模型时无需配置） |

现在你已经可以在两个 IDE 中使用这个 skill 了！

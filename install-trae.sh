#!/bin/bash
# Tech Blog Writer Skill - Trae IDE 安装脚本

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}======================================${NC}"
    echo -e "${BLUE}  Tech Blog Writer Skill 安装程序${NC}"
    echo -e "${BLUE}  目标：Trae IDE${NC}"
    echo -e "${BLUE}======================================${NC}"
}

# 检测 Trae IDE skill 目录
detect_trae_skill_dir() {
    local skill_dir="$HOME/.agents/skills"

    if [ -d "$skill_dir" ]; then
        echo "$skill_dir"
    else
        echo ""
    fi
}

# 创建 Trae skill 目录
create_trae_skill_directory() {
    local skill_dir="$HOME/.agents/skills/tech-blog-writer"

    mkdir -p "$skill_dir"
    mkdir -p "$skill_dir/scripts"
    mkdir -p "$skill_dir/docs"

    echo "$skill_dir"
}

# 复制文件到 Trae
copy_files_to_trae() {
    local target_dir="$1"
    local source_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    local project_root="$(dirname "$source_dir")"

    print_info "复制 skill 文件到 Trae..."

    # 复制 skill 主文件
    cp "$source_dir/tech-blog-writer.py" "$target_dir/"
    cp "$source_dir/skill.yaml" "$target_dir/"
    cp "$source_dir/README.md" "$target_dir/"
    cp "$source_dir/QUICKSTART.md" "$target_dir/"
    cp "$source_dir/INSTALL.md" "$target_dir/"

    # 复制文档
    cp -r "$source_dir/docs/"* "$target_dir/docs/" 2>/dev/null || true

    # 复制核心脚本（从父目录）
    print_info "复制核心脚本..."
    cp -r "$project_root/scripts/"*.py "$target_dir/scripts/" 2>/dev/null || true
    cp -r "$project_root/scripts/lib" "$target_dir/scripts/" 2>/dev/null || true

    # 复制配置示例
    cp "$project_root/brief.yaml.example" "$target_dir/" 2>/dev/null || true

    print_info "文件复制完成"
}

# 设置权限
set_permissions() {
    local target_dir="$1"

    print_info "设置权限..."
    chmod +x "$target_dir/tech-blog-writer.py"
}

# 创建快捷启动脚本
create_launcher_script() {
    local target_dir="$1"

    print_info "创建快捷启动脚本..."

    cat > "$target_dir/run.sh" << 'EOF'
#!/bin/bash
# Tech Blog Writer Skill 启动脚本

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "$SCRIPT_DIR/tech-blog-writer.py" "$@"
EOF

    chmod +x "$target_dir/run.sh"
}

# 创建使用说明
create_usage_doc() {
    local target_dir="$1"

    cat > "$target_dir/USAGE.md" << 'EOF'
# Tech Blog Writer Skill - Trae IDE 使用说明

## 安装位置

```
~/agents/skills/tech-blog-writer/
```

## 使用方法

### 方法1：在 Trae IDE 终端中运行

```bash
# 进入安装目录
cd ~/agents/skills/tech-blog-writer

# 运行
./run.sh

# 或直接运行
python3 tech-blog-writer.py
```

### 方法2：在任意位置运行

```bash
~/agents/skills/tech-blog-writer/run.sh
```

### 方法3：创建别名

在 `~/.zshrc` 或 `~/.bashrc` 中添加：

```bash
alias blog-writer='~/agents/skills/tech-blog-writer/run.sh'
```

然后就可以在任何地方运行：

```bash
blog-writer
```

## 模型配置

### 使用专用写作模型（推荐）

需要配置 `config/models.yaml`：

```yaml
llm_by_stage:
  draft: writer      # GLM-5.1 (40000 tokens)
  outline: reasoner  # DeepSeek-V4-Flash
```

### 使用主 Agent 模型

在步骤3选择"使用主 Agent 模型"，无需配置 `models.yaml`。

## 工作流程

1. 选择工作模式（自动/手动）
2. 选择文章或主题
3. 选择风格和模型配置
4. 生成初稿
5. 审阅和修改
6. 添加图表（可选）
7. 选择发布渠道
8. 发布

## 注意事项

- 首次使用建议选择"自动模式"体验完整流程
- 论文风格记得在步骤3选择"使用主 Agent 模型"（如果没有配置 writer）
- 生成的文章在 `pipeline/{日期}/post.md`

## 更新

重新运行安装脚本即可：

```bash
./install-trae.sh
```

## 卸载

```bash
rm -rf ~/agents/skills/tech-blog-writer
```
EOF
}

# 验证安装
verify_installation() {
    local target_dir="$1"

    print_info "验证安装..."

    if [ -f "$target_dir/tech-blog-writer.py" ]; then
        print_info "✅ skill 主文件安装成功"
    else
        print_error "❌ skill 主文件安装失败"
        return 1
    fi

    if [ -f "$target_dir/run.sh" ]; then
        print_info "✅ 启动脚本创建成功"
    else
        print_error "❌ 启动脚本创建失败"
        return 1
    fi

    return 0
}

# 打印使用说明
print_usage() {
    local target_dir="$1"

    echo ""
    echo -e "${GREEN}======================================${NC}"
    echo -e "${GREEN}  Tech Blog Writer Skill 安装成功！${NC}"
    echo -e "${GREEN}  目标：Trae IDE${NC}"
    echo -e "${GREEN}======================================${NC}"
    echo ""
    echo "安装位置:"
    echo "  $target_dir"
    echo ""
    echo "使用方法:"
    echo "  cd ~/agents/skills/tech-blog-writer"
    echo "  ./run.sh"
    echo ""
    echo "或创建别名（添加到 ~/.zshrc）："
    echo "  alias blog-writer='~/agents/skills/tech-blog-writer/run.sh'"
    echo ""
    echo "然后运行："
    echo "  blog-writer"
    echo ""
    echo "查看详细说明："
    echo "  cat $target_dir/USAGE.md"
    echo ""
}

# 主函数
main() {
    print_header
    echo ""

    # 检测 Trae skill 目录
    skill_dir=$(detect_trae_skill_dir)

    if [ -z "$skill_dir" ]; then
        print_warn "~/agents/skills 目录不存在"
        print_info "将自动创建目录结构..."
    fi

    # 创建目录
    target_dir=$(create_trae_skill_directory)
    print_info "Skill 安装目录: $target_dir"

    # 复制文件
    copy_files_to_trae "$target_dir"

    # 设置权限
    set_permissions "$target_dir"

    # 创建启动脚本
    create_launcher_script "$target_dir"

    # 创建使用说明
    create_usage_doc "$target_dir"

    # 验证安装
    if verify_installation "$target_dir"; then
        print_usage "$target_dir"
        exit 0
    else
        print_error "安装失败"
        exit 1
    fi
}

# 运行主函数
main "$@"

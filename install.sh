#!/bin/bash
# Tech Blog Writer Skill - 通用安装脚本
# 自动检测环境并安装到正确的位置

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
    echo -e "${BLUE}======================================${NC}"
}

# 检测可用环境
detect_environments() {
    local envs=()

    # 检测 Claude Code
    if [ -d "$HOME/.claude" ]; then
        envs+=("claude-code")
    fi

    # 检测 Trae IDE（检查 ~/agents/skills 目录）
    if [ -d "$HOME/.agents/skills" ] || [ -d "/Applications/Trae CN.app" ]; then
        envs+=("trae-ide")
    fi

    echo "${envs[@]}"
}

# 安装到 Claude Code
install_to_claude_code() {
    local source_dir="$1"

    print_info "安装到 Claude Code..."

    local target_dir="$HOME/.claude/skills/tech-blog-writer"
    mkdir -p "$target_dir"
    mkdir -p "$target_dir/scripts"
    mkdir -p "$target_dir/docs"

    # 复制文件
    cp "$source_dir/tech-blog-writer.py" "$target_dir/"
    cp "$source_dir/skill.yaml" "$target_dir/"
    cp "$source_dir/README.md" "$target_dir/"
    cp "$source_dir/QUICKSTART.md" "$target_dir/"
    cp -r "$source_dir/docs/"* "$target_dir/docs/" 2>/dev/null || true

    # 复制核心脚本
    local project_root="$(dirname "$source_dir")"
    cp -r "$project_root/scripts/"*.py "$target_dir/scripts/" 2>/dev/null || true
    cp -r "$project_root/scripts/lib" "$target_dir/scripts/" 2>/dev/null || true

    chmod +x "$target_dir/tech-blog-writer.py"

    print_info "✅ Claude Code 安装完成: $target_dir"
    echo "  使用: /tech-blog-writer"
}

# 安装到 Trae IDE
install_to_trae_ide() {
    local source_dir="$1"

    print_info "安装到 Trae IDE..."

    local target_dir="$HOME/.agents/skills/tech-blog-writer"
    mkdir -p "$target_dir"
    mkdir -p "$target_dir/scripts"
    mkdir -p "$target_dir/docs"

    # 复制文件
    cp "$source_dir/tech-blog-writer.py" "$target_dir/"
    cp "$source_dir/skill.yaml" "$target_dir/"
    cp "$source_dir/README.md" "$target_dir/"
    cp "$source_dir/QUICKSTART.md" "$target_dir/"
    cp -r "$source_dir/docs/"* "$target_dir/docs/" 2>/dev/null || true

    # 复制核心脚本
    local project_root="$(dirname "$source_dir")"
    cp -r "$project_root/scripts/"*.py "$target_dir/scripts/" 2>/dev/null || true
    cp -r "$project_root/scripts/lib" "$target_dir/scripts/" 2>/dev/null || true

    chmod +x "$target_dir/tech-blog-writer.py"

    # 创建启动脚本
    cat > "$target_dir/run.sh" << 'EOF'
#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "$SCRIPT_DIR/tech-blog-writer.py" "$@"
EOF
    chmod +x "$target_dir/run.sh"

    print_info "✅ Trae IDE 安装完成: $target_dir"
    echo "  使用: ~/agents/skills/tech-blog-writer/run.sh"
}

# 主函数
main() {
    print_header
    echo ""

    local source_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

    # 检测可用环境
    local envs=$(detect_environments)

    if [ -z "$envs" ]; then
        print_error "未检测到支持的 IDE 环境"
        print_info "支持的 IDE:"
        print_info "  - Claude Code (~/.claude)"
        print_info "  - Trae IDE (~/agents/skills)"
        exit 1
    fi

    print_info "检测到以下环境: $envs"
    echo ""

    # 如果有多个环境，让用户选择
    if [[ "$envs" == *" "* ]]; then
        print_info "检测到多个环境，请选择安装目标："
        echo "  1. Claude Code"
        echo "  2. Trae IDE"
        echo "  3. 全部安装"
        echo ""

        read -p "请选择 [1-3]: " choice

        case $choice in
            1)
                install_to_claude_code "$source_dir"
                ;;
            2)
                install_to_trae_ide "$source_dir"
                ;;
            3)
                install_to_claude_code "$source_dir"
                echo ""
                install_to_trae_ide "$source_dir"
                ;;
            *)
                print_error "无效选择"
                exit 1
                ;;
        esac
    else
        # 只有一个环境，直接安装
        if [[ "$envs" == *"claude-code"* ]]; then
            install_to_claude_code "$source_dir"
        elif [[ "$envs" == *"trae-ide"* ]]; then
            install_to_trae_ide "$source_dir"
        fi
    fi

    echo ""
    print_info "======================================"
    print_info "  安装完成！"
    print_info "======================================"
    echo ""
    print_info "快速开始："
    echo "  1. 运行 skill"
    echo "  2. 选择工作模式（自动/手动）"
    echo "  3. 选择文章风格"
    echo "  4. 选择模型配置"
    echo "  5. 跟随引导完成文章生成"
    echo ""
}

# 运行主函数
main "$@"

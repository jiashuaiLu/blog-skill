#!/bin/bash
# Tech Blog Writer Skill 卸载脚本

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warn() {
    echo -e "${YELLOW[WARN]${NC} $1"
}

# 检测 Claude Code 配置目录
detect_claude_dir() {
    if [ -d "$HOME/.claude/skills/tech-blog-writer" ]; then
        echo "$HOME/.claude"
    elif [ -d "$HOME/.config/claude/skills/tech-blog-writer" ]; then
        echo "$HOME/.config/claude"
    else
        echo ""
    fi
}

# 主函数
main() {
    echo "======================================"
    echo "  Tech Blog Writer Skill 卸载程序"
    echo "======================================"
    echo ""

    claude_dir=$(detect_claude_dir)

    if [ -z "$claude_dir" ]; then
        print_info "未找到已安装的 Tech Blog Writer Skill"
        exit 0
    fi

    skill_dir="$claude_dir/skills/tech-blog-writer"

    print_info "找到安装目录: $skill_dir"
    read -p "确认卸载? (y/N): " confirm

    if [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]; then
        rm -rf "$skill_dir"
        print_info "✅ Tech Blog Writer Skill 已卸载"
    else
        print_info "取消卸载"
    fi
}

main "$@"

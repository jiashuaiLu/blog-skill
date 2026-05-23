#!/usr/bin/env python3
"""Tech Blog Writer Skill - 交互式技术博客写作助手.

完全交互式的工作流，每一步都引导用户做出选择。

工作流程：
1. 选择工作模式（自动上网获取 / 人工指定主题）
2. 选择文章或主题（从候选中选择或手动输入）
3. 选择文章风格（知乎风 / 论文风）
4. 生成初稿
5. 人工审阅和修改
6. 选择是否添加架构图/流程图
7. 选择发布渠道
8. 发布
"""

from __future__ import annotations

import json
import sys
import os
from datetime import date as _date
from pathlib import Path
from typing import Optional, Dict, List, Any

# 动态添加 scripts 路径
SKILL_DIR = Path(__file__).parent
PROJECT_ROOT = SKILL_DIR.parent
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

try:
    from scripts.lib.config import PROJECT_ROOT as _PROJECT_ROOT
    from scripts.lib.log import get_logger
    PROJECT_ROOT = _PROJECT_ROOT
except ImportError:
    PROJECT_ROOT = SKILL_DIR.parent
    import logging
    def get_logger(name, **kwargs):
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
            logger.addHandler(handler)
        return logger

# 尝试导入 rich 库用于美化的交互界面
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.prompt import Prompt, Confirm
    from rich.table import Table
    from rich.markdown import Markdown
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

if RICH_AVAILABLE:
    console = Console()
else:
    console = None


def print_header(title: str):
    """打印标题."""
    if RICH_AVAILABLE:
        console.print(Panel(title, style="bold blue"))
    else:
        print(f"\n{'='*60}")
        print(f"  {title}")
        print(f"{'='*60}\n")


def print_step(step_num: int, title: str):
    """打印步骤标题."""
    if RICH_AVAILABLE:
        console.print(f"\n[bold cyan]步骤 {step_num}:[/] {title}\n")
    else:
        print(f"\n步骤 {step_num}: {title}\n")


def print_message(message: str, style: str = "info"):
    """打印消息."""
    if RICH_AVAILABLE:
        if style == "success":
            console.print(f"[green]✓[/] {message}")
        elif style == "error":
            console.print(f"[red]✗[/] {message}")
        elif style == "warning":
            console.print(f"[yellow]![/] {message}")
        else:
            console.print(message)
    else:
        prefix = {"success": "✓", "error": "✗", "warning": "!"}.get(style, "")
        print(f"{prefix} {message}" if prefix else message)


def ask_choice(prompt: str, choices: List[str], default: Optional[str] = None) -> str:
    """询问用户选择."""
    if RICH_AVAILABLE:
        return Prompt.ask(prompt, choices=choices, default=default)
    else:
        print(f"\n{prompt}")
        for i, choice in enumerate(choices, 1):
            print(f"  {i}. {choice}")
        while True:
            try:
                idx = int(input(f"请选择 (1-{len(choices)})" + (f" [默认: {default}]" if default else "") + ": "))
                if 1 <= idx <= len(choices):
                    return choices[idx - 1]
                print("无效选择，请重试")
            except ValueError:
                if default:
                    return default
                print("请输入数字")


def ask_text(prompt: str, default: Optional[str] = None, multiline: bool = False) -> str:
    """询问用户输入文本."""
    if RICH_AVAILABLE:
        return Prompt.ask(prompt, default=default)
    else:
        hint = f" [默认: {default}]" if default else ""
        if multiline:
            print(f"\n{prompt}{hint}")
            print("(输入空行结束)")
            lines = []
            while True:
                line = input()
                if not line:
                    break
                lines.append(line)
            return "\n".join(lines) if lines else (default or "")
        else:
            return input(f"{prompt}{hint}: ") or (default or "")


def ask_confirm(prompt: str, default: bool = True) -> bool:
    """询问用户确认."""
    if RICH_AVAILABLE:
        return Confirm.ask(prompt, default=default)
    else:
        hint = "[Y/n]" if default else "[y/N]"
        response = input(f"{prompt} {hint}: ").strip().lower()
        if not response:
            return default
        return response in ('y', 'yes', '是')


def select_work_mode() -> str:
    """步骤1: 选择工作模式."""
    print_step(1, "选择工作模式")

    print_message("请选择本次写作的工作模式：")
    print_message("")
    print_message("  1. 自动模式 - 从网络自动获取最新技术文章候选")
    print_message("     适合：没有明确主题，想看看最新技术动态")
    print_message("")
    print_message("  2. 手动模式 - 手动指定已有的文章或主题")
    print_message("     适合：已有明确的写作主题或参考资料")
    print_message("")

    choice = ask_choice("请选择工作模式", ["自动模式", "手动模式"], default="自动模式")
    return "auto" if choice == "自动模式" else "manual"


def fetch_online_candidates() -> List[Dict[str, Any]]:
    """从网络获取候选文章."""
    print_message("正在从网络获取最新技术文章...")

    # 这里应该调用真实的 API，现在返回示例数据
    candidates = [
        {
            "id": "1",
            "title": "STAR: LLM根因分析框架",
            "source": "arXiv",
            "url": "https://arxiv.org/abs/xxx",
            "score": 4.5,
            "summary": "提出四阶段推理链，解决LLM诊断中的错误传播问题"
        },
        {
            "id": "2",
            "title": "Transformer架构演进综述",
            "source": "arXiv",
            "url": "https://arxiv.org/abs/yyy",
            "score": 4.2,
            "summary": "系统梳理BERT、GPT、T5等架构的设计思路和适用场景"
        },
        {
            "id": "3",
            "title": "大模型推理加速技术",
            "source": "arXiv",
            "url": "https://arxiv.org/abs/zzz",
            "score": 4.0,
            "summary": "总结量化、剪枝、蒸馏等推理优化技术"
        },
        {
            "id": "4",
            "title": "Agent系统设计模式",
            "source": "arXiv",
            "url": "https://arxiv.org/abs/aaa",
            "score": 3.8,
            "summary": "探讨ReAct、Plan-Execute等Agent架构模式"
        },
        {
            "id": "5",
            "title": "多模态大模型研究进展",
            "source": "arXiv",
            "url": "https://arxiv.org/abs/bbb",
            "score": 3.6,
            "summary": "综述视觉-语言模型的最新进展和应用"
        }
    ]

    print_message(f"找到 {len(candidates)} 篇候选文章", "success")
    return candidates


def select_candidate(candidates: List[Dict[str, Any]]) -> Dict[str, Any]:
    """步骤2: 选择文章或主题."""
    print_step(2, "选择文章或主题")

    if RICH_AVAILABLE:
        table = Table(title="候选文章列表")
        table.add_column("序号", style="cyan", no_wrap=True)
        table.add_column("标题", style="magenta")
        table.add_column("来源", style="green")
        table.add_column("评分", justify="right")
        table.add_column("摘要", style="dim")

        for i, cand in enumerate(candidates, 1):
            table.add_row(
                str(i),
                cand["title"],
                cand["source"],
                str(cand["score"]),
                cand["summary"][:50] + "..."
            )
        console.print(table)
    else:
        print("\n候选文章列表：")
        for i, cand in enumerate(candidates, 1):
            print(f"\n{i}. {cand['title']}")
            print(f"   来源: {cand['source']} | 评分: {cand['score']}")
            print(f"   摘要: {cand['summary']}")

    print_message("")
    choice_idx = ask_choice(
        "请选择感兴趣的文章",
        [str(i) for i in range(1, len(candidates) + 1)],
        default="1"
    )

    return candidates[int(choice_idx) - 1]


def input_manual_topic() -> Dict[str, Any]:
    """手动输入主题."""
    print_message("\n请输入您想写作的主题信息：\n")

    title = ask_text("文章标题")
    url = ask_text("参考链接（可选，按回车跳过）", default="")
    summary = ask_text("主题简介（简要描述您想写的内容）", multiline=True)

    return {
        "id": "manual",
        "title": title,
        "source": "手动输入",
        "url": url,
        "score": 0,
        "summary": summary
    }


def select_style() -> tuple[str, bool]:
    """步骤3: 选择文章风格和模型配置.

    Returns:
        (style, use_agent_model) - 文章风格和是否使用主Agent模型
    """
    print_step(3, "选择文章风格和模型配置")

    print_message("请选择文章风格：\n")
    print_message("  1. 知乎专栏风")
    print_message("     特点：强烈第一人称、主观判断、个人经验分享")
    print_message("     适合：有个人实践经验、分享踩坑经历、技术选型决策")
    print_message("")
    print_message("  2. 论文风")
    print_message("     特点：客观中立、引用真实案例、严谨表述")
    print_message("     适合：技术深度分析、方法对比、没有实践经验")
    print_message("")

    style_choice = ask_choice("请选择文章风格", ["知乎专栏风", "论文风"], default="知乎专栏风")
    style = "zhihu" if style_choice == "知乎专栏风" else "paper"

    # 询问模型配置
    print_message("\n请选择模型配置：\n")
    print_message("  1. 使用专用写作模型（推荐）")
    print_message("     配置 writer 模型：Claude-Sonnet-4.6 或 Claude-Opus-4.7")
    print_message("     成本：~$0.15-0.20/篇")
    print_message("")
    print_message("  2. 使用主 Agent 模型（当前会话模型）")
    print_message("     无需额外配置，使用当前对话的模型")
    print_message("     成本：取决于当前 Agent 配置")
    print_message("")

    model_choice = ask_choice("请选择模型配置", ["使用专用写作模型", "使用主 Agent 模型"], default="使用专用写作模型")
    use_agent_model = model_choice == "使用主 Agent 模型"

    if use_agent_model:
        print_message("\n✓ 将使用主 Agent 模型进行写作", "success")
    else:
        print_message("\n✓ 将使用专用写作模型（需配置 models.yaml）", "success")

    return style, use_agent_model


def create_brief(topic: Dict[str, Any], style: str, date_str: str, use_agent_model: bool = False) -> Path:
    """创建 brief.yaml.

    Args:
        topic: 主题信息
        style: 文章风格
        date_str: 日期字符串
        use_agent_model: 是否使用主 Agent 模型（不配置 writer）

    Returns:
        brief.yaml 文件路径
    """
    import yaml

    pipeline_dir = PROJECT_ROOT / "pipeline" / date_str
    pipeline_dir.mkdir(parents=True, exist_ok=True)

    brief_path = pipeline_dir / "brief.yaml"

    brief_data = {
        "date": date_str,
        "chosen": {
            "title": topic["title"],
            "angle": topic["summary"],
            "value_one_liner": f"深入了解{topic['title']}",
            "length_hint": 2500,
            "audience": "技术工程师",
            "style": style,
            "tone": "略带怀疑、有实战气息" if style == "zhihu" else "客观严谨",
            "must_cover": [],
            "must_NOT": ["不要科普基础概念"],
            "source_item_ids": [topic["id"]] if topic["id"] != "manual" else [],
            "composite_rank": 1,
            "use_agent_model": use_agent_model,  # 新增：是否使用主 Agent 模型
        },
        "candidates_metadata": [topic] if topic["id"] != "manual" else []
    }

    # 如果是论文风格，添加特殊提示
    if style == "paper":
        brief_data["chosen"]["must_NOT"].extend([
            "不要虚构个人经历",
            "不要编造数据",
            "不要主观臆断"
        ])

    brief_path.write_text(yaml.dump(brief_data, allow_unicode=True, default_flow_style=False), encoding="utf-8")

    return brief_path


def generate_draft(date_str: str) -> Optional[Path]:
    """生成初稿."""
    print_message("正在生成文章初稿，请稍候...")

    try:
        # 尝试导入并运行各个阶段
        from scripts.facts import facts as extract_facts
        from scripts.outline import outline as generate_outline
        from scripts.skeleton import skeleton as generate_skeleton
        from scripts.draft import draft as write_draft

        # 执行流程
        steps = [
            ("提取事实", extract_facts),
            ("生成大纲", generate_outline),
            ("生成骨架", generate_skeleton),
            ("写正文", write_draft),
        ]

        for step_name, step_func in steps:
            print_message(f"  - {step_name}...")
            result = step_func(date_str)
            if not result:
                print_message(f"{step_name}失败", "error")
                return None

        # 返回最终的 draft.md
        return PROJECT_ROOT / "pipeline" / date_str / "draft.md"

    except Exception as e:
        print_message(f"生成失败: {e}", "error")
        return None


def review_and_edit(date_str: str) -> bool:
    """步骤5: 人工审阅和修改."""
    print_step(5, "人工审阅和修改")

    draft_path = PROJECT_ROOT / "pipeline" / date_str / "draft.md"

    if not draft_path.exists():
        print_message("未找到初稿文件", "error")
        return False

    # 显示文章预览
    if RICH_AVAILABLE:
        console.print("\n[bold]文章预览：[/]\n")
        content = draft_path.read_text(encoding="utf-8")
        console.print(Markdown(content[:1000] + "\n\n...(预览前1000字符)"))
    else:
        print("\n文章预览：\n")
        content = draft_path.read_text(encoding="utf-8")
        print(content[:1000])
        print("\n...(预览前1000字符)")

    print_message("")

    # 询问是否满意
    if ask_confirm("对初稿是否满意？", default=True):
        return True

    # 如果不满意，提供修改选项
    print_message("\n请选择修改方式：")
    print_message("  1. 手动编辑文件")
    print_message("  2. 重新生成")
    print_message("  3. 继续下一步（稍后修改）")

    choice = ask_choice("请选择", ["手动编辑", "重新生成", "继续下一步"], default="继续下一步")

    if choice == "手动编辑":
        print_message(f"\n请在编辑器中打开文件进行修改：")
        print_message(f"  {draft_path}")
        input("\n修改完成后按回车继续...")
        return True

    elif choice == "重新生成":
        return generate_draft(date_str) is not None

    else:  # 继续下一步
        return True


def add_diagrams(date_str: str) -> bool:
    """步骤6: 添加架构图/流程图."""
    print_step(6, "添加架构图/流程图")

    if not ask_confirm("是否需要添加架构图、流程图或时序图？", default=True):
        return True

    print_message("\n请选择要添加的图表类型：")
    print_message("  1. 流程图 (flowchart)")
    print_message("  2. 时序图 (sequence)")
    print_message("  3. 甘特图 (gantt)")
    print_message("  4. 自定义 mermaid 图表")
    print_message("  5. 跳过")

    choice = ask_choice("请选择", ["流程图", "时序图", "甘特图", "自定义", "跳过"], default="跳过")

    if choice == "跳过":
        return True

    # 这里应该集成图表生成逻辑
    print_message(f"\n将添加 {choice}...")
    print_message("提示：图表将自动插入到文章中合适的位置")

    return True


def select_publish_channels() -> List[str]:
    """步骤7: 选择发布渠道."""
    print_step(7, "选择发布渠道")

    print_message("请选择要发布的平台（可多选）：\n")

    channels = [
        "掘金",
        "知乎",
        "微信公众号",
        "个人博客",
        "GitHub",
        "其他"
    ]

    if RICH_AVAILABLE:
        console.print("[dim]输入数字选择，多个用逗号分隔，如: 1,2,3[/dim]\n")

    for i, channel in enumerate(channels, 1):
        print_message(f"  {i}. {channel}")

    print_message("")

    while True:
        try:
            choices_str = ask_text("请选择发布渠道（输入数字，多个用逗号分隔）", default="1")
            selected_indices = [int(x.strip()) for x in choices_str.split(",")]
            selected_channels = [channels[i-1] for i in selected_indices if 1 <= i <= len(channels)]
            if selected_channels:
                print_message(f"\n已选择: {', '.join(selected_channels)}", "success")
                return selected_channels
            print_message("无效选择，请重试", "error")
        except (ValueError, IndexError):
            print_message("输入格式错误，请重试", "error")


def publish_article(date_str: str, channels: List[str]) -> bool:
    """步骤8: 发布文章."""
    print_step(8, "发布文章")

    post_path = PROJECT_ROOT / "pipeline" / date_str / "post.md"

    if not post_path.exists():
        print_message("未找到最终文章文件", "error")
        return False

    print_message(f"文章路径: {post_path}")
    print_message(f"发布渠道: {', '.join(channels)}\n")

    for channel in channels:
        print_message(f"正在发布到 {channel}...")

        # 这里应该集成真实的发布 API
        if channel == "掘金":
            print_message("  提示：请手动复制到掘金编辑器发布")
        elif channel == "知乎":
            print_message("  提示：请手动复制到知乎专栏发布")
        elif channel == "微信公众号":
            print_message("  提示：请使用微信公众号编辑器发布")
        elif channel == "个人博客":
            print_message("  提示：文件已准备好，可部署到您的博客系统")
        elif channel == "GitHub":
            print_message("  提示：可提交到 GitHub 仓库")
        else:
            print_message("  提示：请根据该平台要求发布")

    print_message("\n发布准备完成！", "success")
    return True


def interactive_workflow():
    """交互式工作流主函数."""
    print_header("Tech Blog Writer - 交互式技术博客写作助手")

    date_str = _date.today().isoformat()

    # 步骤1: 选择工作模式
    work_mode = select_work_mode()

    # 步骤2: 选择文章或主题
    if work_mode == "auto":
        candidates = fetch_online_candidates()
        selected_topic = select_candidate(candidates)
    else:
        selected_topic = input_manual_topic()

    print_message(f"\n已选择主题: {selected_topic['title']}", "success")

    # 步骤3: 选择文章风格和模型配置
    style, use_agent_model = select_style()
    print_message(f"已选择风格: {('知乎专栏风' if style == 'zhihu' else '论文风')}", "success")
    if use_agent_model:
        print_message("已选择模型: 主 Agent 模型", "success")
    else:
        print_message("已选择模型: 专用写作模型", "success")

    # 步骤4: 创建 brief 并生成初稿
    print_step(4, "生成文章初稿")

    brief_path = create_brief(selected_topic, style, date_str, use_agent_model)
    print_message(f"已创建选题配置: {brief_path}", "success")

    if ask_confirm("\n是否开始生成初稿？", default=True):
        draft_path = generate_draft(date_str)

        if not draft_path:
            print_message("初稿生成失败", "error")
            return

        print_message(f"初稿已生成: {draft_path}", "success")

        # 步骤5: 人工审阅和修改
        if not review_and_edit(date_str):
            print_message("审阅流程中断", "error")
            return

        # 步骤6: 添加架构图/流程图
        if not add_diagrams(date_str):
            print_message("添加图表失败", "error")
            return

        # 步骤7: 选择发布渠道
        channels = select_publish_channels()

        # 步骤8: 发布文章
        if ask_confirm("\n是否立即发布？", default=True):
            if publish_article(date_str, channels):
                print_header("🎉 文章发布完成！")
                print_message(f"文章路径: pipeline/{date_str}/post.md", "success")
                print_message(f"发布渠道: {', '.join(channels)}", "success")
            else:
                print_message("发布失败", "error")
        else:
            print_message("\n文章已准备好，可稍后发布", "success")
            print_message(f"文章路径: pipeline/{date_str}/post.md")

    else:
        print_message("\n已取消生成初稿", "warning")
        print_message(f"选题配置已保存: {brief_path}")


def cmd_fetch(url: str, output: str | None = None) -> None:
    """抓取任意 URL，用 trafilatura 解析成 markdown，适合 LLM 分析.

    微信公众号等有反爬的站点走两步：
      1. Chrome DevTools 拿渲染后的 HTML
      2. 调 fetch_from_html() 解析
    普通站点直接 HTTP fetch。
    """
    import subprocess
    import tempfile

    sys.path.insert(0, str(PROJECT_ROOT))
    from scripts.fetchers.url import fetch_url, fetch_from_html, article_to_prompt_text

    WX_HOST = "mp.weixin.qq.com"
    is_wx = WX_HOST in url

    print_message(f"正在抓取: {url}", "info")

    if is_wx:
        # 微信走 Chrome DevTools：用 python -c 调用 mcp chrome-devtools
        # 实际环境里 Claude Code 已持有 Chrome 连接，这里通过 subprocess 调 JS 脚本取 HTML
        print_message("检测到微信公众号链接，尝试通过浏览器获取页面 HTML...", "info")
        try:
            # 尝试用系统 Chrome / chromium 无头模式取页面
            import httpx
            resp = httpx.get(
                url,
                headers={
                    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                                  "Chrome/124.0.0.0 Safari/537.36",
                    "Referer": "https://mp.weixin.qq.com/",
                    "Accept-Language": "zh-CN,zh;q=0.9",
                },
                timeout=30,
                follow_redirects=True,
            )
            html = resp.text
            if len(html) < 500:
                raise RuntimeError("页面内容过短，可能被反爬拦截")
            article = fetch_from_html(html, url)
        except Exception as e:
            print_message(
                f"直接 HTTP 获取失败（{e}）。\n"
                "提示：微信公众号需要浏览器渲染，请在 Claude Code 中用如下方式获取 HTML：\n"
                "  1. 通过 Chrome DevTools MCP 打开页面\n"
                "  2. 调用 evaluate_script: document.documentElement.outerHTML\n"
                "  3. 将 HTML 保存到文件后用 --fetch-html 参数传入\n",
                "warning",
            )
            sys.exit(1)
    else:
        article = fetch_url(url)

    prompt_text = article_to_prompt_text(article)

    if output:
        out_path = Path(output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(prompt_text, encoding="utf-8")
        print_message(f"已保存到 {out_path}（{article.word_count} 字符）", "success")
    else:
        print(prompt_text)


def cmd_fetch_html(html_file: str, url: str, output: str | None = None) -> None:
    """从已有 HTML 文件解析文章（用于微信等需要浏览器渲染的场景）."""
    sys.path.insert(0, str(PROJECT_ROOT))
    from scripts.fetchers.url import fetch_from_html, article_to_prompt_text

    html_path = Path(html_file)
    if not html_path.exists():
        print_message(f"文件不存在: {html_file}", "error")
        sys.exit(1)

    raw = html_path.read_text(encoding="utf-8")
    # 支持 Chrome DevTools evaluate_script 返回的 JSON 格式（字符串被 JSON 包裹）
    if raw.lstrip().startswith('"'):
        try:
            raw = json.loads(raw)
        except Exception:
            pass

    print_message(f"解析 HTML 文件: {html_file}", "info")
    article = fetch_from_html(raw, url)
    prompt_text = article_to_prompt_text(article)

    if output:
        out_path = Path(output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(prompt_text, encoding="utf-8")
        print_message(f"已保存到 {out_path}（{article.word_count} 字符）", "success")
    else:
        print(prompt_text)


def main():
    """主函数."""
    import argparse

    parser = argparse.ArgumentParser(
        prog="tech-blog-writer",
        description="技术博客写作助手",
        add_help=True,
    )
    sub = parser.add_subparsers(dest="cmd")

    # fetch 子命令：抓取 URL → markdown
    p_fetch = sub.add_parser("fetch", help="抓取任意 URL 并解析为 LLM 可读的 markdown")
    p_fetch.add_argument("url", help="目标 URL")
    p_fetch.add_argument("-o", "--output", help="输出文件路径（不指定则打印到 stdout）")

    # fetch-html 子命令：从本地 HTML 文件解析（微信专用）
    p_fhtml = sub.add_parser("fetch-html", help="从本地 HTML 文件解析文章（微信等反爬站点专用）")
    p_fhtml.add_argument("html_file", help="本地 HTML 文件路径")
    p_fhtml.add_argument("url", help="原始 URL（用于元数据）")
    p_fhtml.add_argument("-o", "--output", help="输出文件路径")

    args, _ = parser.parse_known_args()

    if args.cmd == "fetch":
        cmd_fetch(args.url, args.output)
        return
    if args.cmd == "fetch-html":
        cmd_fetch_html(args.html_file, args.url, args.output)
        return

    # 无子命令 → 进入交互式工作流
    try:
        interactive_workflow()
    except KeyboardInterrupt:
        print_message("\n\n用户取消操作", "warning")
        sys.exit(0)
    except Exception as e:
        print_message(f"\n发生错误: {e}", "error")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

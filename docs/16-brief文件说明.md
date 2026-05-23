# brief.yaml 文件说明

## 文件位置

```
pipeline/{日期}/brief.yaml
```

例如：
```
pipeline/2026-05-19/brief.yaml
```

## 文件作用

`brief.yaml` 是文章的**选题确认文件**，包含了文章的所有关键设定。它是整个写作流水线的起点。

## 完整字段说明

### 基础字段

```yaml
date: '2026-05-19'  # 文章日期
```

### chosen 字段（核心配置）

```yaml
chosen:
  # 文章标题
  title: 微服务AIOps：LLM根因分析实战

  # 文章角度（重要！这是文章的灵魂）
  angle: |
    从STAR框架出发，拆解LLM在微服务故障诊断中的工程落地细节

  # 一句话价值主张
  value_one_liner: 掌握LLM根因分析的可信工程方案

  # 目标字数
  length_hint: 2500

  # 目标受众
  audience: 后端工程师

  # 文章风格（新增字段）
  style: zhihu  # 可选：zhihu（默认）或 paper

  # 文章语气
  tone: 略带怀疑、有实战气息、可以吐槽

  # 必须覆盖的内容
  must_cover:
    - paper 的核心实验设置
    - 它否证了什么常见假设
    - 我自己在生产里的对照
    - 什么场景反思仍然有效

  # 绝对不要写的内容
  must_NOT:
    - 不要写"什么是 Agent"这种科普段落
    - 不要罗列所有相关 paper

  # 来源文章ID
  source_item_ids:
    - cbb5bcd3

  # 综合排名
  composite_rank: 1
```

### candidates_metadata 字段（候选列表）

这是从打分阶段来的候选文章列表，供你选择：

```yaml
candidates_metadata:
  - id: cbb5bcd367bce753a1bf4a8490bde9a3ac28fa6b
    title: 'STAR: A Stage-attributed Triage and Repair framework...'
    source: arxiv_csai
    url: https://arxiv.org/abs/2605.15581
    days_old: 0.9
    composite: 4.132
    coarse_score: 5.0
  - id: d816035fdd7ad2e764ccffe395e7bea1d265b03d
    title: 'PRISM: Prompt Reliability via Iterative Simulation...'
    # ... 更多候选
```

## 字段详解

### 1. `angle` - 文章角度（最重要）

这是文章的灵魂，决定了文章的视角和深度。

**知乎风格示例**：
```yaml
angle: |
  最近我在做一个客服 Agent，加了自我反思层之后延迟翻倍但效果只涨 2%。
  这篇 paper 系统拆了这件事，结论和我的体感一致。我想从工程视角讲讲什么时候该用。
```

**论文风格示例**：
```yaml
angle: |
  综述 Transformer 架构的发展历程，对比主流变体（BERT、GPT、T5等）的
  设计思路和适用场景，引用真实落地案例说明实际应用效果。
```

### 2. `style` - 文章风格（新增字段）

用于选择文章风格：

| 值 | 说明 | 特点 |
|----|------|------|
| `zhihu` | 知乎专栏风（默认） | 强烈第一人称、主观判断、个人经验分享 |
| `paper` | 论文风 | 客观中立、引用真实案例、严谨表述 |

**使用场景**：
- 有个人经验 → 用 `zhihu`
- 纯技术分析/没有做过 → 用 `paper`

### 3. `must_cover` - 必须覆盖的内容

列出文章必须提到的关键点，确保不遗漏重要内容。

```yaml
must_cover:
  - STAR框架的四阶段设计
  - 阶段审计的具体实现
  - Fast/Slow Routing机制
  - 真实案例的修复效果
```

### 4. `must_NOT` - 绝对不要写的内容

明确禁止的内容，避免文章跑偏。

```yaml
must_NOT:
  - 不要写"什么是 RCA"这种科普段落
  - 不要罗列所有相关 paper
  - 不要虚构个人实验数据
```

## 如何创建 brief.yaml

### 方法1：手动创建

1. 查看 `candidates.yaml`（如果存在）或候选文章列表
2. 选择一个 S/A 级选题
3. 创建 `pipeline/{日期}/brief.yaml`
4. 填写必要字段

### 方法2：从模板创建

**知乎风格模板**：

```yaml
date: '2026-05-19'
chosen:
  title: "文章标题"
  angle: |
    我最近遇到了一个具体问题...
    这篇 paper 的方法解决了我的困惑...
  value_one_liner: "一句话价值主张"
  length_hint: 2500
  audience: "后端工程师"
  style: zhihu
  tone: "略带怀疑、有实战气息"
  must_cover:
    - paper 的核心方法
    - 我在实践中的对照
    - 具体的建议
  must_NOT:
    - 不要科普
    - 不要罗列论文
```

**论文风格模板**：

```yaml
date: '2026-05-19'
chosen:
  title: "技术深度分析标题"
  angle: |
    综述 X 技术的发展历程，对比主流方案的优劣，
    引用真实落地案例说明实际应用效果。
  value_one_liner: "系统梳理 X 技术，帮助读者理解不同方案的取舍"
  length_hint: 2500
  audience: "有一定基础的工程师和研究人员"
  style: paper  # 关键：使用论文风格
  tone: "客观严谨"
  must_cover:
    - 技术原理
    - 方案对比
    - 真实案例（至少3个）
    - 适用场景
  must_NOT:
    - 不要虚构个人经历
    - 不要编造数据
    - 不要主观臆断
```

## 工作流中的位置

```mermaid
flowchart LR
    A[candidates.yaml] --> B[人工选择选题]
    B --> C[创建 brief.yaml]
    C --> D[facts.py<br/>提取事实]
    D --> E[outline.py<br/>生成大纲]
    E --> F[draft.py<br/>写正文]
    F --> G[最终文章]
```

## 常见问题

### Q1: brief.yaml 在哪个目录？

**A**: 在 `pipeline/{日期}/brief.yaml`

例如：`pipeline/2026-05-19/brief.yaml`

### Q2: style 字段必须填吗？

**A**: 不是必须的。默认是 `zhihu` 风格。

```yaml
chosen:
  style: paper  # 如果不填，默认是 zhihu
```

### Q3: angle 字段写多长？

**A**: 建议 100-200 字，清晰说明文章的角度和核心价值。

### Q4: 必须有 source_item_ids 吗？

**A**: 不是必须的，但建议填写，方便追溯来源。

## 示例对比

### 知乎风格示例

```yaml
chosen:
  title: "Agent 自我反思真的有用吗？看这篇拆得最狠的复盘"
  angle: |
    最近我在做一个客服 Agent，加了自我反思层之后延迟翻倍但效果只涨 2%。
    这篇 paper 系统拆了这件事，结论和我的体感一致。我想从工程视角讲讲什么时候该用。
  style: zhihu
  audience: "做过 Agent 工程的同行"
  tone: "略带怀疑、有实战气息、可以吐槽"
```

### 论文风格示例

```yaml
chosen:
  title: "Transformer架构演进：从原理到实践"
  angle: |
    综述 Transformer 架构的发展历程，对比主流变体（BERT、GPT、T5等）的
    设计思路和适用场景，引用真实落地案例说明实际应用效果。
  style: paper  # 关键区别
  audience: "有一定 NLP 基础的工程师和研究人员"
  tone: "客观严谨"
```

## 验证方法

创建 brief.yaml 后，运行下一阶段：

```bash
# 提取事实
python scripts/facts.py

# 生成大纲
python scripts/outline.py

# 写正文
python scripts/draft.py
```

或者一次性运行：

```bash
python scripts/cli.py run 2026-05-19
```

# ResumeTailor Agent

JD-driven, evidence-based resume tailoring workflow for AI application and job search scenarios.

面向岗位 JD 的简历定制实验项目。它不是“把 JD 丢给大模型润色一下”的 Prompt Demo，而是一条更可解释、更适合做项目展示的本地 AI 工作流：

`JD 解析 -> 查询计划 -> 素材切块 -> 证据检索 -> 证据排序 -> 简历生成 -> 面试追问 -> 缺口分析 -> 风险审查 -> Markdown/JSON 导出`

这个项目的核心目标是：基于真实经历素材，生成更贴岗、可追溯、风险更低的简历表达结果，并且把中间链路展示出来，方便做求职项目包装、面试讲解和后续迭代。

## Why It Stands Out

- `JD-driven`: 先解析岗位需求，而不是直接做文案润色
- `Evidence-based`: 先从素材库检索证据，再组织简历表达
- `Workflow-first`: 拆成 parser / planner / retriever / writer / reviewer 等清晰节点
- `Demo-friendly`: 同时提供 `CLI + Streamlit + evaluation`，便于演示、复盘和迭代
- `Risk-aware`: 输出后还有缺口分析和风险审查，不是只追求“生成得像”

## 项目亮点

- 不是纯文案润色，而是 `JD 驱动 + 证据支撑 + 约束生成` 的 AI 应用流程
- 有完整节点拆分，链路清晰，适合讲成一个可解释的 Agent / Workflow 项目
- 检索前显式构建 `Query Plan`，把关键词、扩展词和检索意图结构化
- 支持 `CLI + Streamlit` 双入口，既能自动跑，也能可视化展示中间结果
- 默认可本地运行，不依赖外部模型；有 OpenAI 兼容接口时可开启 LLM 增强
- 不是只输出简历文案，还覆盖 `面试追问`、`素材缺口分析`、`多 JD 对比`、`质量评估`
- 生成环节和审查环节都有“证据约束”意识，减少无依据夸大

## 这个项目解决什么问题

常见的“AI 改简历”工具有两个问题：

- 输出看起来更像润色，而不是基于岗位需求做针对性重组
- 容易写出没有证据支撑的表述，面试时经不起追问

这个项目的思路是先把 JD 拆成结构化需求，再从本地素材里找可复用证据，然后基于证据生成简历摘要与项目亮点，最后补一层风险审查和缺口提示。这样最终结果不只是“更像简历”，而是更接近“可讲、可解释、可回溯”的求职材料。

## 当前能力

- JD 解析：抽取岗位标题、关键词、必须项、加分项、目标层级
- 查询计划：生成 `query_tokens`、`expanded_terms`、`query_text`
- 素材加载：支持 `Markdown`、`TXT`、`JSON`
- 段落级切块：把素材按段落切成独立证据块参与检索
- 轻量混合检索：关键词命中 + token overlap + 本地 embedding 相似度
- 证据排序：保留命中原因和分数，方便解释为什么命中
- 简历输出：生成项目亮点、技能摘要、自我介绍、匹配依据
- 面试追问：基于命中的项目亮点自动生成 follow-up questions
- 缺口分析：识别已覆盖关键词、缺失关键词、薄弱要求和补强建议
- 风险审查：检测潜在无依据表述，并可叠加模型复核
- 多 JD 对比：同时运行多个 JD，并输出关键词差异、主命中项目和风险等级
- 结果评估：可批量跑 case，输出召回、命中、风险和综合得分

## 技术路线

### 1. Rule-first，本地可跑

默认模式不依赖外部模型，主要依靠：

- 规则关键词识别
- 查询词扩展
- 段落切块
- 轻量 hybrid 检索
- 模板化结果组织
- 风险规则扫描

这让项目具备两个优点：

- 演示稳定，离线也能跑
- 适合在面试里说明“没有把效果全压给 LLM”

### 2. 可选 LLM 增强，但要受约束

配置 OpenAI 兼容接口后，系统会：

- 对规则版简历结果做二次增强
- 对审查结果增加模型复核
- 对模型输出做受约束合并，只接受与证据有交集的内容
- 在模型失败时自动回退到规则模式

也就是说，这里不是“直接相信模型”，而是“先有规则底稿，再用模型在边界内优化”。

## 工作流说明

完整链路如下：

1. `JD Parser`
   从 JD 文本中识别岗位标题、关键词、must-have、nice-to-have、目标层级。
2. `Query Planner`
   把关键词和要求转成检索计划，并做同义词扩展，比如 `自动化 -> automation / workflow`。
3. `Materials Loader`
   读取本地素材目录，支持 `md/txt/json`，并按段落切块。
4. `Retriever`
   根据关键词命中、token overlap、局部向量相似度做轻量混合检索。
5. `Evidence Ranker`
   对候选证据进一步排序，保留命中理由。
6. `Resume Writer`
   基于命中证据生成项目亮点、技能摘要、自我介绍和匹配依据。
7. `LLM Enhancer`
   如果配置了接口，对规则版输出做受约束增强。
8. `Interview Generator`
   根据命中的项目亮点自动生成面试追问。
9. `Gap Analyzer`
   分析哪些关键词已覆盖、哪些仍缺失，以及补强建议。
10. `Reviewer`
    对结果做风险审查，识别潜在无证据支撑的表述。
11. `Exporter`
    导出 Markdown 报告和 JSON 运行日志，便于复盘和展示。

## 适合怎么讲这个项目

如果这个项目是用来写简历、做面试展示，推荐这样定义它：

- `面向求职场景的 JD 驱动简历定制 Agent`
- `基于真实证据检索的 Resume Tailoring Workflow`
- `JD 解析 + 检索增强 + 约束生成 + 风险校验` 的 AI 应用实验

更适合强调的不是“模型多强”，而是：

- 你把一个模糊任务拆成了可执行工作流
- 你考虑了证据链、可解释性和风险控制
- 你做了 UI、CLI、评估和对比功能，项目更完整

## 项目结构

```text
岗位JD-RAG/
├── resumetailor_agent/
│   ├── __main__.py
│   ├── cli.py
│   ├── config.py
│   ├── embedding.py
│   ├── evaluator.py
│   ├── exporter.py
│   ├── llm.py
│   ├── materials.py
│   ├── schemas.py
│   ├── ui_helpers.py
│   ├── workflow.py
│   └── nodes/
│       ├── jd_parser.py
│       ├── query_planner.py
│       ├── retriever.py
│       ├── evidence_ranker.py
│       ├── resume_writer.py
│       ├── interview_generator.py
│       ├── gap_analyzer.py
│       └── reviewer.py
├── sample_inputs/
├── sample_materials/
├── outputs/
├── tests/
├── streamlit_app.py
├── requirements.txt
└── README.md
```

## 模块职责

- `resumetailor_agent/cli.py`
  命令行入口，支持单 JD、JD 对比、评估三种模式。
- `resumetailor_agent/workflow.py`
  主编排层，把 parser、retriever、writer、reviewer 等节点串起来。
- `resumetailor_agent/materials.py`
  读取本地素材并按段落切块。
- `resumetailor_agent/llm.py`
  负责 OpenAI 兼容接口调用、增强输出、模型审查和失败回退。
- `resumetailor_agent/evaluator.py`
  负责批量 case 评估和统计汇总。
- `resumetailor_agent/exporter.py`
  导出 Markdown 报告、JSON 日志、对比报告、评估报告。
- `streamlit_app.py`
  可视化演示入口，适合录屏、汇报和现场展示。

## 运行环境

- Python `3.11+` 推荐
- 依赖非常轻量：
  - `pydantic`
  - `streamlit`
  - `pytest`

安装依赖：

```bash
python3.11 -m pip install -r requirements.txt
```

如果你本机不是 `python3.11`，把命令替换成自己的 Python 解释器即可。

## 快速开始

### 1. 准备素材目录

把项目经历、学习笔记、自我介绍草稿、实验记录等放在一个目录里，推荐用 `Markdown`。系统会读取所有 `md/txt/json` 文件，并把每个文件按段落切成证据块。

示例素材：

```md
# GitHub Agent Daily

Built a Python Agent automation workflow for GitHub trending reports.

Implemented markdown export and evidence organization.
```

项目里已经提供了示例素材目录：

```text
sample_materials/
```

### 2. 启动 Streamlit 界面

```bash
python3.11 -m streamlit run streamlit_app.py
```

适合演示的内容包括：

- JD 解析结果
- 查询计划
- 命中证据和命中原因
- 简历输出
- 面试追问
- 缺口分析
- 风险检查
- 多 JD 对比

多 JD 输入格式示例：

```text
AI应用::AI应用实习生，要求 Python、Agent、自动化项目经验。
---
演示岗::AI应用实习生，要求 Streamlit、Python 项目经验。
```

### 3. 运行单 JD 模式

```bash
python3.11 -m resumetailor_agent.cli \
  --jd-file sample_inputs/ai_application_intern_jd.md \
  --materials-dir sample_materials \
  --output-dir outputs \
  --run-id demo-cli
```

也可以直接传文本：

```bash
python3.11 -m resumetailor_agent.cli \
  --jd-text "AI应用实习生，要求 Python、Agent、自动化项目经验。" \
  --materials-dir sample_materials \
  --output-dir outputs \
  --run-id demo-text
```

执行后会打印 Markdown 报告路径，并生成同名 JSON 运行日志。

### 4. 运行多 JD 对比模式

```bash
python3.11 -m resumetailor_agent.cli \
  --compare-jd-files sample_inputs/ai_application_intern_jd.md sample_inputs/ai_application_intern_jd.md \
  --materials-dir sample_materials \
  --output-dir outputs \
  --run-id compare-demo
```

这个模式会生成：

- 每个 JD 各自的单独报告
- 一个汇总对比报告：`outputs/compare-demo-comparison.md`

对比报告会展示：

- 共同关键词
- 每个 JD 的差异关键词
- 每个 JD 的主命中项目
- 每个 JD 的缺失关键词
- 每个 JD 的风险等级

### 5. 运行质量评估模式

```bash
python3.11 -m resumetailor_agent.cli \
  --eval-cases-file sample_inputs/eval_cases.json \
  --output-dir outputs \
  --run-id quality-eval
```

评估模式会批量运行 case，并生成：

- `outputs/quality-eval-evaluation.md`
- `outputs/quality-eval-evaluation.json`
- 每个 case 单独的运行报告

评估汇总指标包括：

- `keyword_recall`
- `project_hit`
- `evidence_presence`
- `risk_score`
- `overall_score`

## OpenAI 兼容接口配置

如果你希望启用 LLM 增强，可以通过参数或环境变量配置：

环境变量：

```bash
export OPENAI_API_KEY="your_key"
export OPENAI_BASE_URL="https://api.openai.com/v1"
export OPENAI_MODEL="gpt-4o-mini"
```

命令行参数：

```bash
python3.11 -m resumetailor_agent.cli \
  --jd-file sample_inputs/ai_application_intern_jd.md \
  --materials-dir sample_materials \
  --output-dir outputs \
  --run-id demo-llm \
  --openai-api-key "$OPENAI_API_KEY" \
  --openai-base-url "$OPENAI_BASE_URL" \
  --openai-model "$OPENAI_MODEL"
```

说明：

- CLI 参数会覆盖环境变量
- 同时提供 `API Key + Model` 时，系统才会进入 LLM 模式
- 未配置或请求失败时，会自动回退到规则模式

## 输出内容说明

### 单 JD 模式输出

默认生成两类文件：

- `outputs/<run-id>.md`
- `outputs/<run-id>.json`

Markdown 报告包含：

1. JD 解析摘要
2. 查询计划
3. 命中经历证据
4. 定制化项目描述
5. 技能描述优化建议
6. 自我介绍摘要
7. 匹配依据
8. 面试高频追问
9. 素材缺口分析
10. 风险提示与建议

JSON 日志则保存完整运行上下文，适合调试、回放和后续评估。

### 多 JD 模式输出

- `outputs/<run-id>-comparison.md`
- 每个 JD 单独的 Markdown/JSON 报告

### 评估模式输出

- `outputs/<run-id>-evaluation.md`
- `outputs/<run-id>-evaluation.json`

## CLI 参数一览

- `--jd-text`
  直接传入 JD 文本。
- `--jd-file`
  从文件读取单个 JD。
- `--compare-jd-files`
  传入多个 JD 文件，进入对比模式。
- `--eval-cases-file`
  传入评估 case JSON 文件，进入评估模式。
- `--materials-dir`
  素材目录，默认是 `sample_materials`。
- `--output-dir`
  报告输出目录，默认是 `outputs`。
- `--run-id`
  输出文件名前缀，默认是 `cli-run`。
- `--openai-api-key`
  可选的 OpenAI 兼容 Key。
- `--openai-base-url`
  可选的 OpenAI 兼容 Base URL。
- `--openai-model`
  可选的模型名。

查看帮助：

```bash
python3.11 -m resumetailor_agent.cli --help
```

## 示例数据

仓库内置了几类演示数据：

- `sample_inputs/`
  单 JD 与评估输入样例。
- `sample_materials/`
  模拟候选人的项目与背景素材。
- `outputs/`
  已生成的示例结果，适合直接查看产出格式。

如果你要做项目展示，建议保留这些示例输出，方便别人快速感知系统结果长什么样。

## 测试

运行测试：

```bash
python3.11 -m pytest -q
```

当前仓库实测结果：

- `43 passed`

## 项目边界

这个项目当前更适合定位为“本地单用户 AI 工作流实验”，边界也需要讲清楚：

- 检索器是轻量 hybrid 检索，不是生产级向量数据库系统
- JD 解析主要是规则与关键词模式，不是复杂的信息抽取模型
- 简历生成默认是规则输出，LLM 只是可选增强层
- 目前更强调可解释性和项目展示，不是成熟商业产品
- 当前没有用户系统、权限系统、在线部署和多租户能力

## 为什么这个项目适合做简历项目包装

它比单纯的“调用大模型 API 做个网页”更有讲述空间，因为你可以自然展开这些点：

- 为什么要先做 JD 解析，而不是直接生成
- 为什么要显式做 Query Planning
- 为什么要按段落切块，而不是整篇素材一起喂模型
- 为什么要把证据命中理由展示出来
- 为什么需要缺口分析和风险审查
- 为什么要同时提供 CLI、UI 和评估模式

这会让项目从“会调接口”升级成“能设计一个完整 AI 应用流程”。

## 后续可扩展方向

- 接入更强的 embedding 和向量库
- 提升 JD 结构化解析粒度
- 增加更细的证据评分与 rerank 逻辑
- 把 gap suggestion 和具体补强任务连接起来
- 增加更多评估 case 和自动化回归基线
- 为 Streamlit 增加更强的结果对比与可视化面板
- 增加导出为面试讲稿、项目卡片、STAR 素材的能力

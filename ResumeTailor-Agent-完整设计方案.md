# AI Resume Experiment Platform：面向岗位定制与结果评估的 AI Workflow 实验平台完整设计方案

## 1. 项目概述

### 1.1 项目名称与版本关系

当前仓库中的实现名仍可保留为：

`ResumeTailor Agent`

但从完整项目包装和后续演进角度，更推荐把大版本项目定义为：

`AI Resume Experiment Platform`

两者关系如下：

1. `ResumeTailor Agent`
   指当前已经能运行的单仓本地工作流系统。
2. `AI Resume Experiment Platform`
   指面向 GitHub 展示与后续扩展的中大型、服务化 AI workflow 项目形态。

也就是说：

`ResumeTailor Agent` 是当前可运行 MVP，`AI Resume Experiment Platform` 是它的目标平台化形态。

### 1.2 一句话定义

这是一个围绕岗位 JD 定制任务构建的 `可复现、可评估、可追溯` 的 AI workflow 实验平台，用于把 `需求理解、证据检索、约束生成、双层审查、质量评估、实验对比` 串成一套完整工程系统。

### 1.3 项目定位

这个项目不再只被定义为“简历改写工具”，也不应只包装成“Prompt Demo”。

更准确的定位是：

> 一个面向岗位定制任务的 AI 应用工程平台，重点展示 `Workflow 编排`、`RAG / Hybrid Retrieval`、`Constraint-first Generation`、`Review Layering`、`Evaluation & Experimentation` 等能力。

### 1.4 为什么要做大

把项目做大，不是为了堆功能，而是为了把它提升为一个更完整、更可信的 GitHub 主项目。

升级后的核心变化是：

1. 从“单次运行工具”升级成“可复现实验平台”。
2. 从“本地脚本链路”升级成“服务化演进架构”。
3. 从“只产出结果”升级成“同时产出 run、report、benchmark、compare artifacts”。
4. 从“只讲业务场景”升级成“同时讲清 AI workflow 方法论和工程实现”。

### 1.5 文档使用方式

为避免设计方案与当前代码脱节，本文档采用 `当前实现状态 + 目标平台设计 + 分阶段演进路线` 的写法。

你可以把它同时当成：

1. 当前仓库的总规格说明。
2. GitHub 项目包装主文档。
3. 下一阶段重构与扩展的架构蓝图。

---

## 2. 当前版本与目标版本的关系

### 2.1 当前仓库是什么

当前仓库已经不是“只有概念”的状态，而是一个能运行的 AI workflow 原型系统，已经具备：

1. 单 JD 定制闭环。
2. 多 JD 对比。
3. 显式 Query Planner。
4. 本地 hybrid-style retrieval。
5. 规则版生成与可选 LLM 增强。
6. 规则审查与可选模型复核接口。
7. 缺口分析与结构化补强建议。
8. Markdown / JSON 导出。
9. 基础评估脚本。
10. Streamlit 演示界面。

### 2.2 当前仓库还不是什么

当前仓库仍然不是：

1. 完整服务化 API 系统。
2. 正式的多服务平台。
3. 带外部向量库和索引管理的检索系统。
4. 有成熟实验注册中心的 benchmark 平台。
5. 多租户在线 SaaS 产品。

### 2.3 目标版本是什么

目标版本是一个中大型、服务化、GitHub 展示优先的 AI workflow 项目：

`AI Resume Experiment Platform`

它的重点不是让功能无限扩张，而是让系统层次清晰：

1. 有在线主链路。
2. 有离线实验链路。
3. 有明确的数据资产层。
4. 有版本化输出和结果对比。
5. 有足够完整的架构叙事。

---

## 3. 问题定义与项目动机

### 3.1 核心现实问题

求职者在面对不同岗位 JD 时，真正困难的往往不是“完全没有经历”，而是：

1. 不知道 JD 真正看重什么能力。
2. 不知道自己哪段经历最适合支撑这些要求。
3. 不知道怎样在不造假的前提下把经历写得更贴岗。
4. 不知道生成结果到底靠不靠谱。
5. 不知道如何比较不同策略、不同模型、不同检索方案的效果差异。

### 3.2 更高层的问题

如果把这个问题提升到 AI 工程角度，本项目要解决的是：

> 如何构建一套面向岗位定制任务的 AI workflow 平台，使其既能完成 `JD -> Evidence -> Resume Output` 的在线生成，又能支撑 `评估、对比、复现、迭代` 的离线实验闭环。

### 3.3 项目动机

这个项目之所以适合做成 GitHub 主项目，原因有三层：

1. `业务层`
   问题真实、明确、可理解。
2. `AI 层`
   天然适合串联解析、检索、约束生成、审查、评估。
3. `工程层`
   非常适合展示模块分层、工作流编排、实验系统设计与可复现性。

---

## 4. 项目目标、边界与成功标准

### 4.1 目标版本总目标

构建一个中大型、服务化演进的 AI workflow 平台，至少具备以下两条链路：

#### 在线主链路

`JD 输入 -> Query Planning -> Hybrid Retrieval -> Evidence Ranking -> Constrained Generation -> Rule/Model Review -> Export`

#### 离线实验链路

`Dataset -> Workflow Variant -> Batch Run -> Evaluation -> Compare -> Versioned Report`

### 4.2 目标版本核心目标

这个大版本最关键的目标不是“加更多求职功能”，而是：

1. 把 AI workflow 主链路做成清晰的工程系统。
2. 把评估与实验系统做成项目亮点，而不是附属脚本。
3. 把结果产出和中间状态做成可复现资产。
4. 让仓库看起来像一个严肃的 AI 应用工程项目，而不是单页小工具。

### 4.3 非目标

为了保持可信和可落地，当前目标版本明确不做：

1. 多租户 SaaS 平台。
2. 复杂账号、组织、权限体系。
3. 自动投递平台。
4. 完整 ATS 集成。
5. 在线简历排版编辑器。
6. 职业测评、社交关系网络、企业 CRM 等泛平台功能。

### 4.4 成功标准

如果这个大版本设计成功，应满足：

1. 项目不再像单一脚本工具，而像清晰的 AI workflow 平台。
2. 在线链路和离线实验链路都能被解释清楚。
3. 模块边界清晰，能对应到仓库目录结构。
4. GitHub 观众能一眼看出它的系统性、可复现性和工程层次。
5. 每个增强模块都能从当前仓库自然演进出来，而不是凭空杜撰。

---

## 5. 目标用户与使用场景

### 5.1 主要观众

这个大版本的第一观众不是普通终端用户，而是：

1. GitHub 作品集观众。
2. 想快速判断项目深度的技术读者。
3. 对 AI workflow、RAG、evaluation、constrained generation 感兴趣的工程面试官。

### 5.2 次级用户

在业务层，它仍然服务真实求职者，尤其是：

1. 需要针对单个 JD 快速定制简历的人。
2. 需要比较多个 JD 对经历改写差异的人。
3. 想识别素材缺口与风险点的人。

### 5.3 核心使用场景

#### 场景一：单 JD 在线定制

用户输入一份 JD，系统返回：

1. JD 结构化理解。
2. 查询计划。
3. 命中证据及原因。
4. 约束生成后的简历内容。
5. 规则审查与模型复核结果。
6. 缺口分析与补强建议。
7. 结构化报告。

#### 场景二：多 JD 对比

用户输入多份 JD，系统返回：

1. 共同关键词。
2. 差异关键词。
3. 各自主命中项目。
4. 缺失点差异。
5. 风险差异。
6. 多份版本化报告。

#### 场景三：离线 benchmark

系统维护一组 case dataset，对不同 workflow 方案进行批量对比，例如：

1. 纯 lexical 检索 vs hybrid 检索。
2. 规则生成 vs constrained LLM merge。
3. 仅规则审查 vs 规则 + 模型复核。

#### 场景四：实验回放与复现

开发者可以查看：

1. 某次 run 的输入。
2. 中间状态。
3. 证据选择。
4. 最终报告。
5. 评估得分。
6. 与其他实验版本的差异。

---

## 6. 系统总体架构

### 6.1 架构风格

目标版本采用：

`单仓 + 服务化分层 + workflow orchestration + offline evaluation`

不是直接做成复杂分布式平台，而是先保持单仓可控，再在设计上形成清晰分层。

### 6.2 顶层分层

推荐拆成六层：

#### 1. 入口层

1. Web UI
2. CLI
3. REST API

#### 2. 编排层

1. Workflow Engine
2. Run Orchestrator
3. Batch Job Scheduler

#### 3. AI 能力层

1. JD Parser
2. Query Planner
3. Hybrid Retriever
4. Evidence Ranker
5. Constrained Generator
6. Rule Reviewer
7. Model Reviewer
8. Interview Planner
9. Gap Analyzer

#### 4. 实验与评估层

1. Evaluation Service
2. Experiment Registry
3. Dataset Manager
4. Benchmark Compare Jobs

#### 5. 数据与资产层

1. Material Store
2. Run Store
3. Report Store
4. Workflow Config / Policy Store

#### 6. 可观测输出层

1. Markdown Reports
2. JSON Run Logs
3. Evaluation Summary
4. Comparison Reports
5. Dashboard Views

### 6.3 两条主链路

#### 在线链路

```text
Web UI / CLI / API
   ↓
Workflow Engine
   ↓
JD Parser
   ↓
Query Planner
   ↓
Hybrid Retriever
   ↓
Evidence Ranker
   ↓
Constrained Generator
   ↓
Rule Reviewer + Model Reviewer
   ↓
Gap Analyzer / Interview Planner
   ↓
Report Export + Run Store
```

#### 离线实验链路

```text
Dataset Manager
   ↓
Experiment Config
   ↓
Batch Run Scheduler
   ↓
Workflow Variants
   ↓
Evaluation Service
   ↓
Experiment Registry
   ↓
Compare Reports / Leaderboard / Versioned Artifacts
```

### 6.4 为什么这样设计

因为这个项目要兼顾两种价值：

1. `在线业务价值`
   真的能完成岗位定制任务。
2. `工程展示价值`
   真的能看起来像一个有评估、有复现、有版本实验的 AI workflow 平台。

---

## 7. 核心服务设计

### 7.1 API Gateway / Application API

职责：

1. 接收来自 Web UI 和 CLI 的请求。
2. 暴露单 run、comparison run、evaluation run 等接口。
3. 统一返回 run id、status、artifact path、summary。

推荐接口风格：

1. `POST /runs`
2. `POST /comparisons`
3. `POST /evaluations`
4. `GET /runs/{id}`
5. `GET /experiments/{id}`
6. `GET /reports/{id}`

### 7.2 Workflow Engine

职责：

1. 编排在线主链路。
2. 保证每个节点输入输出结构清晰。
3. 保存中间状态。
4. 为回放和调试提供 trace。

核心要求：

1. 节点可替换。
2. 节点结果可序列化。
3. 每次 run 可复现。

### 7.3 Retrieval Service

职责：

1. 管理 query planning。
2. 执行 lexical / vector / hybrid 检索。
3. 维护 chunk 索引与 metadata 过滤逻辑。
4. 输出候选 evidence 列表。

### 7.4 Generation Service

职责：

1. 执行 evidence-aware generation。
2. 做结构化字段生成或增强。
3. 进行 field-level conservative merge。
4. 在证据不足时优先保守输出。

### 7.5 Review Service

职责：

1. 执行规则审查。
2. 执行可选模型复核。
3. 合并风险等级与问题列表。
4. 返回 review layers、evidence gaps、unsupported claims。

### 7.6 Evaluation Service

职责：

1. 读取 benchmark dataset。
2. 调度 workflow variant 批量运行。
3. 输出质量指标。
4. 支持版本对比。

### 7.7 Experiment Registry

职责：

1. 注册实验配置。
2. 记录每次实验的参数、版本、结果摘要。
3. 支持按日期、variant、metric 查看实验结果。

### 7.8 Dataset Manager

职责：

1. 管理 JD 样例、素材样例、标注期望。
2. 管理 benchmark case。
3. 管理不同评估任务的数据集版本。

### 7.9 Report Service

职责：

1. 导出单 run 报告。
2. 导出 comparison 报告。
3. 导出 evaluation 报告。
4. 统一 artifact 命名与路径规范。

---

## 8. 工作流节点设计

### 8.1 节点设计原则

每个节点都应满足：

1. 单一职责。
2. 输入输出结构明确。
3. 中间结果可记录。
4. 可被替换或增强。
5. 失败时能快速定位问题。

### 8.2 节点清单

#### JD Parser

输入：

1. 原始 JD 文本。

输出：

1. 结构化需求对象。
2. 关键词。
3. must-have。
4. nice-to-have。
5. 聚焦方向。

#### Query Planner

输入：

1. 结构化 JD。

输出：

1. query tokens。
2. expanded terms。
3. query text。
4. retrieval hints。

说明：

当前仓库已显式实现这一层，目标版本中它应被正式视为一等节点，而不是辅助函数。

#### Hybrid Retriever

输入：

1. QueryPlan
2. MaterialChunk 集合

输出：

1. Top-K 候选 evidence
2. lexical score
3. vector score
4. metadata / match reason

#### Evidence Ranker

输入：

1. 候选 evidence

输出：

1. 去重后 evidence 列表
2. 排序后 evidence 列表
3. explainable reasons

#### Constrained Generator

输入：

1. JD summary
2. ranked evidence
3. policy config

输出：

1. fit summary
2. project highlights
3. skills summary
4. self intro
5. matched requirements

要求：

1. 优先 evidence-grounded。
2. 不支持的字段必须保守回退。
3. 输出结构必须稳定。

#### Interview Planner

输入：

1. resume output
2. ranked evidence

输出：

1. 面试追问
2. 对应提示

#### Gap Analyzer

输入：

1. JD summary
2. ranked evidence

输出：

1. matched keywords
2. missing keywords
3. weak requirements
4. suggestion cards

#### Rule Reviewer

输入：

1. resume output
2. evidence texts

输出：

1. risk level
2. rule issues

#### Model Reviewer

输入：

1. resume output
2. evidence texts

输出：

1. evidence gaps
2. model review issues
3. merged risk signals

#### Exporter

输入：

1. run context

输出：

1. markdown
2. json
3. comparison artifact
4. evaluation artifact

---

## 9. 数据模型设计

### 9.1 核心实体

目标版本建议至少定义以下核心对象：

#### JDDocument

字段建议：

1. `id`
2. `raw_text`
3. `parsed`
4. `source`
5. `created_at`

#### MaterialAsset

字段建议：

1. `id`
2. `title`
3. `type`
4. `source_file`
5. `raw_text`
6. `tags`
7. `metadata`

#### MaterialChunk

字段建议：

1. `id`
2. `asset_id`
3. `raw_text`
4. `summary`
5. `tags`
6. `embedding_ref`

#### QueryPlan

字段建议：

1. `keywords`
2. `query_tokens`
3. `expanded_terms`
4. `query_text`
5. `filters`

#### EvidenceItem

字段建议：

1. `chunk_id`
2. `score`
3. `lexical_score`
4. `vector_score`
5. `reason`
6. `chunk_snapshot`

#### ResumeDraft

字段建议：

1. `fit_summary`
2. `project_highlights`
3. `skills_summary`
4. `self_intro`
5. `matched_requirements`
6. `constraint_mode`
7. `llm_enhanced`

#### ReviewResult

字段建议：

1. `risk_level`
2. `issues`
3. `review_layers`
4. `model_review`
5. `mode`

#### GapResult

字段建议：

1. `matched_keywords`
2. `missing_keywords`
3. `weak_requirements`
4. `suggestion_cards`

#### RunRecord

字段建议：

1. `run_id`
2. `workflow_version`
3. `inputs`
4. `query_plan`
5. `retrieval`
6. `generation`
7. `review`
8. `gap`
9. `artifacts`
10. `created_at`

#### EvaluationCase

字段建议：

1. `label`
2. `jd_source`
3. `materials_source`
4. `expected_keywords`
5. `expected_projects`
6. `expected_risk_level`

#### ExperimentConfig

字段建议：

1. `experiment_id`
2. `retrieval_mode`
3. `generator_mode`
4. `review_mode`
5. `dataset_version`
6. `notes`

### 9.2 设计意义

这些对象的重要性在于：

1. 它们让系统从“函数链”升级成“可管理的 workflow 状态系统”。
2. 它们为评估、回放、对比提供统一数据基础。
3. 它们让 GitHub 观众更容易理解系统边界和工程成熟度。

---

## 10. 检索策略设计

### 10.1 当前适合保留的优点

当前仓库的检索思路有真实价值：

1. 可解释。
2. 本地可运行。
3. 对显式岗位关键词命中很直观。
4. 适合作为 baseline。

### 10.2 目标版本检索策略

目标版本更推荐：

`Hybrid Retrieval = lexical + vector + rerank`

分为三步：

1. Query Planner 负责产生查询表达。
2. Retriever 负责 lexical / vector 双通道召回。
3. Ranker 负责最终重排与去重。

### 10.3 推荐能力点

为了让项目看起来像严肃 AI workflow 平台，检索层建议具备：

1. 多种 retrieval mode。
2. chunk metadata filter。
3. 命中理由保留。
4. vector signal 和 lexical signal 同时可见。
5. benchmark 里可切换不同检索配置。

### 10.4 不必过度包装的点

这个大版本无需硬写成：

1. 企业级向量数据库平台。
2. PB 级数据检索系统。
3. 高吞吐实时检索基础设施。

更可信的表述是：

> 一个面向特定任务的小规模、可复现实验型 hybrid retrieval 系统。

---

## 11. 生成与约束策略设计

### 11.1 当前策略

当前生成层已经从“完全自由生成”前进到：

1. 规则组织内容。
2. 可选结构化增强。
3. 字段级 conservative merge。

### 11.2 目标版本策略

目标版本应明确采用：

`constraint-first generation`

核心约束如下：

1. 生成必须依赖 evidence。
2. 证据不足时宁可保守，不做夸大补全。
3. 输出必须是结构化字段。
4. 每个字段都支持独立回退。

### 11.3 推荐实现原则

1. 规则草稿先行。
2. 模型只增强，不直接接管全部内容。
3. 每个增强字段都要检查 evidence grounding。
4. 模型失败时稳定回退到规则版本。

### 11.4 为什么这是项目亮点

因为这能把项目从“让大模型润色文本”提升为：

> 一个有明确安全边界和证据边界的 constrained generation workflow。

---

## 12. 审查与风险控制策略

### 12.1 目标

审查层不是可有可无的后处理，而是平台可信度的核心部分。

### 12.2 双层审查结构

推荐结构：

1. `Rule Review`
   检查高风险词、夸大型措辞、明显 unsupported claim。
2. `Model Review`
   检查潜在 evidence gap、表述和证据不一致、语义级风险。

### 12.3 目标输出

审查结果至少应包含：

1. `risk_level`
2. `issues`
3. `review_layers`
4. `model_review.enabled`
5. `model_review.evidence_gaps`

### 12.4 目标版本可继续增强的能力

1. 字段级风险定位。
2. 事实支撑缺口分类。
3. 版本间风险变化对比。
4. 评估集上的“真实性一致性分”。

---

## 13. 评估与实验系统设计

### 13.1 为什么评估系统必须是主角

如果这个项目要作为 GitHub 主项目，真正拉开层次的，不是 UI，而是：

1. 你能否跑 benchmark。
2. 你能否比较 variant。
3. 你能否保存实验结果。
4. 你能否解释为什么这版比上一版更好。

### 13.2 评估系统的最小闭环

至少需要：

1. case dataset。
2. evaluation runner。
3. metrics summary。
4. comparison report。

### 13.3 推荐指标

建议按四类指标组织：

#### 检索相关

1. 关键词召回率
2. 主项目命中率
3. evidence presence

#### 生成相关

1. 结构完整性
2. 保守回退率
3. unsupported field rejection rate

#### 风险相关

1. risk distribution
2. unsupported claim count
3. model review hit rate

#### 综合相关

1. overall score
2. variant delta
3. run reproducibility status

### 13.4 实验注册中心

Experiment Registry 不一定非要上数据库，但在设计上应具备：

1. 记录 experiment config。
2. 记录 dataset version。
3. 记录 metric summary。
4. 支持不同 variant 对比。

### 13.5 目标包装话术

这个模块最适合包装成：

> 一个支持 workflow benchmark、variant compare 和 artifact replay 的 AI evaluation subsystem。

---

## 14. 界面与交互设计

### 14.1 UI 目标

UI 在目标版本里不只是展示最终结果，而要承接：

1. run 调试。
2. evidence 查看。
3. comparison 展示。
4. evaluation dashboard 展示。

### 14.2 推荐页面结构

#### 页面一：Run Studio

展示：

1. JD 输入
2. Query Plan
3. Evidence
4. Resume Output
5. Review Result
6. Gap Suggestion

#### 页面二：Comparison Lab

展示：

1. 多 JD 输入
2. common keywords
3. unique keywords
4. top project by JD
5. risk / gap difference

#### 页面三：Evaluation Dashboard

展示：

1. case 数量
2. 平均指标
3. variant 对比
4. 失败 case
5. artifact link

#### 页面四：Experiment Explorer

展示：

1. experiment config
2. run list
3. report links
4. metric summary

### 14.3 当前与目标差异

当前 Streamlit 更偏：

1. 单次运行展示。
2. 本地调试视角。

目标版本 UI 更偏：

1. workflow control console
2. comparison dashboard
3. evaluation dashboard

---

## 15. 技术选型与仓库结构设计

### 15.1 推荐技术栈

目标版本推荐围绕以下技术栈组织：

1. `Python`
2. `FastAPI` 或同级 API 框架
3. `Streamlit` 或轻量 Web console
4. `Pydantic`
5. `Markdown / JSON artifact`
6. `OpenAI 兼容 API`
7. `FAISS / Chroma / local vector backend`

### 15.2 选型理由

#### Python

1. 与 AI 工作流生态兼容。
2. 便于快速搭建 prototype 和 benchmark。

#### FastAPI

1. 便于把 workflow 暴露成服务接口。
2. 适合单仓服务化演进。

#### Streamlit

1. 适合快速做控制台与结果展示。
2. 对 GitHub Demo 友好。

#### Pydantic

1. 适合 workflow schema 化。
2. 适合 run record 和 artifact model 定义。

#### Local Vector Backend

1. 便于展示 hybrid retrieval 的真实形态。
2. 不必依赖云向量服务也可演示。

### 15.3 目标仓库结构建议

```text
岗位JD-RAG/
├── apps/
│   ├── api/
│   └── web/
├── resumetailor_agent/
│   ├── core/
│   ├── workflows/
│   ├── services/
│   ├── stores/
│   ├── exporters/
│   ├── evaluators/
│   └── schemas/
├── datasets/
│   ├── jd_cases/
│   ├── eval_cases/
│   └── materials/
├── experiments/
│   ├── configs/
│   └── registry/
├── outputs/
├── tests/
├── README.md
└── requirements.txt
```

### 15.4 演进原则

这里强调的是“概念分层优先”，不是要求你一次性把当前仓库全部重构完。

更合理的路线是：

1. 先保留当前单仓实现。
2. 再逐步把 services、evaluators、stores 独立出来。
3. 最后才考虑 API 和更正式的 app 层。

---

## 16. 输出格式与可观测资产设计

### 16.1 单 run 输出

单 run 报告至少应包含：

1. JD 摘要
2. Query Plan
3. Evidence
4. Resume Output
5. Interview Output
6. Gap Output
7. Review Output
8. Artifact Path

### 16.2 多 JD 输出

多 JD 报告应至少包含：

1. common keywords
2. unique keywords
3. top project per JD
4. missing keywords per JD
5. risk per JD
6. per-run report link

### 16.3 评估输出

评估报告应至少包含：

1. case count
2. average metric
3. per-case metric
4. variant summary
5. failed case links

### 16.4 运行日志

运行日志不仅用于调试，还应用于：

1. 回放。
2. 实验对比。
3. benchmark 归档。
4. GitHub artifact 展示。

---

## 17. 当前实现与目标版本映射

### 17.1 当前已具备的基础

当前仓库已经具备目标版本的以下雏形：

1. `Workflow Engine 雏形`
   当前 `workflow.py` 已承担轻量编排角色。
2. `Query Planner`
   已有显式查询计划对象与结构。
3. `Hybrid-style Retriever`
   已有 lexical + local vector signal。
4. `Constrained Merge Baseline`
   已有 evidence-aware conservative merge。
5. `Review Layer Baseline`
   已有 rule review 和 model review 接口层。
6. `Evaluation Runner Baseline`
   已有批量评估脚本与报告导出。
7. `Comparison Path`
   已有多 JD 对比和差异摘要雏形。

### 17.2 还需要补齐的关键模块

真正让它成为“大项目”的缺口主要在：

1. 正式 API 层。
2. 更清晰的 service / store 分层。
3. 更正式的 dataset 目录与版本机制。
4. 更完整的 experiment registry。
5. 更强的 benchmark 体系。
6. 更像控制台的 UI 结构。

### 17.3 为什么这个映射重要

因为它说明：

1. 这个大项目不是从零杜撰。
2. 它确实能从当前仓库演进出来。
3. 你的项目包装有清楚的“当前 -> 下一版 -> 平台版”路径。

---

## 18. 分阶段演进路线

### 18.1 阶段一：V1 本地工作流版

目标：

`能跑通单 JD 和多 JD 定制链路`

状态：

已完成

### 18.2 阶段二：V1.5 质量增强版

目标：

1. Query Planner 显式化
2. local vector signal
3. 更强 constrained merge
4. 结构化 gap suggestion
5. 基础 evaluation

状态：

已完成基础版

### 18.3 阶段三：V2 服务化工作流版

目标：

1. 引入 API 层
2. 拆出 services / stores
3. 把在线链路变成正式 service-oriented workflow

### 18.4 阶段四：V2.2 实验平台版

目标：

1. dataset manager
2. experiment registry
3. benchmark compare jobs
4. evaluation dashboard

### 18.5 阶段五：V2.5 GitHub 展示强化版

目标：

1. README 重构
2. 架构图与 run examples
3. benchmark artifact 展示
4. demo scripts 与 sample datasets

---

## 19. 这个项目最适合提炼的亮点

### 19.1 业务亮点

1. 真实问题驱动。
2. 直接对应岗位定制场景。
3. 不只是“写简历”，而是“任务理解 + 证据对齐 + 风险控制”。

### 19.2 AI 亮点

1. Hybrid Retrieval
2. Query Planning
3. Constraint-first Generation
4. Rule + Model Review
5. Evaluation & Benchmarking

### 19.3 工程亮点

1. 节点化 workflow。
2. 服务化演进路径。
3. artifact-first 输出。
4. 可复现实验链路。
5. 在线主链路与离线实验链路并存。

### 19.4 GitHub 展示亮点

最适合这样概括：

> 一个围绕岗位定制任务构建的 AI workflow 实验平台，兼具在线生成链路、风险审查链路和离线 benchmark / compare 链路。

---

## 20. 风险与应对策略

### 20.1 风险一：项目被吹得过大

如果直接写成企业级平台，会丧失可信度。

应对：

1. 强调单仓服务化演进。
2. 强调实验平台而非企业级平台。
3. 强调 current-to-target mapping。

### 20.2 风险二：功能多但主线弱

如果只堆页面和子系统，会稀释项目主线。

应对：

1. 始终围绕 `workflow + evaluation` 两条主线组织设计。
2. 所有模块都要回到这两条主线。

### 20.3 风险三：实现跨度太大

如果试图一次性实现全部层次，会拖慢节奏。

应对：

1. 把“设计上的完整性”和“实现上的阶段性”分开。
2. 先完成平台骨架，再逐步补服务。

### 20.4 风险四：看起来像伪平台

如果没有数据集、评估、实验对比，这个“大项目”就只是名字变大了。

应对：

1. 必须保留 evaluation 与 experiment 作为主模块。
2. 必须有 benchmark artifact。
3. 必须有 variant compare 结果。

---

## 21. 总结

如果只把当前仓库继续包装成“简历定制工具”，它虽然真实，但项目上限有限。

更好的路径是：

把它提升为一个中大型、服务化演进、GitHub 展示优先的 AI workflow 项目：

`AI Resume Experiment Platform`

这个版本的关键不在于做成“求职超级平台”，而在于把一个真实任务场景，升级成：

1. 有在线 workflow 主链路的 AI 应用系统。
2. 有离线 benchmark 与 compare 链路的实验平台。
3. 有结构化 artifact、run log、report、dataset、experiment config 的工程项目。

因此，这个项目最有价值的包装，不是“会帮人改简历”，而是：

> 它展示了你如何把一个真实任务，做成一个 `可解释、可评估、可复现、可服务化演进` 的 AI workflow 平台。

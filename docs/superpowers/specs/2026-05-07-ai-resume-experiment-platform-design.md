# AI Resume Experiment Platform Design

**Date:** 2026-05-07

**Purpose:** Capture the upgraded direction for evolving `ResumeTailor Agent` from a local workflow tool into a GitHub-first, service-oriented AI workflow experiment platform.

## Canonical Design Doc

The primary full design document is:

- [ResumeTailor-Agent-完整设计方案.md](/Users/smx/program/vscode/5.6简历项目包装/岗位JD-RAG/ResumeTailor-Agent-完整设计方案.md)

This spec is a compact index for future implementation planning.

## Chosen Direction

The project is now positioned as:

`AI Resume Experiment Platform`

Key framing:

1. `ResumeTailor Agent` remains the current runnable MVP.
2. `AI Resume Experiment Platform` is the target medium-large platform shape.
3. The project is optimized for `GitHub showcase` first, not for multi-tenant productization.

## Core Architectural Decision

The target version should be described as a `single-repo, service-oriented AI workflow platform` with two primary paths:

1. Online path:
   `JD -> Query Planning -> Hybrid Retrieval -> Evidence Ranking -> Constrained Generation -> Review -> Export`
2. Offline path:
   `Dataset -> Workflow Variant -> Batch Run -> Evaluation -> Compare -> Versioned Report`

## Required Top-Level Modules

1. Entry layer: Web UI, CLI, REST API
2. Orchestration layer: Workflow Engine, Run Orchestrator, Batch Scheduler
3. AI capability layer: Parser, Planner, Retriever, Ranker, Generator, Reviewer, Gap Analyzer
4. Evaluation layer: Evaluation Service, Experiment Registry, Dataset Manager, Benchmark Jobs
5. Asset layer: Material Store, Run Store, Report Store, Workflow Policy Config
6. Output layer: Markdown / JSON artifacts, comparison reports, evaluation dashboards

## Why This Direction

This framing makes the project stronger because it:

1. Preserves the real business scenario.
2. Elevates the project from tool to reproducible AI workflow system.
3. Adds benchmark and experiment value, which is more compelling on GitHub.
4. Keeps the scope believable by avoiding SaaS, multi-tenant, and enterprise-platform overclaiming.

## Major Upgrade Themes

1. `Hybrid retrieval` as a first-class subsystem
2. `Constraint-first generation` instead of free-form polishing
3. `Rule review + model review` as a layered trust mechanism
4. `Evaluation and experiment registry` as core platform modules
5. `Artifact-first outputs` for reproducibility and replay

## Boundaries

Deliberately excluded from the current target version:

1. Multi-tenant user system
2. ATS / recruiting platform integration
3. Full online resume editor
4. Large-scale distributed platform claims
5. “AI job super-app” style platform sprawl

## Next Planning Hook

When converting this design into an implementation plan, the first planning split should be:

1. Service boundaries and repository restructuring
2. Evaluation / dataset / experiment workflow
3. UI console expansion for run, compare, and evaluation views

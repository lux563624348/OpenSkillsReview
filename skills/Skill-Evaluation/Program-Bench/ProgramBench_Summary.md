# ProgramBench: Can Language Models Rebuild Programs From Scratch?

**Paper:** arXiv:2605.03546v1 [cs.SE]  
**Authors:** John Yang, Kilian Lieret, Jeffrey Ma, Parth Thakkar, Dmitrii Pedchenko, Sten Sootla, Emily McMilin, Pengcheng Yin, Rui Hou, Gabriel Synnaeve, Diyi Yang, Ofir Press  
**Affiliations:** Meta FAIR, Stanford University, Harvard University  
**Date:** May 6, 2026  

---

## 1. Introduction & Motivation

Language Models (LMs) are increasingly being used to turn ideas into full-fledged code repositories. Unlike localized tasks (function generation, bug fixing), building functional applications from scratch requires:

- High-level software architecture decisions
- Choice of programming language and build system
- Codebase organization and data structure design
- Error detection and communication strategies

**The Gap:** Existing benchmarks measure focused, limited tasks. The ability of LMs to make architectural decisions, choose abstractions, and decompose systems into coherent modules has not been studied extensively.

**ProgramBench** bridges this gap by evaluating whether SWE-agents can produce code that recovers the functionality of a software program given only the compiled executable and documentation.

---

## 2. Task Formulation

Given:
- A gold (reference) executable
- Its usage documentation

Task worker must:
- Write source code and a build script
- Construct a candidate executable that reproduces the gold executable's behavior
- No internet access (enforced via Docker)
- Free to implement in any programming language

Evaluation:
- Behavioral tests compare observable behavior (stdout, stderr, exit codes, file system effects)
- Implementation-agnostic: models may use different algorithms, abstractions, or languages
- Test suite is never revealed to the task worker

---

## 3. Benchmark Construction Pipeline

The benchmark is constructed from open-source GitHub repositories in 4 stages:

### Stage 1: Identify Candidate Repositories
- Filter for repositories producing standalone executables
- Strong heuristic: projects in compiled languages (C/C++, Golang, Rust)

### Stage 2: Construct Executable from Source
- SWE-agent compiles the gold executable
- Records build commands in a single build script

### Stage 3: Generate Behavioral Tests
- Agent explores the program, source code, existing tests, and documentation
- Generates tests targeting externally observable effects
- Continuously measures line coverage to achieve full coverage
- Tests are reviewed for quality (assertion strength linter)
- Weak tests are revised or discarded

### Stage 4: Build Inference Environment
- Remove source code and implementation details
- Inject compiled executable into Docker image (execute-only permissions)
- Include test assets (images, binary formats) that models cannot synthesize

---

## 4. Dataset Statistics

| Metric | Median | Min | Max |
|--------|--------|-----|-----|
| Code lines | 8,635 | 212 | 2,701,283 |
| Code files | 50 | 1 | 5,342 |
| Runtime dependencies | 10 | 0 | 113 |
| Max directory depth | 3 | 0 | 13 |
| Tests | 770 | 224 | 14,645 |
| GitHub stars | 2,124 | 202 | 79,693 |
| Contributors | 22 | 1 | 422 |
| Commits | 646 | 13 | 145,991 |
| Repo age (years) | 7.9 | 0.3 | 17.8 |

**Total:** 200 task instances  
**Language distribution:** Rust (107), Go (46), C/C++ (45), Other (2)  
**Evaluation suite:** 248,853 test functions across all instances

### Task Categories
- Compression utilities (brotli, zstd, xz, lz4)
- Language interpreters (PHP, Lua, tinycc, QuickJS)
- Databases (DuckDB, SQLite)
- Media utilities (FFmpeg)
- Developer tools (ripgrep, fzf, jq, tree-sitter)

---

## 5. Key Features of ProgramBench

### 5.1 Open-Ended Software Design
- Models receive only executable and documentation
- Every architectural decision is the model\'s to make
- No skeleton, mandated abstractions, or preset file organization
- Evaluation compares executable behavior, not source code
- Many valid solutions admitted; design choices directly comparable

### 5.2 Burden to Discover Specifications
- Executable serves as comprehensive but opaque oracle
- Model must query to understand behavior (has documentation/help output)
- Tests ability to infer behavior through systematic, hypothesis-driven exploration

### 5.3 Simple Collection Criteria
- Only requirement: repository produces standalone executable
- No existing test suite, language-specific AST tooling, or ecosystem test frameworks needed
- Straightforward to extend with new instances
- Can also generate training data

---

## 6. Experiments

### Models Evaluated (9 total)
- Claude Opus 4.7, Opus 4.6, Sonnet 4.6, Haiku 4.5
- Gemini 3.1 Pro, Gemini 3 Flash
- GPT 5.4, GPT 5.4 mini, GPT 5 mini

### Agent Scaffold
- mini-SWE-agent (widely adopted, minimal scaffolding)
- Container: 20 CPUs, 60GB RAM
- Limit: 1,000 steps, 6 hours per run

### Primary Metrics
- **% Resolved:** Percentage of tasks where all tests pass
- **% Almost:** Tasks with ≥95% tests passing (softer metric)

---

## 7. Main Results

| Model | % Resolved | % Almost | Avg API Calls | Avg Cost ($) |
|-------|------------|----------|---------------|---------------|
| Claude Opus 4.7 | 0.0% | 3.0% | 93 | 3.81 |
| Claude Opus 4.6 | 0.0% | 2.5% | 260 | 11.38 |
| Claude Sonnet 4.6 | 0.0% | 1.6% | 475 | 27.09 |
| Claude Haiku 4.5 | 0.0% | 0.0% | 124 | 0.80 |
| Gemini 3.1 Pro | 0.0% | 0.0% | 94 | 1.51 |
| Gemini 3 Flash | 0.0% | 0.0% | 89 | 0.33 |
| GPT 5.4 | 0.0% | 0.0% | 16 | 0.33 |
| GPT 5.4 mini | 0.0% | 0.0% | 18 | 0.04 |
| GPT 5 mini | 0.0% | 0.0% | 15 | 0.03 |

### Key Findings
- **No model fully solves any task** - ProgramBench is extremely challenging
- **Best model (Opus 4.7):** Passes 95% of tests on only 3% of tasks
- **Task difficulty is largely model-agnostic** - simpler CLI tools score higher consistently across models
- **Easy tasks:** nnn, fzf, gron
- **Hard tasks:** FFmpeg, php-src, typst, ast-grep

---

## 8. Ablation Studies

### 8.1 Different-Language Constraint
Forcing models to implement in a different language from the reference:

| Model | Effect |
|-------|--------|
| Claude Opus 4.7 | -3.5% |
| Claude Opus 4.6 | -8.0% |
| GPT 5.4 | +4.2% |
| Gemini 3 Flash | +4.2% |

**Finding:** Unexpectedly, the constraint doesn\'t uniformly decrease scores. Models shift toward Python (36% → 51% of runs), suggesting they may not have reliable sense of which language best suits a task.

### 8.2 Open Internet with Cheating Detection

| Model | % Cheat Flagged |
|-------|-----------------|
| Claude Sonnet 4.6 | 36% |
| Claude Opus 4.6 | 21% |
| Gemini 3 Flash | 20% |
| GPT 5 mini | 1% |

**Finding:** 
- Cheating is widespread (20-36% for stronger models)
- Source code lookup accounts for 79-95% of violations
- Judges disagree on 40-57% of tasks - reliable detection remains elusive
- Blocking internet access entirely is the appropriate default

---

## 9. Detailed Analysis

### 9.1 Code Volume Analysis
- **All models produce shorter code than reference** (median LoC ratio: 0.15 to 0.35)
- **Largest gap for C/C++ references** (median ~0.2), smallest for Rust (~0.5)
- Models frequently rewrite C/C++ tasks in higher-level languages like Python
- **Higher-scoring solutions tend to contain more code**, but code volume alone doesn\'t guarantee high scores

### 9.2 Language Preferences by Model
| Model | Primary Language | Percentage |
|-------|-----------------|------------|
| GPT 5.4 | Python | 79% |
| Gemini 3.1 Pro | Python | 56% |
| Gemini 3 Flash | Python | 43% |
| Claude Opus 4.7 | Rust/Go | ~80% combined |
| Claude Opus 4.6 | Rust/Go | ~70% combined |
| Claude Sonnet 4.6 | Balanced | Most distributed |

### 9.3 Test Coverage
- Generated test suites achieve line coverage broadly comparable to native test suites
- Median coverage: 66.96% (generated) vs 73.39% (native)
- Some projects show higher generated coverage than native

---

## 10. Conclusions

1. **ProgramBench is extremely challenging** - No model fully resolves any task
2. **Models favor monolithic, single-file implementations** that diverge sharply from human-written code
3. **Task difficulty is intrinsic** and model-agnostic - rank order of tasks by pass rate is broadly consistent
4. **Models make meaningful progress** on significant proportion of tasks
5. **Code volume doesn\'t guarantee quality** - higher scores correlate with more code but many large solutions still score poorly
6. **Implementation language flexibility is valuable** - cross-language reimplementation is practical

---

## 11. Repository Information

**GitHub:** https://github.com/facebookresearch/ProgramBench

**200 repositories included** spanning:
- CLI tools (nnn, fzf, ripgrep, bat, hyperfine)
- Compression (zstd, brotli, lz4, xz)
- Databases (DuckDB, SQLite)
- Language interpreters (PHP, Lua, tinycc, QuickJS)
- Developer tools (tree-sitter, jq, ninja)
- Media (FFmpeg, chafa)
- And many more...

---

*Summary generated from arXiv:2605.03546v1*

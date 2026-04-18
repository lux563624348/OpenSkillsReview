---
name: ai-trade-ecometrics
description: >
  Write an analysis paper on how automation, algorithmic trading, or AI trading agents affect financial markets, investment structure, and labor markets. Use this skill whenever the user wants a research paper, essay, report, deep analysis, or thought piece about AI trading, quant automation, trading-agent adoption, market structure shifts, investor stratification, employment effects in finance, or broader labor-market consequences of trading automation. Use it even if the user does not explicitly ask for a "paper" but clearly wants a structured, evidence-aware analysis.
---

# AI Trade Ecometrics

Use this skill to turn a broad idea about automation or AI trading into a structured analysis paper. The goal is not to produce hype copy. The goal is to produce a defensible paper with a clear thesis, explicit assumptions, balanced argumentation, and a clean separation between what is observed, what is inferred, and what remains uncertain.

The existing file [analysis.md](./analysis.md) is background material and a seed thesis. Treat it as reference context, not as a script to copy verbatim.

## What This Skill Produces

Produce one of these by default, depending on the user's wording:

- A research-style analysis paper
- A policy or market-structure memo
- A long-form essay with explicit evidence and counterarguments

Unless the user specifies otherwise, optimize for a paper that is:

- Analytical rather than promotional
- Balanced rather than purely directional
- Readable by finance-literate readers
- Explicit about uncertainty

## When This Skill Should Trigger

Use this skill when the user asks for topics such as:

- "Write a paper on AI trading and labor markets"
- "Analyze how automation changes investing"
- "How do AI trading agents affect hedge funds and retail investors?"
- "Write a report on algorithmic trading and employment in finance"
- "Compare AI trading with past technology shifts in markets"
- "Assess the impact of trading automation on market efficiency and inequality"

Do not use this skill for:

- Short tactical trade ideas
- Pure coding of a trading bot
- A backtest-only request
- A token-specific due-diligence memo

## Required Inputs

If the user already provided these, do not ask again. Otherwise, infer reasonable defaults and state them briefly in the paper.

- Topic scope
- Geographic scope
- Time horizon
- Target audience
- Desired tone
- Evidence standard

Use these defaults when missing:

- Topic scope: AI trading, automation, and algorithmic market participation
- Geographic scope: U.S. and global developed markets
- Time horizon: near-term 1 to 3 years and structural 5 to 10 years
- Target audience: finance-literate general reader
- Desired tone: analytical and balanced
- Evidence standard: qualitative reasoning with clearly marked factual claims

## Core Writing Rules

Follow these rules every time:

1. Separate facts from interpretations.
2. Avoid invented statistics, dates, adoption rates, or market-share claims.
3. If a numerical claim is not sourced by the user or available in the current context, either omit it or label it as a hypothesis, estimate, or common market claim that needs verification.
4. Distinguish impacts on:
   - market structure
   - investment performance and competition
   - labor demand and job design
   - regulation and fairness
5. Include at least one serious counterargument.
6. Do not assume AI always improves alpha. Discuss crowding, model convergence, data access asymmetry, and regime-break risk.
7. Do not frame the conclusion as inevitable. Use scenarios and conditions.

## Recommended Workflow

### Step 1: Frame the research question

Convert the user's idea into a precise question.

Good examples:

- "How will AI trading agents reshape investor competition and job roles in finance over the next decade?"
- "Does automation in trading democratize institutional capability, or mainly widen the gap between top-tier and mid-tier firms?"
- "What labor-market changes follow from the adoption of AI in research, execution, and risk management?"

### Step 2: Define the analytical lens

Pick one primary lens and up to two supporting lenses.

Primary lens options:

- Market structure
- Institutional competition
- Labor economics
- Technology diffusion
- Regulation and fairness

Supporting lenses:

- Historical analogy
- Productivity economics
- Investor-behavior change
- Risk management and tail events

### Step 3: Build the thesis and the tensions

State a thesis in one or two sentences, then define the main tensions. Good papers in this domain usually revolve around tensions such as:

- democratization vs concentration
- efficiency vs resilience
- automation vs human judgment
- productivity gains vs labor displacement
- lower research costs vs stronger data monopolies

### Step 4: Organize the paper into clear sections

Use the default structure below unless the user asks for another format.

## Default Paper Structure

Use this structure in order:

```markdown
# [Title]

## Executive Summary
- 3 to 5 sentences

## Research Question

## Core Thesis

## Historical Parallel
- Compare AI trading with prior market technology shifts such as electronic trading, Bloomberg-era information compression, quant expansion, or execution automation.

## Investment-Market Impact
- Market efficiency
- Information asymmetry
- Retail vs institutional capability
- Competition among large, mid-sized, and small firms
- Crowding, correlation, and model convergence risks

## Labor-Market Impact
- Roles most exposed to automation
- Roles likely to be redesigned rather than eliminated
- Skills that become more valuable
- Organizational effects on small funds, banks, and asset managers

## Counterarguments And Limits
- What the bullish automation thesis misses
- What current AI systems still struggle with
- Data, compliance, and regime-shift constraints

## Scenarios
- Base case
- Bull case
- Bear case

## Regulatory And Social Implications

## Conclusion
```

### Step 5: Use evidence carefully

When the user asks for a rigorous paper, do the following:

- Prefer concrete mechanisms over unsupported numbers
- Use historical analogies only when the transmission mechanism is explained
- Mark speculative claims as speculative
- State where evidence is thin

If browsing or data lookup is available in the environment and the user asks for a sourced paper, gather current sources before writing. If reliable sourcing is not available, say that the piece is a conceptual analysis rather than a fully sourced empirical paper.

## Writing Guidance By Section

### Executive Summary

Summarize:

- what is changing
- who benefits
- who is pressured
- what remains uncertain

### Historical Parallel

Do not force a simplistic "AI equals the PC revolution" analogy. Explain:

- what was similar
- what is structurally different
- why the comparison is still useful

### Investment-Market Impact

Address at least four of the following:

- execution speed and market efficiency
- signal crowding
- reduced research and monitoring costs
- institutional edge from proprietary data and infrastructure
- compression of informational advantage for mid-tier players
- retail enablement through AI tooling
- risk of synchronized strategies and feedback loops

### Labor-Market Impact

Separate tasks from jobs. A strong paper should distinguish:

- tasks likely to be automated
- jobs likely to shrink
- jobs likely to change shape
- jobs likely to gain leverage from AI

Useful role categories:

- junior research
- execution trading
- portfolio support and reporting
- risk and surveillance
- senior discretionary decision-making
- compliance and model governance

### Counterarguments And Limits

Always include some of the following:

- AI can standardize mediocre process faster than it creates true edge
- access to data and infrastructure may stay concentrated
- market participants using similar models can destroy excess returns
- black-swan and regime-shift environments are hard to encode
- legal and compliance requirements can slow deployment

## Style Requirements

Write in a sober, publication-ready tone.

- Avoid hype language
- Avoid deterministic claims
- Prefer "may", "likely", "under this scenario", and "conditional on"
- Keep paragraphs focused
- Use subheadings generously in long papers

## Prohibited Failure Modes

Do not do the following:

- copy `analysis.md` verbatim
- present unsupported statistics as facts
- collapse "financial market impact" and "labor-market impact" into one vague section
- assume all automation effects are positive
- confuse finance job displacement with total-economy labor outcomes
- present a one-sided manifesto instead of analysis

## Fast Adaptation Modes

If the user asks for a specific format, adapt while preserving the same analytical discipline.

Examples:

- For "op-ed": keep stronger voice, but still preserve counterarguments
- For "white paper": increase structure and define assumptions explicitly
- For "academic-style note": use tighter claims and more caveats
- For "investor memo": focus more on market structure and competitive implications

## Output Checklist

Before finishing, confirm that the paper:

- has a clear research question
- states a thesis early
- separates investment impact from labor impact
- contains at least one counterargument section
- avoids unsourced hard numbers unless provided by the user
- ends with a conditional conclusion rather than a slogan

## Suggested Use Of `analysis.md`

Read [analysis.md](/home/xli/github/PSC/OpenSkillsReview/skills/Skill-Finance/AI-trade-ecometrics/analysis.md) when you want seed ideas for:

- the FICC-to-crypto framing
- the computer-revolution analogy
- investor stratification
- the "mini hedge fund" concept
- labor polarization in finance

Treat those ideas as raw material to refine, challenge, or rebalance. Do not inherit its assumptions uncritically.

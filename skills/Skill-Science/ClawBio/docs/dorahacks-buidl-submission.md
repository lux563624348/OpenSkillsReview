# DoraHacks BUIDL Submission — ClawBio

> Copy each section below into the corresponding DoraHacks field.
> Last updated: 5 March 2026

---

## Project Name

ClawBio

## Tagline (short description for sidebar)

ClawBio turns biomedical research into installable AI agent skills, making computational reproduction a one-liner. 21 skills, 14 production-ready, built on OpenClaw. Local-first. Privacy-focused. Reproducible.

## Category

AI / Robotics

---

## The Problem

Reproducing a single figure from a published paper should take 30 seconds. Instead it takes weeks — or fails entirely.

Published biomedical research references custom scripts scattered across GitHub repos, undocumented dependencies, environment-specific configurations, and dead download links. A 2023 study found that **only 26% of computational biology papers could be reproduced** without contacting the authors. Researchers routinely spend weeks recreating a single pipeline. That time should be spent on science.

Meanwhile, general-purpose LLMs (ChatGPT, Claude) generate plausible-looking bioinformatics code that **hallucinates** star allele calls, uses outdated clinical guidelines, and produces results with no audit trail. A pharmacogenomics report from ChatGPT is dangerous — it gets CYP2D6 *4 wrong as "reduced function" when it's actually **no function**. For a patient on codeine, that's the difference between pain relief and zero therapeutic effect.

The biomedical research community needs executable, reproducible, expert-validated pipelines — not PDFs and not LLM hallucinations.

## What ClawBio Does

ClawBio is the **first bioinformatics-native AI agent skill library**, built on OpenClaw. It packages published research methods as installable, composable skills that any user — or any AI agent — can run with a single command.

Instead of cloning repos, debugging dependencies, and reverse-engineering methods sections, you install a skill and run it:

> **python clawbio.py run pharmgx --input my_23andme.txt --output report**
>
> 12 genes. 51 drugs. CPIC guidelines. < 1 second. SHA-256 verified.

**14 production-ready skills** covering:

- **Personal genomics**: PharmGx Reporter (12 genes, 51 drugs, CPIC guidelines), Drug Photo (snap a medication → personalised dosage card from your genotype), NutriGx Advisor (40 SNPs, 13 dietary domains), Genome Comparator, Ancestry PCA
- **Population genetics**: Equity Scorer (HEIM diversity metrics — FST, heterozygosity, representation gaps), GWAS Lookup (federated query across **9 genomic databases** including gnomAD, ClinVar, GTEx, UK Biobank PheWAS), Polygenic Risk Scores (PGS Catalog, 6+ traits)
- **Research infrastructure**: UKB Navigator (semantic search across 22,000+ UK Biobank fields), Metagenomics Profiler (Kraken2/RGI/HUMAnN3), scRNA Orchestrator (Scanpy automation), Semantic Similarity Index (13.1M PubMed abstracts)
- **Orchestration**: Bio Orchestrator routes requests to the right skill by file type, keywords, and analysis intent

Every analysis ships with a **reproducibility bundle**:

| File | Purpose |
|---|---|
| **report.md** | Full analysis with figures and tables |
| **figures/** | Publication-quality PNGs |
| **commands.sh** | Exact commands to reproduce |
| **environment.yml** | Conda environment snapshot |
| **checksums.sha256** | SHA-256 of every input and output file |

A reviewer can reproduce your Figure 3 in 30 seconds without emailing you.

## Architecture

ClawBio is a three-layer system:

**Layer 1 — Bio Orchestrator** (routing layer)

Routes incoming queries to the right specialist skill based on file type, keywords, and analysis intent. A user asks a question or uploads a file; the orchestrator picks the skill.

**Layer 2 — Specialist Skills** (14 production-ready)

| Skill | What it does |
|---|---|
| PharmGx Reporter | 12 genes, 51 drugs, CPIC guidelines |
| Drug Photo | Medication photo to personalised dosage card |
| GWAS Lookup | Federated query across 9 genomic databases |
| Equity Scorer | HEIM diversity metrics across populations |
| Metagenomics Profiler | Kraken2 / RGI / HUMAnN3 pipelines |
| Ancestry PCA | PCA vs SGDP (345 samples, 164 populations) |
| GWAS PRS | Polygenic risk scores from PGS Catalog |
| UKB Navigator | Semantic search across 22,000+ UK Biobank fields |
| NutriGx Advisor | 40 SNPs, 13 dietary domains |
| Genome Comparator | Pairwise IBS + ancestry estimation |
| ClinPGx | Gene-drug lookup from 4 pharmacogenomic databases |
| Profile Report | Unified personal genomic dashboard |
| Semantic Similarity | Disease research equity from 13.1M PubMed abstracts |
| scRNA Orchestrator | Scanpy single-cell RNA-seq automation |

**Layer 3 — Reproducibility + On-Chain Provenance**

Every output includes commands.sh, environment.yml, and checksums.sha256. These SHA-256 hashes are blockchain-ready — publishable to IPFS or any on-chain registry for immutable scientific provenance.

**Core design principles:**

- **Local-first**: Genomic data never leaves the user's machine. No cloud uploads. No data exfiltration. Every skill runs on localhost.
- **Agent-native**: Ships with `llms.txt` (LLM-optimised project summary), `AGENTS.md` (universal agent guide), and `skills/catalog.json` (machine-readable skill index). AI agents can discover, understand, and contribute to ClawBio without human intervention.
- **Composable**: Skills chain — Drug Photo calls PharmGx Reporter; GWAS Lookup feeds Polygenic Risk Scores; Profile Report aggregates all results into a unified genomic dashboard.
- **Reproducible by default**: Every output includes the exact commands, environment, and checksums needed to reproduce it. These SHA-256 hashes are blockchain-ready — publishable to IPFS or any on-chain registry for immutable scientific provenance.

**Technical stack:**

- **Framework**: OpenClaw (180k+ GitHub stars)
- **Language**: Python 3.10+ (pandas, scikit-learn, BioPython, scanpy)
- **APIs**: PubMed/NCBI, GWAS Catalog, gnomAD, ClinVar, Open Targets, Ensembl, GTEx, LDlink, UK Biobank PheWAS, LOVD, PGS Catalog
- **Data**: IHME Global Burden of Disease (175 diseases), CPIC pharmacogenomics guidelines, 13.1M PubMed abstracts (PubMedBERT 768-dim embeddings), SGDP reference panel (345 samples, 164 populations)
- **CI**: GitHub Actions on Python 3.10/3.11/3.12, 57+ tests
- **Provenance**: SHA-256 checksums on all inputs/outputs, designed for on-chain publication via IPFS

## On-Chain Reproducibility (Web3 Integration)

Every ClawBio analysis generates SHA-256 checksums for all input files, output files, and the execution environment. This creates a **tamper-proof provenance chain** that maps directly to blockchain infrastructure:

1. **Analysis runs locally** → produces `checksums.sha256` with hashes of every file
2. **Checksums publish to IPFS** → content-addressed, immutable, decentralised storage
3. **IPFS CID recorded on-chain** → permanent, verifiable proof that this exact analysis produced these exact results
4. **Anyone can verify** → re-run the skill, compare hashes, confirm the chain of custody

This turns every ClawBio report into a **verifiable scientific credential**. Reviewers don't need to trust the author — they verify the hash. Journals don't need to host supplementary data — it's on IPFS. Funding bodies can audit computational claims — the proof is on-chain.

**Why this matters for OpenClaw**: If every OpenClaw skill adopted this pattern, the ecosystem would become a **decentralised registry of verifiable computational research** — a Web3 primitive for science.

## Traction

**ClawBio is one week old.** Published 25 February 2026. Every number below is real, from GitHub Pulse:

| Metric | Value |
|---|---|
| GitHub stars | **140** |
| Forks | **23** |
| Commits | **131** |
| Pull requests | **13** (10 merged) |
| Open issues | **10** |
| Releases | **3** |
| Contributors | **4** (across 3 countries) |
| Page views (14 days) | **5,933** from **2,372 unique visitors** |
| Repo clones (14 days) | **1,547** from **371 unique cloners** |

**In one week:**
- First community PR merged within 48 hours (NutriGx Advisor from @drdaviddelorenzo)
- 3 releases shipped: v0.2.0 (tests + CI + ClawHub), v0.3.0 (Imperial College AI Agent Hack), v0.3.1 (Agent-Friendly — llms.txt, AGENTS.md, catalog.json)
- 21 skills catalogued (14 MVP, 7 planned), growing weekly
- Presented live at the London Bioinformatics Meetup (26 Feb 2026)
- 3 skills published to the OpenClaw package registry (ClawHub)

**Where traffic comes from:**
- LinkedIn: 1,467 views (883 unique) — 62% of all traffic
- Google organic: 522 views (171 unique) — already indexed and ranking
- GitHub internal: 481 views (137 unique)
- Microsoft Teams + Slack: 59 views — people are sharing in work channels

**Most visited pages:** Main repo (2,816 views), `/skills` directory (253 views), PharmGx Reporter (96 views) — visitors drill into the actual skills, not just the README. 371 people cloned it to try it themselves.

## Why It Matters

Published papers should ship as executable skills, not just PDFs.

~7% of people are CYP2D6 Poor Metabolisers — codeine gives them zero pain relief but they keep getting prescribed it. ~0.5% carry DPYD variants where a standard chemotherapy dose can be lethal. These aren't hypothetical risks. ClawBio catches both in under one second from a consumer genetic test that costs £79.

Health equity research is systematically biased toward well-studied European populations. ClawBio's Equity Scorer quantifies that gap across 175 diseases using IHME Global Burden of Disease data — making the invisible visible.

ClawBio makes computational research reproducible by default, lowers the barrier from weeks of setup to a single command, and does it with agentic AI technology that is completely open, free, and community-driven.

## Built With

- OpenClaw framework (180k+ stars)
- Python 3.10+ (pandas, scikit-learn, BioPython, scanpy, matplotlib)
- 9 federated genomic APIs (GWAS Catalog, gnomAD, ClinVar, Open Targets, Ensembl, GTEx, LDlink, UK Biobank PheWAS, LOVD)
- PubMed/NCBI APIs for literature and variant data
- IHME Global Burden of Disease data for equity scoring
- CPIC pharmacogenomics guidelines (51 drugs, 12 genes)
- PGS Catalog (polygenic risk scores)
- PubMedBERT embeddings (13.1M abstracts)
- SGDP reference panel (345 samples, 164 populations)
- GitHub Actions CI (Python 3.10/3.11/3.12)
- SHA-256 reproducibility checksums (IPFS-ready)

## Links

- GitHub: https://github.com/ClawBio/ClawBio
- Organisation: https://github.com/ClawBio
- GitHub Pages: https://clawbio.github.io/ClawBio/
- Slides (London Bioinformatics Meetup): https://clawbio.github.io/ClawBio/slides/
- Latest Release (v0.3.1): https://github.com/ClawBio/ClawBio/releases/tag/v0.3.1
- Video (Demo at Imperial): https://github.com/ClawBio/ClawBio/releases/download/v0.2.0/demo.mp4

---

## Bounty-Specific Notes

### AI Agents for Good ($5,000 USDT — FLock.io)
ClawBio is AI agents for good in healthcare. PharmGx Reporter prevents adverse drug reactions (7% of the population at risk for CYP2D6-related prescribing errors). Equity Scorer makes health research bias measurable across 175 diseases. All local-first, privacy-preserving, open-source. FLock.io's decentralised AI model hub aligns with ClawBio's modular, composable architecture.

### Biodock Inc. ($1,250 USD — BioTrack)
ClawBio is the only bioinformatics-native project in this hackathon. Biodock does deep AI for biological imaging — ClawBio complements this by providing the genomics, pharmacogenomics, and population genetics layer that imaging-based biomarkers ultimately feed into.

### BioHack Bounty (£250 GBP — BioTrack)
Same bio focus. ClawBio's Metagenomics Profiler (Kraken2/RGI/HUMAnN3) and scRNA Orchestrator demonstrate breadth beyond personal genomics into environmental and cellular biology.

### CEO Claw Challenge ($1,000 USD — AfterQuery)
ClawBio demonstrates how a working academic researcher uses OpenClaw agents for real scientific research — not toy demos, but analyses that feed directly into peer-reviewed publications.

### Human for Claw ($500 USD — Imperial Blockchain)
21 skills built by humans packaging domain expertise for the OpenClaw ecosystem. Community PRs from 3 external contributors. AGENTS.md enables AI agents to contribute autonomously.

### Claw for Human ($500 USD — Imperial Blockchain)
Drug Photo: snap a medication photo in Telegram, get a personalised dosage card against your own genotype in seconds. ClawBio's entire value proposition is "Claw serving humans" — making expert genomic analysis accessible to anyone.

### Z.AI General Bounty ($4,000 USD — Z.AI)
Multi-agent orchestration with Bio Orchestrator routing across 14 specialist skills. Agent-native infrastructure (llms.txt, AGENTS.md, catalog.json) as a model for how AI ecosystems should be built.

---

## Demo Script (for March 7 pitch)

**2-3 minutes. Three acts.**

**Act 1 — The Problem (30s)**
"You read a paper. You want to reproduce Figure 3. You clone the repo, fix the Python version, download 2GB from Zenodo — link is dead. You email the author. Three weeks later: still broken. You give up."

**Act 2 — The Solution (90s)**
Live terminal demo:
1. `python clawbio.py list` → show 14 skills in the terminal
2. `python clawbio.py run pharmgx --demo` → personalised drug report in <1 second (highlight: "10 drugs AVOID for this genotype")
3. Show the reproducibility bundle: `commands.sh`, `environment.yml`, `checksums.sha256`
4. "These checksums are IPFS-ready. Publish once, verify forever. That's on-chain science."

**Act 3 — The Impact (30s)**
"ClawBio is one week old. In that week: 153 stars, 23 forks, 2,617 unique visitors, 1,862 people cloned it. 4 contributors across 3 countries. First community PR merged in 48 hours. 21 skills and growing. Papers should ship as executable skills, not PDFs. ClawBio makes that real."

---

## Team

**Manuel Corpas** — Founder & Lead Developer
- Alan Turing Institute Fellow
- Senior Lecturer in Bioinformatics, University of Westminster
- 20+ years in computational genomics
- Built and deployed two AI agents (RoboTerri/Telegram, RoboIsaac/WhatsApp) for daily research operations
- Published researcher with expertise in pharmacogenomics, population genetics, and health equity

**Community Contributors:**
- @jaymoore-research — research infrastructure
- @drdaviddelorenzo — NutriGx Advisor (first community PR)
- @YonghaoZhao722 — scRNA Orchestrator

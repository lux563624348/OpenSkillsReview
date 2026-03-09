# ClawBio Safety Audit: Silent Degradation Fixes

**Date**: 2026-02-28
**Commit**: `bbad73c`
**Scope**: All 4 production skills (PharmGx, Equity Scorer, NutriGx, Metagenomics)

## Background

A community review identified a systematic pattern across ClawBio skills: when encountering missing data, unknown values, or failed operations, the tools silently degraded to "everything is fine" defaults. Missing SNPs became reference-homozygous, unrecognised diplotypes became "Normal (inferred)", and failed subprocess calls became warnings.

This created a systematic bias toward **under-reporting risk and over-reporting normalcy**.

## Audit Methodology

Every function in all four production skills was examined for:
1. Missing input data treated as reference/normal
2. `.get()` defaults that hide missing information
3. `try/except` blocks that swallow errors and return optimistic results
4. Division-by-zero guards that fabricate values
5. Failed subprocesses downgraded to warnings

## Findings: 32 fixes across 4 skills

### PharmGx Reporter (11 fixes)

The most critical skill — drug safety recommendations.

| Severity | Finding | Fix |
|----------|---------|-----|
| **CRITICAL** | Zero PGx SNPs generated a full "all normal" report | Aborts with `sys.exit(1)` |
| **CRITICAL** | Missing SNPs → reference-homozygous (`*1/*1`) | Returns `NOT_TESTED` |
| **CRITICAL** | Missing DPYD → "Normal Metabolizer" (5-FU lethality risk) | Returns `Indeterminate (not genotyped)` |
| **CRITICAL** | Missing CYP2C9/VKORC1 → "Standard warfarin dose" | Returns `indeterminate` with clinical testing recommendation |
| **CRITICAL** | DEL/INS/TA7 variants always counted as 0 copies | Logged warning, variant skipped |
| **HIGH** | Unknown diplotype → "Normal (inferred)" | Returns `Unknown (unmapped diplotype: ...)` |
| **HIGH** | `phenotype_to_key` defaulted to `normal_metabolizer` | Defaults to `indeterminate` |
| **HIGH** | Missing phenotype in drug recs → "Use recommended dose" | Returns "Phenotype not covered by guidelines" |
| **HIGH** | Untested gene → drug silently omitted from report | Shows as `INSUFFICIENT DATA` |
| **HIGH** | Unknown file format → parsing proceeded anyway | Emits stderr warning |
| **MEDIUM** | Partial SNP coverage not indicated in diplotype | Annotated: e.g. `*1/*1 (2/4 SNPs tested)` |

**New features added:**
- `indeterminate` drug category for untested/unmapped genes
- Data Quality Warning section in report header
- Structural variant warnings logged to stderr

### Equity Scorer (7 fixes)

| Severity | Finding | Fix |
|----------|---------|-----|
| **CRITICAL** | 100% UNKNOWN populations scored 0.74/1.0 on representation | Sets to `None` with warning when >50% UNKNOWN |
| **CRITICAL** | CSV pipeline fabricated heterozygosity from hardcoded literature estimates | Labeled `literature_estimate` in report |
| **CRITICAL** | CSV pipeline claimed 100% FST coverage with no FST computed | Set to `0` (no FST computed) |
| **HIGH** | Missing GT field in VCF → used index 0 (wrong field) | Raises `ValueError` |
| **HIGH** | Division-by-zero → fabricated 0.0 allele frequency | Uses `NaN`, downstream uses `nanmean()` |
| **HIGH** | No polymorphic sites → FST = 0.0 ("identical populations") | Returns `NaN` |
| **HIGH** | Unmapped samples silently assigned UNKNOWN | Emits warning with count and percentage |

### NutriGx Advisor (8 fixes)

| Severity | Finding | Fix |
|----------|---------|-----|
| **CRITICAL** | Allele mismatch silently yielded `risk_count=0` (no risk) | Returns `status=allele_mismatch`, `risk_count=None` |
| **CRITICAL** | Zero panel coverage generated full report | Aborts with `sys.exit(1)` |
| **HIGH** | Unexpected `risk_count` values defaulted to 0.0 | Raises `ValueError` |
| **HIGH** | VCF parse errors silently dropped variants | Logged with variant details |
| **HIGH** | Unrecognised file format defaulted to 23andMe | Raises `ValueError` |
| **HIGH** | Missing GT in VCF FORMAT → used index 0 | Skips variant with warning |
| **HIGH** | Missing SNPs excluded from denominator, biasing scores low | Coverage qualifier added: e.g. `3/5 SNPs tested` |
| **MEDIUM** | Unknown domain → generic "no specific recommendation" | Shows `Insufficient genetic data to assess this domain` |

### Metagenomics Profiler (6 fixes)

| Severity | Finding | Fix |
|----------|---------|-----|
| **CRITICAL** | `run_command()` treated all failures as warnings | `critical=True` parameter; Kraken2/RGI raise `RuntimeError` |
| **CRITICAL** | Missing RGI output returned phantom file path | Raises `FileNotFoundError` |
| **CRITICAL** | Missing RGI file → empty DataFrame = "0 ARGs detected" | Reports `ANALYSIS FAILED: Resistome could not be profiled` |
| **HIGH** | Missing HUMAnN3 output returned fabricated path | Returns `None` |
| **HIGH** | Kraken2/Bracken did not verify output files exist | Post-run file existence check added |
| **HIGH** | HUMAnN3 database never validated | Validated like Kraken2; skip with note if missing |

**Report now distinguishes three states:**
- Analysis succeeded (normal output)
- Analysis failed (explicit `FAILED` banner)
- Analysis skipped by user (explicit `skipped` note)

## Design Principle

The core architectural fix: **distinguish "tested and found normal" from "never tested."**

Before this patch, every function in every pipeline treated these two states identically. After this patch:
- Missing data produces `NOT_TESTED`, `Indeterminate`, `NaN`, or `None`
- Reports include explicit Data Quality Warning sections
- Zero-data inputs abort instead of generating misleading reports
- Coverage qualifiers show how much data underlies each result

## Verification

- All 4 skills pass `ast.parse()` syntax validation
- PharmGx demo: 30/30 SNPs, 51 drugs assessed correctly
- PharmGx bad input: aborts with exit code 1 (zero SNPs)
- PharmGx safety regression: 7/7 tests pass (NOT_TESTED, Indeterminate, Unknown, warfarin, indeterminate drugs)
- Equity Scorer VCF demo: HEIM Score 76.2/100 with all figures
- Equity Scorer CSV demo: FST coverage now 0.0 (was 1.0), het labeled as literature estimate
- NutriGx demo: 23/28 SNPs found, 5 allele mismatches correctly flagged
- NutriGx empty input: aborts with exit code 1
- Metagenomics: syntax verified (requires external databases for full run)

---

# Security Audit: Genome Comparator Skill

**Date**: 2026-03-02
**Commit**: `6e1f0e9`
**Scope**: New `genome-compare` skill + integration changes (clawbio.py, orchestrator.py, ci.yml, Makefile, CLAUDE.md, README.md, RoboTerri Telegram bot)

## Background

The genome-compare skill was added for the UK AI Agent Hack demo day (7 March 2026). It compares a user's 23andMe genotype data against George Church's public PGP-1 genome via Identity By State (IBS) and estimates continental ancestry via EM admixture. Demo patient is Manuel Corpas (PGP-UK uk6D0CFA). Four parallel security audits were conducted: genome_compare.py, integration files, RoboTerri Telegram bot, and data files.

## Audit Methodology

Every file added or modified on 2026-03-02 was examined for:
1. Network exfiltration (HTTP requests, socket connections, cloud SDK usage)
2. Command injection (subprocess, os.system, eval, exec)
3. Path traversal (user-supplied paths escaping intended directories)
4. Deserialization attacks (pickle, unsafe YAML, custom decoders)
5. Denial of service (unbounded memory, infinite loops, missing timeouts)
6. Information leakage (system paths, credentials, raw genotypes in output)
7. Input validation (malformed files, schema validation, boundary checks)
8. Data file integrity (zip bombs, polyglots, embedded scripts)
9. Genetic data privacy (raw genotypes vs aggregate statistics)
10. CI/CD pipeline safety (dependency pinning, permissions)

## Positive Security Properties

These are intentional design decisions that eliminate entire vulnerability classes:

| ID | Property | Details |
|----|----------|---------|
| GOOD-01 | **No network activity** | `genome_compare.py` imports zero HTTP/socket/cloud libraries. All processing is local. Genetic data never leaves the machine. |
| GOOD-02 | **No command injection surface** | No `subprocess`, `os.system()`, `eval()`, or `exec()` in the skill script. Pure Python computation + stdlib file I/O. |
| GOOD-03 | **No dangerous deserialization** | Only `json.load()` (safe) and `gzip.open()` (safe). No pickle, no unsafe YAML. |
| GOOD-04 | **No credential exposure** | No environment variables, API keys, tokens, or `.env` files read. |
| GOOD-05 | **Subprocess uses list form** | `clawbio.py` uses `subprocess.run(cmd, ...)` with a list (not `shell=True`). RoboTerri uses `asyncio.create_subprocess_exec` (not `create_subprocess_shell`). |
| GOOD-06 | **Defensive parsing** | 23andMe parser skips blank lines, comments, short lines, non-rsID entries, and handles missing genotypes gracefully. |
| GOOD-07 | **Numerical stability** | EM algorithm uses log-sum-exp normalisation, clips frequencies to [0.001, 0.999], and converges via `np.allclose(atol=1e-7)`. |
| GOOD-08 | **Bounded iteration** | EM loop hard-capped at 200 iterations. |
| GOOD-09 | **Matplotlib Agg backend** | All plots force non-interactive `Agg` backend with graceful `ImportError` fallback. |
| GOOD-10 | **Proper file handle management** | All file opens use `with` statements. |
| GOOD-11 | **Trusted dependency chain** | Only external dep is `numpy`. `matplotlib` optional. All others are stdlib. |
| GOOD-12 | **No raw genotypes in report** | Report contains only aggregate statistics (IBS scores, ancestry %). Individual SNP genotypes are never written to output. |
| GOOD-13 | **Data files verified clean** | Both `.gz` files pass `gzip -t`, have valid magic bytes (`1f 8b`), 2.9x compression ratio (no zip bomb), zero trailing bytes (no polyglot). AIMs panel JSON has no embedded scripts, URLs, or executable patterns. |

## Findings: 20 items across 4 audit areas

### genome_compare.py (10 findings)

| Severity | ID | Category | Finding | Lines | Recommendation |
|----------|----|----------|---------|-------|----------------|
| **MEDIUM** | GC-001 | Path Traversal | `--output` writes to arbitrary filesystem location via `mkdir(parents=True)` | 742, 859 | Validate output resolves within allowed root |
| LOW | GC-002 | Path Traversal | `--input`, `--reference`, `--aims-panel` read from arbitrary paths | 854-861 | Add path validation if ever exposed as a service |
| LOW | GC-003 | Info Leakage | Input filename and SHA-256 prefix exposed in report | 548, 709 | Allow `--label` flag for anonymised reports |
| LOW | GC-004 | DoS | No upper bound on input file size / line count | 79-100 | Add `MAX_LINES = 10_000_000` check |
| LOW | GC-005 | Input Validation | Invalid files produce empty reports silently (no minimum SNP check) | 79-100 | Warn if `<1,000` SNPs parsed |
| INFO | GC-006 | Input Validation | AIMs panel JSON not schema-validated; missing keys raise raw `KeyError` | 196-200 | Wrap in try/except with user-friendly message |
| INFO | GC-007 | Filesystem | `mkdir(parents=True, exist_ok=True)` creates arbitrary directory trees | 742, 745 | See GC-001 |
| LOW | GC-008 | Exception Handling | `except Exception` in figure generation masks serious errors | 816-817 | Log full traceback; re-raise for `PermissionError`, `OSError` |
| INFO | GC-009 | Division by Zero | `n_concordant/n_overlap` at line 558 if `n_overlap == 0` | 558 | Add `if n_overlap > 0` guard |
| INFO | GC-010 | DoS (positive) | EM iteration properly bounded at 200 with convergence check | 297, 324 | No action needed |

### Integration Files (5 findings)

| Severity | ID | Category | Finding | File | Lines | Recommendation |
|----------|-----|----------|---------|------|-------|----------------|
| ~~**HIGH**~~ **FIXED** | INT-001 | Command Injection | `extra_args` passes arbitrary CLI flags to subprocess unfiltered | clawbio.py | 174-175 | **Fixed**: per-skill `allowed_extra_flags` allowlist; core flags (`--input`, `--output`, `--demo`) always blocked |
| ~~**HIGH**~~ **FIXED** | INT-002 | Path Traversal | Orchestrator `--skill` arg concatenated to path without validation | orchestrator.py | 199 | **Fixed**: rejects `/`, `\`, `..` in skill name + `resolve()` check that path stays within `SKILLS_DIR` |
| **MEDIUM** | INT-003 | Info Disclosure | Error messages include full filesystem paths, sent to Telegram | clawbio.py | 129, 138, 209 | Sanitize paths before returning to external channels |
| LOW | INT-004 | Keyword Collision | `"compare"` and `"ibs"` are overly broad orchestrator keywords | orchestrator.py | 67-72 | Use multi-word keywords; add word-boundary matching |
| LOW | INT-005 | CI Pipeline | Dependencies not pinned; `permissions:` not restricted | ci.yml | 25-28 | Pin versions; add `permissions: contents: read` |

### RoboTerri Telegram Bot (5 findings)

| Severity | ID | Category | Finding | Lines | Recommendation |
|----------|-----|----------|---------|-------|----------------|
| ~~**HIGH**~~ **FIXED** | TG-001 | Code Injection | PDF extraction embeds `tmp_path` (with user filename) into `python -c` f-string | 2819-2832 | **Fixed**: path passed as `sys.argv[1]`, never embedded in code string |
| **MEDIUM** | TG-002 | Path Traversal | Telegram filename used unsanitized in temp path construction | 2800-2804 | `re.sub(r'[/\\]', '_', Path(filename).name)` |
| **MEDIUM** | TG-003 | Authorisation | `_received_files` takes first file regardless of `chat_id` | 1916-1918 | Scope file access by `chat_id` |
| **MEDIUM** | TG-004 | DoS | No file size or type validation before passing to skill subprocess | 1957-1964 | Add 50MB limit and extension allowlist |
| LOW | TG-005 | Info Disclosure | Absolute server paths sent to Telegram chat | 2015-2016 | Use relative path or directory name only |

### Data Files (0 actionable findings)

| Status | File | Details |
|--------|------|---------|
| CLEAN | `george_church_23andme.txt.gz` | Valid gzip, 4.8MB, 569K SNPs, CC0 |
| CLEAN | `manuel_corpas_23andme.txt.gz` | Valid gzip, 4.8MB, 576K SNPs, CC0 |
| CLEAN | `aims_panel.json` | Valid JSON, 65 markers, no scripts/URLs |
| CLEAN | `manuel_ancestry.json` | Valid JSON, 1 URL (PGP-UK profile — legitimate provenance) |
| CLEAN | `test_genome_compare.py` | No eval/exec/subprocess, no network access, deterministic inputs |

## Summary by Severity

| Severity | Count | IDs |
|----------|-------|-----|
| ~~**HIGH**~~ **FIXED** | 3 | INT-001, INT-002, TG-001 (all fixed 2026-03-02) |
| **MEDIUM** | 5 | GC-001, INT-003, TG-002, TG-003, TG-004 |
| **LOW** | 7 | GC-002, GC-003, GC-004, GC-005, GC-008, INT-004, INT-005, TG-005 |
| **INFO** | 4 | GC-006, GC-007, GC-009, GC-010 |

**Note**: TG-001 (PDF f-string injection) and INT-001 (`extra_args` passthrough) are pre-existing patterns, not introduced by the genome-compare commit. They are documented here because they affect the genome-compare execution path.

## Priority Remediation

1. ~~**Immediate** — TG-001: Fix PDF extraction code injection~~ **FIXED 2026-03-02**
2. ~~**Immediate** — INT-001: Allowlist `extra_args` per skill~~ **FIXED 2026-03-02**
3. ~~**Immediate** — INT-002: Validate skill names contain no path separators~~ **FIXED 2026-03-02**
4. **Short-term** — TG-002, TG-003, TG-004: Sanitize filenames, scope files by chat, add size limits
5. **Short-term** — INT-003: Redact filesystem paths from error messages sent to Telegram
6. **Maintenance** — GC-001 through GC-009: Hardening for service deployment

## Overall Assessment

The genome-compare skill itself is **well-written and security-conscious**. Its most important property is what it does NOT do: no subprocess calls, no network access, no dangerous deserialization, no credential handling. The attack surface is very small. All HIGH findings (INT-001, INT-002, TG-001) are in the surrounding infrastructure (clawbio.py runner, orchestrator, Telegram bot) rather than in the skill code itself.

**Risk rating for genome_compare.py**: Low. No critical or high findings.
**Risk rating for integration path**: Medium. Three HIGH findings in surrounding code.

---

## Disclaimer

ClawBio is a **research and educational tool**. It is not a medical device and does not provide clinical diagnoses. Consult a healthcare professional before making any medical decisions based on genetic data.

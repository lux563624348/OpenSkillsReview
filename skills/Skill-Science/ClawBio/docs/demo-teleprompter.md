# ClawBio Demo — Teleprompter Script (FLock Track)

> Total time: ~3 minutes
> Setup: Zoom recording, screen share your terminal, face in corner
> Have: terminal ready at ClawBio repo root, phone with Telegram (RoboTerri) ready
> Font size: Cmd+ a few times so terminal text is large

---

## BEFORE YOU HIT RECORD

Run these once to warm up:
```bash
cd /path/to/ClawBio
export FLOCK_API_KEY=<your-key>   # set this BEFORE you start recording
python3 clawbio.py list
python3 clawbio.py run pharmgx --demo --output /tmp/warmup
python3 skills/bio-orchestrator/orchestrator.py --input "what drugs should I avoid with my genotype" --provider flock --output /tmp/warmup2
```

Also: send a test message to RoboTerri on Telegram to make sure it's responding.

Delete warmup outputs, clear terminal, hit record.

---

## FLock Track Checklist (all 5 must appear)

- [ ] OpenClaw agent framework
- [ ] SDG-aligned with measurable impact
- [ ] FLock API for open-source model inference
- [ ] Open-source models only
- [ ] Multi-channel deployment (Telegram + WhatsApp)

---

## ACT 1 — THE PROBLEM + SDG FRAMING (25 seconds)

> [Look at camera, no screen share yet]

SAY:

"7 percent of people are poor metabolisers for a gene called CYP2D6.
Codeine gives them zero pain relief — but they keep getting prescribed it.
Half a percent carry DPYD variants where standard chemotherapy can be lethal.

These are UN Sustainable Development Goal 3 problems — good health and well-being.
And they're solvable today, from a consumer genetic test that costs 79 pounds.

ClawBio is an open-source AI agent skill library, built on OpenClaw,
that makes this kind of genomic analysis reproducible, local-first, and free."

---

## ACT 2 — THE SKILLS (15 seconds)

> [Switch to screen share — terminal visible]

TYPE:
```bash
python3 clawbio.py list
```

SAY:

"21 skills. 14 production-ready. One week old.
Pharmacogenomics. Health equity. Metagenomics. Single-cell RNA-seq.
Every skill runs locally — your genomic data never leaves your machine."

---

## ACT 3 — PHARMGX DEMO (35 seconds)

TYPE:
```bash
python3 clawbio.py run pharmgx --demo
```

> [Wait for output — ~1 second]

SAY:

"Full pharmacogenomics report from a 23andMe file.
12 genes. 51 drugs. CPIC clinical guidelines. Under one second.

Look at the drug summary — this patient has drugs to AVOID,
20 to use with caution, and 30 at standard dosing.

Every output ships with a reproducibility bundle —
commands.sh, environment.yml, and SHA-256 checksums.
A reviewer can reproduce this result in 30 seconds."

---

## ACT 4 — FLOCK INTELLIGENT ROUTING (35 seconds)

SAY:

"Now — what happens when someone asks a plain English question?
We route it through FLock's open-source AI."

TYPE:
```bash
python3 skills/bio-orchestrator/orchestrator.py --input "what drugs should I avoid with my genotype" --provider flock --output /tmp/demo_flock
```

> [Wait for output — "FLock routed to: pharmgx-reporter, 95% confidence"]

SAY:

"FLock routes to pharmgx-reporter at 95 percent confidence.
Open-source model. No proprietary APIs. Through FLock's inference platform."

TYPE:
```bash
python3 skills/bio-orchestrator/orchestrator.py --input "how diverse is my biobank cohort" --provider flock --output /tmp/demo_flock2
```

SAY:

"Different question — routes to equity-scorer.
The orchestrator understands bioinformatics intent
and picks the right skill every time."

---

## ACT 5 — MULTI-CHANNEL: TELEGRAM + WHATSAPP (30 seconds)

> [Show your phone screen, or switch to a Telegram screenshot/screen share]

SAY:

"ClawBio doesn't just run in the terminal.
Here's RoboTerri — our Telegram agent.
It runs the same 14 skills over chat.

Send a photo of a medication — it identifies the drug,
checks your genotype, and returns a personalised dosage card.
All on your phone. All local-first.

We also have RoboIsaac on WhatsApp — same skills, different channel.
Two production agents, already live, already serving users."

> [If you can show a quick Telegram interaction, do it here.
> Otherwise, show a screenshot of a previous RoboTerri conversation
> where it returned a PharmGx or Drug Photo result.]

---

## ACT 6 — THE CLOSE (20 seconds)

> [Look at camera]

SAY:

"ClawBio is one week old.
153 stars. 23 forks. 2,617 unique visitors. 1,862 people cloned it.
4 contributors across 3 countries.

Built on OpenClaw. Powered by FLock.
Deployed on Telegram and WhatsApp.
Targeting SDG 3 — good health — and SDG 10 — reduced inequalities.

Papers should ship as executable skills, not PDFs.
ClawBio makes that real."

> [End recording]

---

## AFTER RECORDING

1. Upload to YouTube
2. Update DoraHacks Demo video field with the new YouTube link
3. Apply to the FLock "AI Agents for Good" bounty

---

## CRITERIA COVERAGE CHECK

| FLock Requirement | Where in demo |
|---|---|
| OpenClaw agent framework | Act 1 intro + Act 2 skill list |
| SDG-aligned, measurable impact | Act 1 (SDG 3 + SDG 10), Act 3 (drug safety) |
| FLock API for open-source model inference | Act 4 (two live FLock routing calls) |
| Open-source models only | Act 4 ("no proprietary APIs") |
| Multi-channel deployment | Act 5 (Telegram + WhatsApp) |

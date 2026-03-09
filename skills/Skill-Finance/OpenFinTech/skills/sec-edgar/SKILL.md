---
name: sec-edgar
description: Retrieve SEC EDGAR filings metadata and XBRL data using the SEC data API with proper User-Agent compliance.
---

# SEC EDGAR Skill

## When to use

Use this skill when the user asks for:
- Official filings (10-K, 10-Q, 8-K) or filing metadata.
- Audited financial figures from company filings.
- XBRL company facts or standardized line items.

## Key rules

- SEC requires a descriptive `User-Agent` header with contact info.
- Respect rate limits. Space requests and avoid bulk scraping.
- Always normalize CIKs to 10 digits (zero-padded).

## Quick start

```python
import requests

headers = {
    "User-Agent": "Your Name (your.email@domain.com)",
    "Accept-Encoding": "gzip, deflate",
}

# Company submissions (filing history)
ciK = "0000320193"  # Apple
submissions_url = f"https://data.sec.gov/submissions/CIK{ciK}.json"
submissions = requests.get(submissions_url, headers=headers).json()

# Company facts (XBRL line items)
facts_url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{ciK}.json"
facts = requests.get(facts_url, headers=headers).json()
```

## Useful endpoints

- Submissions: `https://data.sec.gov/submissions/CIK{cik}.json`
- Company facts: `https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json`
- XBRL frames: `https://data.sec.gov/api/xbrl/frames/{taxonomy}/{tag}/{unit}/{year}.json`

## Pitfalls

- Filings are reported in different units. Always check `unit` in XBRL data.
- CIKs must be zero-padded to 10 digits.
- Some companies have multiple classes or amended filings; filter by form and accession number.

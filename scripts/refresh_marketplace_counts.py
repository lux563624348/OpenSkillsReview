#!/usr/bin/env python3
"""Fetch the latest skill counts for marketplaces referenced by the deep research report."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import json
import logging
import re
import sys
from typing import Iterable, List, Optional

import requests

OUTPUT_PATH = Path("data/marketplace_counts.json")
REQUEST_TIMEOUT = 30

@dataclass
class Marketplace:
    name: str
    url: str
    patterns: List[str]
    context: str

MARKETPLACES: Iterable[Marketplace] = [
    Marketplace(
        name="SkillsMP (Agent Skills Marketplace)",
        url="https://skillsmp.com",
        patterns=[
            r"Total\s+Skills\s*([0-9,]+)",
            r"([0-9,]+)\s+skills\s+on\s+SkillsMP",
        ],
        context="SkillsMP reports a global “Total Skills” value on the timeline/search page.",
    ),
    Marketplace(
        name="clawhub.ai/skills",
        url="https://clawhub.ai/skills",
        patterns=[
            r"([0-9,]+)\+?\s+skills",
            r"Skills\s*\(?([0-9,]+)\)?",
        ],
        context="The skills directory page highlights the total number of published skills.",
    ),
    Marketplace(
        name="anthropics/skills",
        url="https://github.com/anthropics/skills",
        patterns=[
            r"([0-9,]+)\+?\s+skills",
            r"([\d,]+)\s+skill[s]?\s+for\s+Claude",
        ],
        context="Repository docs and metadata may reference the total number of bundled skills.",
    ),
    Marketplace(
        name="Agent Skills Directory",
        url="https://www.skillsdirectory.org",
        patterns=[
            r"([\d,]+)\s+unique skills",
            r"([\d,]+)\s+indexed skill files",
            r"Total skills\s*[:\-]?\s*([\d,]+)",
        ],
        context="The landing page highlights unique skills vs. indexed files.",
    ),
    Marketplace(
        name="agentskill.sh",
        url="https://agentskill.sh",
        patterns=[
            r"Find\s+and\s+install\s+([\d,]+)\+?\s+skills",
            r"([\d,]+)\+?\s+skills",
        ],
        context="The homepage callout is the primary counter.",
    ),
    Marketplace(
        name="skills.sh",
        url="https://skills.sh",
        patterns=[
            r"All\s+Time\s*\(?([\d,]+)\)?",
            r"([\d,]+)\s+skills\s+in\s+the\s+leaderboard",
        ],
        context="Leaderboard stats include the “All Time” total.",
    ),
    Marketplace(
        name="MCP Market – Skills",
        url="https://mcpmarket.com/tools/skills",
        patterns=[
            r"([\d,]+)\s+Skills",
            r"([\d,]+)\s+skill\s+entries",
        ],
        context="The Tools / Skills section exposes a tally near the top.",
    ),
    Marketplace(
        name="AwesomeSkill.ai",
        url="https://awesomeskill.ai",
        patterns=[
            r"([\d,]+)\+\s+skills",
            r"([\d,]+)\s+skills",
        ],
        context="Header copy promises a 50,000+ skill catalogue.",
    ),
    Marketplace(
        name="AgentSkills Directory",
        url="https://agentskills.to/skills",
        patterns=[
            r"Discover\s+([0-9KMk\+]+)\s+skills",
            r"([0-9KMk\+]+)\s+Skills",
        ],
        context="Category headline and hero callouts show the count.",
    ),
    Marketplace(
        name="LobeHub",
        url="https://lobehub.com/bg/skills",
        patterns=[
            r"([0-9,]+)\+?\s+skills",
            r"([\d,]+)\s+Skills",
        ],
        context="The skills catalog view typically surfaces a total listing count.",
    ),
    Marketplace(
        name="prompts.chat",
        url="https://prompts.chat",
        patterns=[
            r"([\d,]+)\s+found\s+<\/span>.*?Skills",
            r"([\d,]+)\s+found\s+Prompts",
        ],
        context="Separate counters for skills and prompts appear on the site.",
    ),
    Marketplace(
        name="K-Dense-AI/scientific-skills",
        url="https://github.com/K-Dense-AI/claude-scientific-skills",
        patterns=[
            r"([0-9,]+)\+?\s+skills",
            r"([\d,]+)\s+scientific\s+skills",
        ],
        context="Repository docs may advertise the number of scientific skills included.",
    ),
    Marketplace(
        name="agent-skills.cc",
        url="https://agent-skills.cc/",
        patterns=[
            r"([0-9,]+)\+?\s+skills",
            r"([\d,]+)\s+AI\s+skills",
        ],
        context="Homepage hero text includes an aggregate skill counter.",
    ),
    Marketplace(
        name="awesomeskills.dev (curated)",
        url="https://awesomeskills.dev",
        patterns=[
            r"View\s+all\s+([\d,]+)\s+skills",
            r"([0-9,]+)\s+skills\s+→",
        ],
        context="Curated list links to the total number of verified skills.",
    ),
    Marketplace(
        name="AgentSkillsHub",
        url="https://agentskillshub.dev/",
        patterns=[
            r"([0-9,]+)\+?\s+skills",
            r"([\d,]+)\s+verified\s+skills",
        ],
        context="Landing page text may expose a curated skill total.",
    ),
    Marketplace(
        name="Awesome Claude Skills",
        url="https://awesome-skills.com",
        patterns=[
            r"Discover\s+([0-9,]+)\+",
        ],
        context="Metadata includes a “122+” curated skill count.",
    ),
    Marketplace(
        name="Skill Registry",
        url="https://skillregistry.io/",
        patterns=[
            r"([0-9,]+)\+?\s+skills",
            r"([\d,]+)\s+registered\s+skills",
        ],
        context="Directory summary or hero stats may display a total registered-skill count.",
    ),
]


def fetch_page(url: str) -> Optional[str]:
    try:
        response = requests.get(url, timeout=REQUEST_TIMEOUT, headers={"User-Agent": "OpenSkillsReview/1.0"})
        response.raise_for_status()
        return response.text
    except requests.RequestException as err:
        logging.warning("Failed to fetch %s: %s", url, err)
        return None


def extract_value(content: str, patterns: Iterable[str]) -> Optional[str]:
    for pattern in patterns:
        match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
        if match:
            raw = match.group(1)
            return raw.strip()
    return None


def normalize(raw_value: Optional[str]) -> Optional[str]:
    if not raw_value:
        return None
    normalized = raw_value.replace(",", "").replace(" ", "")
    return normalized


def refresh_counts() -> dict:
    results = []
    for marketplace in MARKETPLACES:
        logging.info("Checking %s", marketplace.name)
        content = fetch_page(marketplace.url)
        value = None
        if content:
            value = extract_value(content, marketplace.patterns)
        results.append(
            {
                "name": marketplace.name,
                "url": marketplace.url,
                "context": marketplace.context,
                "count": normalize(value),
                "raw_match": value,
            }
        )
    return {
        "timestamp": datetime.now().isoformat(),
        "entries": results,
    }


def write_payload(payload: dict) -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(payload, indent=2))
    logging.info("Wrote latest counts to %s", OUTPUT_PATH)


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    payload = refresh_counts()
    write_payload(payload)


if __name__ == "__main__":
    main()

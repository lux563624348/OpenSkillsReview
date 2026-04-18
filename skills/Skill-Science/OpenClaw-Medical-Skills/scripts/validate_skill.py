#!/usr/bin/env python3
"""
Quick validation script for skills - minimal version
"""

import re
from pathlib import Path

import yaml

def validate_skill(skill_path):
    """Basic validation of a skill"""
    skill_path = Path(skill_path)

    # Check that it's a directory containing SKILL.md
    skill_md = skill_path / 'SKILL.md'
    if not skill_path.is_dir() or not skill_md.exists():
        return False, "SKILL.md not found in directory"

    # Read and validate frontmatter
    content = skill_md.read_text(encoding='utf-8', errors='replace')
    # Allow frontmatter block to appear anywhere in the file
    match = re.search(r'(?m)^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return False, "Invalid frontmatter format"

    frontmatter_text = match.group(1)

    # Parse YAML frontmatter
    try:
        frontmatter = yaml.safe_load(frontmatter_text)
        if not isinstance(frontmatter, dict):
            return False, "Frontmatter must be a YAML dictionary"
    except yaml.YAMLError as e:
        return False, f"Invalid YAML in frontmatter: {e}"

    # Required fields: other frontmatter keys are allowed.
    if 'name' not in frontmatter:
        return False, "Missing 'name' in frontmatter"
    if 'description' not in frontmatter:
        return False, "Missing 'description' in frontmatter"

    # Extract name for validation
    name = frontmatter.get('name', '')
    if not isinstance(name, str):
        return False, f"Name must be a string, got {type(name).__name__}"
    name = name.strip()
    if name:
        # Check naming convention (kebab-case: lowercase with hyphens)
        if not re.match(r'^[a-z0-9-]+$', name):
            return False, f"Name '{name}' should be kebab-case (lowercase letters, digits, and hyphens only)"
        if name.startswith('-') or name.endswith('-') or '--' in name:
            return False, f"Name '{name}' cannot start/end with hyphen or contain consecutive hyphens"
        # Check name length (max 64 characters per spec)
        if len(name) > 64:
            return False, f"Name is too long ({len(name)} characters). Maximum is 64 characters."

    # Extract and validate description
    description = frontmatter.get('description', '')
    if not isinstance(description, str):
        return False, f"Description must be a string, got {type(description).__name__}"
    description = description.strip()

    return True, "Skill is valid!"

if __name__ == "__main__":
    import sys
    import json
    import os

    if len(sys.argv) != 2:
        print("Usage: validate_skill.py <path/to/skill_dir> OR validate_skill.py openclaw.plugin.json", file=sys.stderr)
        raise SystemExit(2)

    target = sys.argv[1]

    if target.endswith('openclaw.plugin.json'):
        try:
            with open(target, 'r') as f:
                manifest = json.load(f)
            assert 'id' in manifest, "Missing 'id' in manifest"
            assert 'skills' in manifest, "Missing 'skills' array in manifest"
            missing = [s for s in manifest['skills'] if not os.path.isdir(s)]
            if missing:
                print(f"Missing skill directories: {missing[:5]} (Total {len(missing)} missing)", file=sys.stderr)
                raise SystemExit(1)
            print(f"✅ Manifest valid, found {len(manifest['skills'])} skills")
            raise SystemExit(0)
        except Exception as e:
            print(f"Error validating manifest: {e}", file=sys.stderr)
            raise SystemExit(1)

    ok, msg = validate_skill(target)
    if ok:
        print(msg)
        raise SystemExit(0)
    else:
        print(msg, file=sys.stderr)
        raise SystemExit(1)
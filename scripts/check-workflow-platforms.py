#!/usr/bin/env python3
"""Reject disallowed runner references in GitHub Actions workflows."""

import re
import sys
from pathlib import Path


root = Path.cwd()
workflows = root / ".github" / "workflows"
if not workflows.is_dir():
    sys.exit(f"Workflow directory not found: {workflows}")

files = sorted((*workflows.glob("*.yml"), *workflows.glob("*.yaml")))
if not files:
    sys.exit(f"No workflow files found in {workflows}")

disallowed = re.compile("windows", re.IGNORECASE)
violations = 0
for path in files:
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if disallowed.search(line):
            print(f"{path.relative_to(root)}:{line_number}: disallowed platform reference", file=sys.stderr)
            violations += 1

if violations:
    sys.exit(1)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify_brahmand_canon.py
Comprehensive Canon Verification & Orthography Audit Suite for Bramhand.
Enforces all user rules, canonical locks, and orthographic constraints across all markdown files.
"""

import os
import re
import sys
from pathlib import Path

# Force UTF-8 stdout for Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = Path(__file__).resolve().parent.parent

# User and Canon Rules
BANNED_BINDI_NAHI = "नहीं"  # Must be 0 everywhere! Always 'नही'

BANNED_WORDS = [
    "status window",
    "blue screen",
    "hp bar",
    "mp bar",
    "level up",
    "leveling up",
    "dungeon core",
    "mana circuit",
    "dantian",
    "cultivation realm",
    "quest notification",
    "gamer system",
    "nadi 43,200",
    "खंदक-युद्ध",
    "श्वसन-मास्क",
    "८-तास रोटेशन",
    "हिल्डा",
    "वोल्फगांग",
    "सायलास",
    "लिनिया",
    "बीट्रिस व्हेनेझ्झा"
]

BANNED_MODERN = [
    "dadar",
    "worli",
    "mumbai",
    "smartphone",
    "vada pav",
    "rupee",
    "₹"
]

# Strict objective world-building directories where modern earth references and protagonist leaks are banned
OBJECTIVE_WORLD_DIRS = {"01_WORLD_BIBLE", "02_POWER_SYSTEM"}

# Protagonist files where Neel & RITA are canonically documented
PROTAGONIST_CANON_FILES = {
    "00_Season_1_Protagonist_Index.md",
    "02_Neel_Canonical_Dossier.md",
    "04_Rita_Canonical_Dossier.md",
    "05_Neel_Rita_Master_Lexicon_and_Style_Library.md",
    "02_Volume_1_Central_City_Arc.md"
}

def scan_file(file_path):
    issues = []
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        lines = content.splitlines()

    # 1. Check Bindi Nahi (Strict 0 across all files, everywhere)
    bin_matches = [i + 1 for i, line in enumerate(lines) if BANNED_BINDI_NAHI in line]
    if bin_matches:
        issues.append(f"VIOLATION: Found 'नहीं' with bindi on lines: {bin_matches}")

    rel_parts = file_path.relative_to(ROOT_DIR).parts
    is_objective_world = len(rel_parts) > 1 and rel_parts[0] in OBJECTIVE_WORLD_DIRS
    file_name = file_path.name

    # 2. Check Objective World Bible for modern leaks or Neel
    if is_objective_world:
        neel_matches = [i + 1 for i, line in enumerate(lines) if re.search(r'\bNeel\b', line, re.IGNORECASE)]
        if neel_matches:
            issues.append(f"VIOLATION: Found 'Neel' in objective world bible on lines: {neel_matches}")

        for mword in BANNED_MODERN:
            mword_matches = [i + 1 for i, line in enumerate(lines) if mword.lower() in line.lower()]
            if mword_matches:
                issues.append(f"VIOLATION: Found modern artifact '{mword}' in world bible on lines: {mword_matches}")

        for bword in BANNED_WORDS:
            bword_matches = [i + 1 for i, line in enumerate(lines) if bword.lower() in line.lower()]
            if bword_matches:
                issues.append(f"VIOLATION: Found banned term '{bword}' in world bible on lines: {bword_matches}")

    # 3. Check 129 Character Dossiers (excluding protagonist-specific files)
    elif len(rel_parts) > 1 and rel_parts[0] == "03_CHARACTERS" and file_name not in PROTAGONIST_CANON_FILES:
        for bword in BANNED_WORDS:
            bword_matches = [i + 1 for i, line in enumerate(lines) if bword.lower() in line.lower()]
            if bword_matches:
                issues.append(f"VIOLATION: Found banned term '{bword}' on lines: {bword_matches}")

    return issues

def verify_all():
    print("=" * 80)
    print("  BRAMHAND — THE 3-HEADED COSMOS: CANON & QUALITY VERIFICATION SUITE")
    print("=" * 80)
    print(f"Target Root Directory: {ROOT_DIR}\n")

    md_files = sorted(list(ROOT_DIR.glob("**/*.md")))
    print(f"Discovered {len(md_files)} Markdown files across production directories:\n")

    total_violations = 0

    for md_path in md_files:
        rel_path = md_path.relative_to(ROOT_DIR)
        issues = scan_file(md_path)
        if issues:
            print(f"[FAIL] {rel_path} ({len(issues)} violations):")
            for iss in issues:
                print(f"       - {iss}")
            total_violations += len(issues)
        else:
            size_kb = md_path.stat().st_size / 1024
            print(f"[PASS] {rel_path} ({size_kb:.1f} KB) — 100% Clean")

    print("\n" + "-" * 80)
    print("SPECIAL CHECK: 129 Character Roster Count")
    print("-" * 80)

    roster_file = ROOT_DIR / "03_CHARACTERS" / "01_Character_Master_Sheet_129.md"
    if roster_file.exists():
        with open(roster_file, "r", encoding="utf-8") as f:
            roster_text = f.read()
        char_ids = re.findall(r'\*\*CHR-[A-Z]+-\d+[A-Z]?\*\*', roster_text)
        print(f"Found {len(char_ids)} bold canonical IDs in Master Index Table.")
        if len(char_ids) == 129:
            print("[PASS] Master Index Table matches exact 129 canonical count!")
        else:
            print(f"[WARNING] Expected 129 IDs, found {len(char_ids)}.")
            total_violations += 1
    else:
        print("[FAIL] 01_Character_Master_Sheet_129.md not found!")
        total_violations += 1

    print("\n" + "=" * 80)
    if total_violations == 0:
        print("  ALL CANONICAL TESTS PASSED! ZERO VIOLATIONS! (100% GREEN)")
    else:
        print(f"  VERIFICATION FAILED: {total_violations} TOTAL VIOLATIONS DETECTED!")
    print("=" * 80)
    return total_violations

if __name__ == "__main__":
    sys.exit(verify_all())

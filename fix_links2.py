#!/usr/bin/env python3
"""Second-pass link fixer: slug-based fuzzy matching for remaining (#) links."""

import os
import re
import glob

CONTENT_DIR = "src/content/questions"

# Build slug set from all MDX files
all_slugs = set()
mdx_files = glob.glob(f"{CONTENT_DIR}/**/*.mdx", recursive=True)

for filepath in mdx_files:
    with open(filepath, "r") as f:
        content = f.read()
    slug_match = re.search(r'^slug:\s*["\'](.+?)["\']', content, re.MULTILINE)
    if slug_match:
        all_slugs.add(slug_match.group(1))

print(f"Loaded {len(all_slugs)} slugs")

# CTA-style links to skip (no target page)
CTA_PATTERNS = [
    r'^see how .+ works? →?$',
    r'^start .+ →?$',
    r'^talk to .+ →?$',
    r'^taxcloud\.com$',
    r'^see if .+ →?$',
    r'^start here →?$',
]

def is_cta(text):
    t = text.lower().strip()
    for pat in CTA_PATTERNS:
        if re.match(pat, t):
            return True
    return False

def text_to_slug_candidate(text):
    """Convert link text to slug format for matching."""
    s = text.lower()
    # Remove trailing arrow/extra text
    s = re.sub(r'\s*→.*$', '', s)
    # Remove trailing punctuation
    s = re.sub(r'[?!.,;:]+$', '', s)
    # Remove parenthetical qualifiers like "(CSP)"
    s = re.sub(r'\s*\([^)]+\)', '', s)
    s = s.strip()
    # Replace spaces and special chars with hyphens
    s = re.sub(r'[^\w\s-]', '', s)
    s = re.sub(r'[\s_]+', '-', s)
    s = re.sub(r'-+', '-', s)
    s = s.strip('-')
    return s

def find_slug(link_text):
    """Try to find a matching slug for this link text."""
    if is_cta(link_text):
        return None

    candidate = text_to_slug_candidate(link_text)
    if candidate in all_slugs:
        return candidate

    # Try some common variations
    variations = [
        candidate,
        candidate.replace('-and-', '-'),
        re.sub(r'-i-', '-', candidate),
        # "sales tax in X" → "sales-tax-in-X"
    ]

    for v in variations:
        if v in all_slugs:
            return v

    # Try partial prefix match (link text might be a shorter version of the title)
    matches = [s for s in all_slugs if s.startswith(candidate[:20]) and len(candidate) > 15]
    if len(matches) == 1:
        return matches[0]

    return None

# Process files
total_replaced = 0
total_unmatched = 0
unmatched_set = set()

for filepath in sorted(mdx_files):
    with open(filepath, "r") as f:
        content = f.read()

    if "(#)" not in content:
        continue

    pattern = re.compile(r'\[([^\]]+)\]\(#\)')

    def replace_link(m):
        global total_replaced, total_unmatched
        link_text = m.group(1)
        slug = find_slug(link_text)
        if slug:
            total_replaced += 1
            return f"[{link_text}](/{slug})"
        else:
            if not is_cta(link_text):
                total_unmatched += 1
                unmatched_set.add(link_text)
            return m.group(0)

    new_content = pattern.sub(replace_link, content)

    if new_content != content:
        with open(filepath, "w") as f:
            f.write(new_content)

print(f"\nReplaced: {total_replaced} additional links")
print(f"Still unmatched: {total_unmatched}")
if unmatched_set:
    print("\nStill unmatched (non-CTA):")
    for t in sorted(unmatched_set):
        print(f"  - {t}")

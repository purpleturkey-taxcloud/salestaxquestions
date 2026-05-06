#!/usr/bin/env python3
"""Replace (#) placeholder links in MDX files with actual slugs."""

import os
import re
import glob

CONTENT_DIR = "src/content/questions"

# Step 1: Build title → slug map from all MDX files
title_to_slug = {}
slug_to_title = {}

mdx_files = glob.glob(f"{CONTENT_DIR}/**/*.mdx", recursive=True)

for filepath in mdx_files:
    with open(filepath, "r") as f:
        content = f.read()

    title_match = re.search(r'^title:\s*["\'](.+?)["\']', content, re.MULTILINE)
    slug_match = re.search(r'^slug:\s*["\'](.+?)["\']', content, re.MULTILINE)

    if title_match and slug_match:
        title = title_match.group(1)
        slug = slug_match.group(1)
        title_to_slug[title] = slug
        slug_to_title[slug] = title

print(f"Loaded {len(title_to_slug)} title→slug mappings")

# Normalize for fuzzy matching: lowercase, strip punctuation
import unicodedata

def normalize(text):
    text = text.lower().strip()
    # Remove trailing punctuation like ? . !
    text = re.sub(r'[?!.,;:]+$', '', text)
    # Collapse whitespace
    text = re.sub(r'\s+', ' ', text)
    return text

normalized_map = {normalize(t): s for t, s in title_to_slug.items()}

def find_slug(link_text):
    """Try to find a slug for this link text."""
    # Exact match first
    if link_text in title_to_slug:
        return title_to_slug[link_text]

    # Normalized match
    norm = normalize(link_text)
    if norm in normalized_map:
        return normalized_map[norm]

    # Try removing trailing arrow or extra text
    clean = re.sub(r'\s*→.*$', '', link_text).strip()
    if clean in title_to_slug:
        return title_to_slug[clean]
    norm_clean = normalize(clean)
    if norm_clean in normalized_map:
        return normalized_map[norm_clean]

    return None

# Step 2: Process each file
total_replaced = 0
total_unmatched = 0
unmatched_set = set()

for filepath in sorted(mdx_files):
    with open(filepath, "r") as f:
        content = f.read()

    if "(#)" not in content:
        continue

    # Find all [text](#) patterns
    pattern = re.compile(r'\[([^\]]+)\]\(#\)')

    file_replaced = 0
    file_unmatched = []

    def replace_link(m):
        global total_replaced, total_unmatched
        link_text = m.group(1)
        slug = find_slug(link_text)
        if slug:
            total_replaced += 1
            return f"[{link_text}](/{slug})"
        else:
            total_unmatched += 1
            unmatched_set.add(link_text)
            return m.group(0)  # leave as-is

    new_content = pattern.sub(replace_link, content)

    if new_content != content:
        with open(filepath, "w") as f:
            f.write(new_content)

print(f"\nReplaced: {total_replaced} links")
print(f"Unmatched (left as #): {total_unmatched}")
if unmatched_set:
    print("\nUnmatched link texts:")
    for t in sorted(unmatched_set):
        print(f"  - {t}")

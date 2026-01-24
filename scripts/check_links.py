#!/usr/bin/env python3
"""
Check markdown links in changed files (for pre-commit hooks).

Usage: python scripts/check_links.py [file1] [file2] ...
       Or via pre-commit: automatically receives changed file paths

This script checks links in markdown files. For now, it performs basic validation.
Full link checking (including external URLs) is handled by CI/CD.
"""

import re
import sys
from pathlib import Path
from urllib.parse import urlparse

REPO_ROOT = Path(__file__).resolve().parent.parent


def check_file_links(file_path: Path) -> list[str]:
    """Check links in a markdown file and return list of errors."""
    errors = []
    
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as e:
        return [f"Error reading file: {e}"]
    
    # Find all markdown links: [text](url)
    link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    links = re.findall(link_pattern, content)
    
    for text, url in links:
        # Skip anchor links (internal page links)
        if url.startswith("#"):
            continue
        
        # Check for common issues
        if url.startswith("http://") or url.startswith("https://"):
            # External link - basic validation (full checking in CI)
            parsed = urlparse(url)
            if not parsed.netloc:
                errors.append(f"Invalid external URL: {url} in {file_path.name}")
        elif url.startswith("mailto:"):
            # Email link - skip validation
            continue
        elif url.startswith("/"):
            # Absolute path - check if file exists
            target = REPO_ROOT / url.lstrip("/")
            if not target.exists():
                errors.append(f"Broken internal link: {url} in {file_path.name}")
        else:
            # Relative path - check if file exists
            target = file_path.parent / url
            if not target.exists():
                # Try with .md extension
                if not url.endswith(".md"):
                    target_md = file_path.parent / f"{url}.md"
                    if not target_md.exists():
                        errors.append(f"Broken relative link: {url} in {file_path.name}")
    
    return errors


def main() -> None:
    if len(sys.argv) < 2:
        # No files provided - nothing to check
        print("No files to check")
        sys.exit(0)

    all_errors = []
    file_paths = [Path(arg) for arg in sys.argv[1:]]
    
    for file_path in file_paths:
        # Resolve relative paths
        if not file_path.is_absolute():
            file_path = REPO_ROOT / file_path
        
        if not file_path.exists():
            all_errors.append(f"File not found: {file_path}")
            continue
        
        errors = check_file_links(file_path)
        all_errors.extend(errors)
    
    if all_errors:
        print("Link checking failed:", file=sys.stderr)
        for error in all_errors:
            print(f"  {error}", file=sys.stderr)
        sys.exit(1)
    
    print(f"OK: checked links in {len(file_paths)} file(s)")
    sys.exit(0)


if __name__ == "__main__":
    main()

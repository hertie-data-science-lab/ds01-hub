#!/usr/bin/env python3
"""
Build script for DS01 documentation.
Converts markdown files to HTML using the Hertie DSL site template.
"""

import os
import re
import shutil
from pathlib import Path
import markdown
from markdown.extensions.toc import TocExtension
from markdown.extensions.tables import TableExtension
from markdown.extensions.fenced_code import FencedCodeExtension

# Configuration
DOCS_DIR = Path("docs")
TEMPLATE_DIR = Path("_templates")
OUTPUT_DIR = Path("site")
TEMPLATE_FILE = TEMPLATE_DIR / "doc-page.html"

# Navigation structure (order matters)
NAV_STRUCTURE = [
    ("Home", "index.html", None),
    ("Quickstart", "quickstart.html", None),
    ("Quick Reference", "quick-reference.html", None),
    ("Getting Started", "getting-started/index.html", "getting-started"),
    ("Core Guides", "core-guides/index.html", "core-guides"),
    ("Intermediate", "intermediate/index.html", "intermediate"),
    ("Advanced", "advanced/index.html", "advanced"),
    ("Key Concepts", "key-concepts/index.html", "key-concepts"),
    ("Background", "background/index.html", "background"),
    ("Reference", "reference/index.html", "reference"),
    ("Troubleshooting", "troubleshooting/index.html", "troubleshooting"),
]


def get_title_from_markdown(content: str, filepath: Path) -> str:
    """Extract title from markdown content (first H1) or filename."""
    match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if match:
        return match.group(1).strip()
    # Fallback to filename
    name = filepath.stem
    if name in ('README', 'index'):
        name = filepath.parent.name
    return name.replace('-', ' ').replace('_', ' ').title()


def get_files_in_section(section_dir: Path) -> list:
    """Get all markdown files in a section, README first."""
    if not section_dir.exists():
        return []

    files = []
    readme = section_dir / "README.md"
    if readme.exists():
        files.append(readme)

    for f in sorted(section_dir.glob("*.md")):
        if f.name != "README.md":
            files.append(f)

    return files


def md_to_html_path(md_path: Path) -> str:
    """Convert markdown path to HTML path."""
    rel = md_path.relative_to(DOCS_DIR)
    if rel.name == "README.md":
        return str(rel.parent / "index.html")
    return str(rel.with_suffix(".html"))


def build_sidebar(current_page: str) -> str:
    """Build the sidebar navigation HTML."""
    html = ["<ul>"]

    for title, url, section_dir in NAV_STRUCTURE:
        is_active = current_page == url

        if section_dir:
            # Section with children
            section_path = DOCS_DIR / section_dir
            children = get_files_in_section(section_path)

            html.append(f'<li><span class="section-title"><a href="{url}">{title}</a></span>')

            if children:
                html.append("<ul>")
                for child in children:
                    child_url = md_to_html_path(child)
                    child_content = child.read_text(encoding='utf-8')
                    child_title = get_title_from_markdown(child_content, child)

                    # Skip if same as section title
                    if child.name == "README.md":
                        continue

                    active_class = ' class="active"' if current_page == child_url else ''
                    html.append(f'<li><a href="{child_url}"{active_class}>{child_title}</a></li>')
                html.append("</ul>")

            html.append("</li>")
        else:
            # Top-level page
            active_class = ' class="active"' if is_active else ''
            html.append(f'<li><span class="section-title"><a href="{url}"{active_class}>{title}</a></span></li>')

    html.append("</ul>")
    return "\n".join(html)


def build_breadcrumb(filepath: Path) -> str:
    """Build breadcrumb HTML for a page."""
    rel = filepath.relative_to(DOCS_DIR)
    parts = list(rel.parts)

    if len(parts) == 1:
        # Top-level file
        return ""

    # Section page
    section = parts[0]
    section_title = section.replace('-', ' ').replace('_', ' ').title()

    if parts[-1] == "README.md":
        return f"<li>{section_title}</li>"

    page_content = filepath.read_text(encoding='utf-8')
    page_title = get_title_from_markdown(page_content, filepath)

    return f'<li><a href="index.html">{section_title}</a></li><li>{page_title}</li>'


def convert_internal_links(content: str) -> str:
    """Convert .md links to .html links."""
    # Convert [text](path.md) to [text](path.html)
    content = re.sub(r'\]\(([^)]+)\.md\)', r'](\1.html)', content)
    # Convert README.html to index.html
    content = re.sub(r'\]\(([^)]*)/README\.html\)', r'](\1/index.html)', content)
    content = re.sub(r'\]\(README\.html\)', r'](index.html)', content)
    return content


def build_page(md_path: Path, template: str) -> str:
    """Convert a markdown file to HTML using the template."""
    content = md_path.read_text(encoding='utf-8')
    title = get_title_from_markdown(content, md_path)

    # Convert internal links
    content = convert_internal_links(content)

    # Convert markdown to HTML
    md = markdown.Markdown(extensions=[
        'tables',
        'fenced_code',
        'codehilite',
        TocExtension(permalink=True),
        'nl2br',
    ])
    html_content = md.convert(content)

    # Build page-specific elements
    html_path = md_to_html_path(md_path)
    sidebar = build_sidebar(html_path)
    breadcrumb = build_breadcrumb(md_path)

    # Fill template
    page = template.replace("{{title}}", title)
    page = page.replace("{{sidebar}}", sidebar)
    page = page.replace("{{breadcrumb}}", breadcrumb)
    page = page.replace("{{content}}", html_content)

    return page


def main():
    """Build all documentation pages."""
    print("Building DS01 documentation...")

    # Clean output directory
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True)

    # Load template
    template = TEMPLATE_FILE.read_text(encoding='utf-8')

    # Find all markdown files
    md_files = list(DOCS_DIR.rglob("*.md"))
    print(f"Found {len(md_files)} markdown files")

    # Process each file
    for md_path in md_files:
        html_path_str = md_to_html_path(md_path)
        output_path = OUTPUT_DIR / html_path_str

        # Create parent directories
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Build and write page
        html = build_page(md_path, template)
        output_path.write_text(html, encoding='utf-8')
        print(f"  {md_path} -> {output_path}")

    print(f"\nBuild complete! Output in {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()

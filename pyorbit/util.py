from typing import Any, Dict, List
from pathlib import Path
import os
import shutil

import mistune
import sass
import jinja2
from jinja2 import Environment, FileSystemLoader


def parse_frontmatter(contents: str):
    _, frontmatter, markdown = contents.split("---", maxsplit=2)
    frontmatter = frontmatter.strip().split("\n")
    frontmatter = {
        line.split(":")[0].strip(): line.split(":")[1].strip()
        for line in frontmatter
        if line.strip() != ""
    }
    return frontmatter, markdown


def read_pages(pages_dir: Path) -> List[Dict[str, Dict]]:
    pages = []
    for file in pages_dir.glob("**/*.md"):
        with open(file, "r", encoding="utf-8") as f:
            frontmatter, content = parse_frontmatter(f.read())
            slug = file.relative_to(pages_dir).with_suffix("").as_posix()
            pages.append({**frontmatter, "slug": slug, "content": content})

    return pages


def read_templates(layouts_dir: Path) -> Dict[str, jinja2.Template]:
    env = Environment(loader=FileSystemLoader(layouts_dir))
    layouts = {}

    for file in layouts_dir.glob("*.html"):
        try:
            layouts[file.stem] = env.get_template(file.name)
        except Exception:
            print(f"Error parsing {file}")

    return layouts


def build_page(
        page: Dict[str, Any],
        templates: Dict[str, jinja2.Template],
        partials: Dict[str, jinja2.Template],
        output_dir: Path,
        pages: List[Dict],
        posts: List[Dict],
        is_post: bool = False
    ):
    if is_post or page["slug"] == "index" or page["slug"] == "404":
        output_path = output_dir / f"{page['slug']}.html"
    else:
        output_path = output_dir / f"{page['slug']}" / "index.html"
    os.makedirs(output_path.parent, exist_ok=True)
    try:
        template = templates[page["layout"]]
        rendered_partials = {k: v.render(**page) for k, v in partials.items()}
        page["content"] = mistune.html(page["content"])
        with open(output_path, "w", encoding="utf-8") as out_f:
            out_f.write(template.render(**page, **rendered_partials, pages=pages, posts=posts))
    except Exception as e:
        print(f"Error parsing {page['slug'], page['layout']}")
        print(e)


def build_site(
    theme_root: Path,
    pages_dir: Path,
    posts_dir: Path,
    partials_dir: Path,
    layout_dir: Path,
    output_dir: Path,
):
    if output_dir.exists(): shutil.rmtree(output_dir); output_dir.mkdir()

    partials = read_templates(partials_dir)
    templates = read_templates(layout_dir)
    pages = read_pages(pages_dir)
    posts = read_pages(posts_dir)

    css_path = output_dir / "assets/css"; css_path.mkdir(parents=True)
    sass.compile(
        dirname=(theme_root / "assets/css", "_site/assets/css"),
        output_style="compressed",
    )

    for page in pages: build_page(page, templates, partials, output_dir, pages, posts)
    for post in posts: build_page(post, templates, partials, output_dir, pages, posts, is_post=True)

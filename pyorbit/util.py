from typing import Dict
from pathlib import Path
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


def read_layouts(layouts_dir: Path) -> Dict[str, jinja2.Template]:
    env = Environment(loader=FileSystemLoader(layouts_dir))
    layouts = {}

    for file in layouts_dir.glob("*.html"):
        try:
            layouts[file.stem] = env.get_template(file.name)
        except Exception:
            print(f"Error parsing {file}")

    return layouts


def build_site(
    theme_root: Path,
    pages_dir: Path,
    posts_dir: Path,
    partials_dir: Path,
    layout_dir: Path,
    output_dir: Path,
):
    if output_dir.exists(): shutil.rmtree(output_dir); output_dir.mkdir()

    partials = read_layouts(partials_dir)
    templates = read_layouts(layout_dir)

    # compile scss -> css
    css_path = output_dir / "assets/css"; css_path.mkdir(parents=True)
    # TODO: move around syntax.scss so it doesnt get outputted to _site
    sass.compile(
        dirname=(theme_root / "assets/css" , "_site/assets/css"), output_style="compressed"
    )

    # build pages
    for file in pages_dir.glob("*.md"):
        if file.name == "index.md":
            with open(file, "r", encoding="utf=8") as in_f:
                frontmatter, content = parse_frontmatter(in_f.read())
                page_name = file.name.replace(".md", "")
                rendered_partials = {
                    k: v.render(**frontmatter) for k, v in partials.items()
                }
                with open(f"_site/index.html", "w", encoding="utf-8") as out_f:
                    template = templates[frontmatter["layout"]]
                    content = mistune.html(content)
                    out_f.write(
                        template.render(
                            content=content, **rendered_partials, **frontmatter
                        )
                    )
        try:
            with open(file, "r", encoding="utf=8") as in_f:
                frontmatter, content = parse_frontmatter(in_f.read())
                page_name = file.name.replace(".md", "")
                rendered_partials = {
                    k: v.render(**frontmatter) for k, v in partials.items()
                }
                (output_dir / page_name / "index.html").parent.mkdir(parents=True)
                with open(f"_site/{page_name}/index.html", "w", encoding="utf-8") as out_f:
                    template = templates[frontmatter["layout"]]
                    content = mistune.html(content)
                    out_f.write(
                        template.render(
                            content=content, **rendered_partials, **frontmatter
                        )
                    )
        except ValueError:
            print(f"Error parsing {file}")


    # build posts
    for file in posts_dir.glob("**/*.md"):
        try:
            with open(file, "r", encoding="utf=8") as in_f:
                frontmatter, content = parse_frontmatter(in_f.read())
                html_name = file.name.replace(".md", ".html")
                rendered_partials = {
                    k: v.render(**frontmatter) for k, v in partials.items()
                }
                with open(f"_site/{html_name}", "w", encoding="utf-8") as out_f:
                    template = templates[frontmatter["layout"]]
                    content = mistune.html(content)
                    out_f.write(
                        template.render(
                            content=content, **rendered_partials, **frontmatter
                        )
                    )
        except ValueError:
            print(f"Error parsing {file}")

from pyorbit.util import *
from pathlib import Path
import time

# TODO make sample theme and use it here

theme_root_path = Path("themes/blank")
pages_path = Path("themes/blank/pages")
posts_path = Path("themes/blank/posts")
partials_path = Path("themes/blank/layouts/partials")
layouts_path = Path("themes/blank/layouts")
output_path = Path("_site")

start = time.perf_counter()
build_site(theme_root_path, pages_path, posts_path, partials_path, layouts_path, output_path)
print(f"Built site in {time.perf_counter() - start:.2f} seconds")

pgs = read_pages(posts_path)
print([pg['slug'] for pg in pgs])
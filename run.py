from pyorbit.util import *
from pathlib import Path
import time

# TODO make sample theme and use it here

pages_path = Path("site/pages")
posts_path = Path("site/posts")
partials_path = Path("site/layouts/partials")
layouts_path = Path("site/layouts")
output_path = Path("_site")

start = time.perf_counter()
build_site(pages_path, posts_path, partials_path, layouts_path, output_path)
print(f"Built site in {time.perf_counter() - start:.2f} seconds")

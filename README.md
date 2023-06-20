# PyOrbit

Yet another static site generator written in Python.

## Why pyorbit > other SSGs ???

building this site (4 posts and some layouts) from scratch [takes ~200 ms](https://twitter.com/tommy_b_nguyen/status/1669071006319648769).
in my experience with jekyll on my personal blog (30 posts) it takes 6000-7000 ms to build the site from scratch.

aside from being a bit faster at building the site, pyorbit is < 100 LOC of python with 3 dependencies.
a tiny project with enough room to explore new features as a learning project (whether you're new to python, or want to try out a relevant library).
and although pyorbit is small, it has enough features that with a bit of effort i would be able to recreate my [personal site](https://tommynguyen.dev/) with it.
so it has just enough functionality to be used in the wild.
see below for features that would take me from actually replacing using jekyll in my personal blog.

## Preqreqs
- have python3 (tested with Python 3.10, not sure about others)

## Usage
super rough, subject to change rapidly

1. `python -m venv venv`
2. `./venv/Scripts/activate`
3. `pip install -r requirements-dev.txt`
4. `python run`
5. (optional if you want to see site in browser) `python -m http.server --directory _site`


## TODO
- add nice CLI tool
- support code highlighting?
- incrementally build pages (don't do full rebuilds every time we build site)
- add file watching/serving so you can live edit files and re-build (for live editing + feedback)
- docs
- add GH actions or smthin so we can autodeploy sites built w this on GH pages
- also add instructions for hosting on other platforms
  - AWS S3 buckets
  - Netlify   

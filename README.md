# PyOrbit

Yet another static site generator written in Python.


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

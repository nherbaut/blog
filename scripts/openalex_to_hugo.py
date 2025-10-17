#!/usr/bin/env python3
import sys, re, subprocess, json, urllib.parse, os, datetime

try:
    import requests
    import yaml
except ImportError:
    sys.stderr.write("pip install requests PyYAML\n")
    sys.exit(1)

SITE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT_DIR = os.path.join(SITE_ROOT, "content", "articles")

def slugify(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"[^\w\s-]", "", s, flags=re.UNICODE)   # drop non-word chars
    s = re.sub(r"[\s_]+", "-", s)                      # spaces/underscores -> hyphen
    s = re.sub(r"-{2,}", "-", s).strip("-")            # collapse hyphens
    return s or "untitled"

def extract_doi(input_str: str) -> str:
    s = input_str.strip()
    if s.startswith("https://doi.org/") or s.startswith("http://doi.org/"):
        return s.split("doi.org/", 1)[1]
    if s.lower().startswith("doi:"):
        return s.split(":", 1)[1].strip()
    return s  # assume raw DOI

def fetch_openalex_by_doi(doi: str) -> dict:
    # OpenAlex: /works/doi:{doi}
    q = f"doi:{doi}"
    url = f"https://api.openalex.org/works/{urllib.parse.quote(q, safe=':')}"
    r = requests.get(url, timeout=20)
    if r.status_code == 404:
        sys.stderr.write("OpenAlex: work not found for DOI\n")
        sys.exit(2)
    r.raise_for_status()
    return r.json()

def pick_venue(meta: dict) -> str:
    hv = (meta.get("host_venue") or {})
    if hv.get("display_name"):
        return hv["display_name"]
    pl = (meta.get("primary_location") or {}).get("source") or {}
    return pl.get("display_name") or "?"

def pick_authors(meta: dict) -> list:
    auths = meta.get("authorships") or []
    # Preserve order as given
    names = []
    for a in auths:
        person = (a.get("author") or {})
        name = person.get("display_name")
        if name:
            names.append(name)
    return names

def pick_topics(meta: dict, limit=5) -> list:
    # Use concepts as proxies for topics, by descending score
    concepts = meta.get("concepts") or []
    concepts = sorted(concepts, key=lambda c: c.get("score") or 0, reverse=True)
    return [c.get("display_name") for c in concepts[:limit] if c.get("display_name")]

def ensure_dirs():
    os.makedirs(CONTENT_DIR, exist_ok=True)

def hugo_new(relpath: str):
    # Use archetype kind "articles"
    cmd = ["hugo", "new", "--kind", "articles", relpath]
    subprocess.run(cmd, check=True, cwd=SITE_ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def read_front_matter(path: str) -> tuple[dict, str]:
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    if not text:
        return {}, ""

    # Detect delimiter (YAML or TOML)
    first_line_end = text.find("\n")
    first_line = text[:first_line_end] if first_line_end != -1 else text
    if first_line.startswith("---"):
        delim = "---"
    elif first_line.startswith("+++"):
        delim = "+++"
    else:
        # No front matter
        return {}, text

    # Find closing delimiter at BOL
    # Work line-wise to avoid accidental matches in content
    lines = text.splitlines(keepends=True)
    if not lines or not lines[0].startswith(delim):
        return {}, text

    close_idx = None
    for i in range(1, len(lines)):
        if lines[i].startswith(delim):
            close_idx = i
            break

    if close_idx is None:
        # Malformed front matter without closing delimiter
        return {}, text

    fm_text = "".join(lines[1:close_idx])
    body = "".join(lines[close_idx + 1:])

    import yaml
    data = yaml.safe_load(fm_text) or {}
    return data, body


def write_front_matter(path: str, data: dict, body: str):
    with open(path, "w", encoding="utf-8") as f:
        f.write("---\n")
        yaml.safe_dump(
            data, f,
            sort_keys=False, allow_unicode=True, default_flow_style=False
        )
        f.write("---")
        if body and (body.startswith("\n") or body.startswith("\r\n")):
            f.write(body)
        else:
            f.write("\n" + (body or ""))

def main():
    if len(sys.argv) != 3:
        sys.stderr.write('Usage: openalex_to_hugo.py "Custom Title" https://doi.org/10.xxxx\n')
        sys.exit(2)

    page_title = sys.argv[1]
    doi_input = sys.argv[2]
    doi = extract_doi(doi_input)

    ensure_dirs()

    slug = slugify(page_title)
    rel_md_path = os.path.join("articles", f"{slug}.md")
    abs_md_path = os.path.join(SITE_ROOT, "content", rel_md_path)

    if os.path.exists(abs_md_path):
        sys.stderr.write(f"File exists: {abs_md_path}\n")
        sys.exit(3)

    # Create skeleton via archetype
    hugo_new(rel_md_path)

    # Fetch OpenAlex metadata
    meta = fetch_openalex_by_doi(doi)

    # Map fields
    article_title = meta.get("title") or page_title
    publication_year = meta.get("publication_year") or None
    venue = pick_venue(meta)
    authors = pick_authors(meta)
    topics = pick_topics(meta)
    oa = ((meta.get("open_access") or {}).get("oa_url")) or ((meta.get("primary_location") or {}).get("landing_page_url")) or ""
    doi_norm = meta.get("doi") or doi  # OpenAlex returns canonical DOI or None

    # Load, patch, write
    fm, body = read_front_matter(abs_md_path)

    # Ensure required Hugo page fields
    fm["title"] = page_title
    fm["type"] = "articles"
    fm.setdefault("draft", False)
    if "date" not in fm:
        fm["date"] = datetime.datetime.now().isoformat()

    # Required article params
    fm["article_doi"] = doi_norm
    fm["article_oaurl"] = oa or ""
    fm["article_topics"] = topics or []
    fm["article_article_authors"] = authors or []
    fm["article_title"] = article_title
    fm["article_venue"] = venue or ""
    if publication_year:
        fm["article_publication_year"] = int(publication_year)

    write_front_matter(abs_md_path, fm, body)

    print(abs_md_path)

if __name__ == "__main__":
    main()


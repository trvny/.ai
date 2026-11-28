"""Check public output paths and metadata after Astro build."""
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

DIST = Path(__file__).resolve().parents[1] / "dist"
BASE = "https://ai.bartek.lol/"


class Metadata(HTMLParser):
    def __init__(self):
        super().__init__()
        self.canonical = None
        self.favicon = None
        self.description = None
        self.schemas = []
        self.schema_text = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "link":
            if attrs.get("rel") == "canonical":
                self.canonical = attrs.get("href")
            if "icon" in attrs.get("rel", "").split():
                self.favicon = attrs.get("href")
        elif tag == "meta" and attrs.get("name") == "description":
            self.description = attrs.get("content")
        elif tag == "script" and attrs.get("type") == "application/ld+json":
            self.schema_text = ""

    def handle_data(self, data):
        if self.schema_text is not None:
            self.schema_text += data

    def handle_endtag(self, tag):
        if tag == "script" and self.schema_text is not None:
            self.schemas.append(json.loads(self.schema_text))
            self.schema_text = None


def main():
    sitemap = (DIST / "sitemap.xml").read_text(encoding="utf-8")
    urls = re.findall(r"<loc>([^<>&]+)</loc>", sitemap)
    expected = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    expected += "".join(f"  <url><loc>{url}</loc></url>\n" for url in urls) + "</urlset>\n"
    assert sitemap == expected, "Unexpected sitemap structure"
    assert urls and len(urls) == len(set(urls))
    index = (DIST / "llms.txt").read_text(encoding="utf-8")
    full = (DIST / "llms-full.txt").read_text(encoding="utf-8")
    robots = (DIST / "robots.txt").read_text(encoding="utf-8")
    assert f"Sitemap: {BASE}sitemap.xml" in robots
    assert (DIST / "favicon.svg").is_file()
    for url in urls:
        assert url.startswith(BASE), url
        slug = url.removeprefix(BASE).strip("/")
        path = DIST / slug / "index.html"
        metadata = Metadata()
        metadata.feed(path.read_text(encoding="utf-8"))
        assert metadata.canonical and metadata.canonical.rstrip("/") == url.rstrip("/"), (url, metadata.canonical)
        assert metadata.description, url
        assert metadata.favicon and urlsplit(metadata.favicon).path == "/favicon.svg", (url, metadata.favicon)
        types = {schema.get("@type") for schema in metadata.schemas}
        assert ("TechArticle" if slug else "WebSite") in types, (url, types)
        assert not slug or "BreadcrumbList" in types, url
        assert url in index and f"Source page: {url}\n" in full, url
    print(f"Verified {len(urls)} pages, metadata, sitemap, LLM exports and robots")


if __name__ == "__main__":
    main()

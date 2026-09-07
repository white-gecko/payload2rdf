from bs4 import BeautifulSoup
from extruct import extract
from w3lib.html import get_base_url


def extract_metadata(url, html):
    base_url = get_base_url(html, url)

    # Extruct: strukturierte Metadaten
    metadata = (
        extract(
            html,
            base_url=base_url,
        )
        or {}
    )

    metadata["html"] = [dict(extract_html_metadata(html))]

    return metadata


def extract_html_metadata(html):
    """Extract basic metadata from HTML documents encoded in the lang attribute, title tag and common meta-tags."""
    soup = BeautifulSoup(html, "html.parser")
    lang = soup.get("lang")
    title = soup.title.string if soup.title and soup.title.string else None
    keywords = list(get_meta_tag(soup, "keywords"))
    description = list(get_meta_tag(soup, "description"))
    author = list(get_meta_tag(soup, "author"))

    if lang:
        yield "lang", lang
    if title:
        yield "title", title
    if keywords:
        yield "keywords", keywords
    if description:
        yield "description", description
    if author:
        yield "author", author


def get_meta_tag(soup, name: str):
    """Get a meta-tags content attributes value."""
    for element in soup.find_all("meta", attrs={"name": "name"}):
        yield element["content"]

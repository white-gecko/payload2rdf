import extruct
from w3lib.html import get_base_url
from bs4 import BeautifulSoup


def extract_metadata(url, html):
    base_url = get_base_url(html, url)

    # Extruct: strukturierte Metadaten
    metadata = extruct.extract(
        html,
        base_url=base_url,
        syntaxes=["json-ld", "microdata", "opengraph", "rdfa", "microformat"],
    )

    # Fallback: einfache <title> + <meta name="description">
    fallback = extract_fallback_metadata(html)
    metadata["fallback"] = [
        fallback
    ]  # in eine Liste verpacken, um Mapping-Logik zu matchen

    return metadata


def extract_fallback_metadata(html):
    soup = BeautifulSoup(html, "html.parser")
    title = soup.title.string.strip() if soup.title and soup.title.string else None
    description = soup.find("meta", attrs={"name": "description"})
    return {
        "title": title,
        "description": description["content"].strip()
        if description and description.has_attr("content")
        else None,
    }

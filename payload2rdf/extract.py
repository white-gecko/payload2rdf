from bs4 import BeautifulSoup
from extruct import extract
from w3lib.html import get_base_url


def extract_metadata(url, html):
    """
    Extract metadata from HTML content.

    This function uses the extruct library to extract structured metadata from HTML content.
    It also extracts basic HTML metadata such as language, title, keywords, description, and author.

    Args:
        url (str): The URL of the HTML content.
        html (str): The HTML content to extract metadata from.

    Returns:
        dict: A dictionary containing the extracted metadata.
    """
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
    """
    Get the content attribute value of a meta tag.

    This function searches for meta tags with a specific name attribute and yields their content values.

    Args:
        soup (BeautifulSoup): The BeautifulSoup object representing the HTML content.
        name (str): The name attribute value to search for in meta tags.

    Yields:
        str: The content attribute value of the meta tag.
    """
    for element in soup.find_all("meta", attrs={"name": "name"}):
        yield element["content"]

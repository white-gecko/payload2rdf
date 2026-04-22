# payload2rdf/warc_reader.py

from warcio.archiveiterator import ArchiveIterator


def extract_html_records(warc_path):
    with open(warc_path, "rb") as stream:
        for record in ArchiveIterator(stream):
            if record.rec_type == "response" and record.http_headers:
                content_type = record.http_headers.get_header("Content-Type")
                if content_type and "html" in content_type:
                    payload = (
                        record.content_stream().read().decode("utf-8", errors="ignore")
                    )
                    url = record.rec_headers.get_header("WARC-Target-URI")
                    if not payload.strip():
                        continue  # Leeres Dokument überspringen
                    print(f"\n Inhalt von {url[:80]}...\n{payload[:300]}\n{'-' * 50}")
                    yield url, payload

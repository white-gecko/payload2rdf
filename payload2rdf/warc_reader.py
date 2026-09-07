from loguru import logger
from warcio.archiveiterator import ArchiveIterator


def extract_html_records(warc_path, record_id):
    """
    Extract HTML records from a WARC file.

    This function reads through a WARC file and extracts all records that contain
    HTML content. It yields each HTML record found in the archive for further processing.

    Args:
        warc_path (str): The file path to the WARC file to be processed

    Yields:
        warcio.recordreader.ArcRecord: HTML records from the WARC file
    """
    with open(warc_path, "rb") as stream:
        for record in ArchiveIterator(stream):
            if record_id and not record.rec_headers["WARC-Record-ID"] == record_id:
                continue
            if record.rec_type not in ["response", "resource"]:
                continue
            if "application/http" in record.content_type and record.http_headers:
                content_type = record.http_headers.get_header("Content-Type")
                if content_type and "html" in content_type:
                    payload = (
                        record.content_stream().read().decode("utf-8", errors="ignore")
                    )
                    url = record.rec_headers.get_header("WARC-Target-URI")
                    if not payload.strip():
                        # skip empty documents
                        continue
                    logger.debug(
                        f"Content of {url[:80]}...\n{payload[:300]}\n{'-' * 50}"
                    )
                    yield url, payload

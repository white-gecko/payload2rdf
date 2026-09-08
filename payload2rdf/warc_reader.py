from collections.abc import Iterator
from typing import BinaryIO

from loguru import logger
from warcio.archiveiterator import ArchiveIterator


def extract_html_records(
    warc_file_stream: BinaryIO, record_id: str
) -> Iterator[tuple[str, str]]:
    """
    Extract HTML records from a WARC file.

    This function reads through a WARC file and extracts all records that contain
    HTML content. It yields each target URI and payload found in the archive for further processing.

    Args:
        warc_file_stream (binary stream): The opened WARC file or a binary stream to be processed
        record_id (str): optionally a record_id, to identify an exact record. It needs to be specified
                         in the same way as in the WARC file, i.e. including the angular brackets,
                         e.g. `<urn:uuid:31ee6876-e5a5-4d4d-86e5-3839a49290f5>`

    Yields:
        uri, payload (tuple[str, str]): the WARC-Target-URI and the HTML payload of the record
    """
    final = False
    for record in ArchiveIterator(warc_file_stream):
        if final:
            break
        if record_id:
            if record.rec_headers["WARC-Record-ID"] != record_id:
                continue
            else:
                final = True
        if record.rec_type not in ["response", "resource"]:
            continue
        if "application/http" in record.content_type and record.http_headers:
            content_type = record.http_headers.get_header("Content-Type")
            if content_type and "html" in content_type:
                payload = (
                    record.content_stream().read().decode("utf-8", errors="ignore")
                )
                uri = record.rec_headers.get_header("WARC-Target-URI")
                if not payload.strip():
                    # skip empty documents
                    continue
                logger.debug(f"Content of {uri[:80]}...\n{payload[:300]}\n{'-' * 50}")
                yield uri, payload

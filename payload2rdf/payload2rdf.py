from rdflib import Graph

from .extract import extract_metadata
from .mapping import map_metadata_to_graph
from .warc_reader import read_html_payload


def payload2rdf(warc_file_stream, select_record_id=None, mapping=None):
    """
    Convert WARC file payloads to RDF graphs.

    This function reads HTML payloads from a WARC file, extracts metadata, and maps it to RDF graphs.

    Args:
        warc_file_stream (BinaryIO): The opened WARC file or a binary stream to be processed.
        mapping (dict): The mapping rules to apply.
        select_record_id (str, optional): The WARC-Record-ID to select a specific record. Defaults to None.

    Yields:
        record_id, target_uri, record_graph (tuple[str, str, Graph]): The WARC-Record-ID, WARC-Target-URI, and the RDF graph of the record.
    """
    for record_id, target_uri, html_payload in read_html_payload(
        warc_file_stream, select_record_id
    ):
        metadata = extract_metadata(target_uri, html_payload)
        record_graph = Graph()
        map_metadata_to_graph(record_graph, target_uri, metadata, mapping)

        yield record_id, target_uri, record_graph

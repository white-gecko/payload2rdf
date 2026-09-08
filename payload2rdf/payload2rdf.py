from rdflib import Graph

from .extract import extract_metadata
from .mapping import map_metadata_to_graph
from .warc_reader import read_html_payload


def payload2rdf(warc_file_stream, mapping, select_record_id):
    for record_id, target_uri, html_payload in read_html_payload(
        warc_file_stream, select_record_id
    ):
        metadata = extract_metadata(target_uri, html_payload)
        record_graph = Graph()
        map_metadata_to_graph(record_graph, target_uri, metadata, mapping)

        yield record_id, target_uri, record_graph

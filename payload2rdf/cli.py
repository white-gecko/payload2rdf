import click
from loguru import logger
from rdflib import Graph

from payload2rdf.extract import extract_metadata
from payload2rdf.mapping import load_mapping, map_metadata_to_graph
from payload2rdf.warc_reader import extract_html_records


@click.command()
@click.argument("warc_file", type=click.Path(exists=True))
@click.option(
    "--mapping-file",
    type=click.Path(exists=True),
    default="mappings.yaml",
    help="YAML-Datei mit den Mapping-Regeln",
)
@click.option(
    "--format",
    "-f",
    "rdf_format",
    default="turtle",
    show_default=True,
    type=click.Choice(["xml", "turtle", "nt", "n3"], case_sensitive=False),
    help="Optional RDF serialization format.",
)
def cli(warc_file, mapping_file, rdf_format):
    """Extract metdata as RDF from a WARC file for each record using specified mapping rules.

    This command processes a WARC file, extracts metadata from the payload of each record, and maps the metadata to RDF using the provided mapping configuration.
    The resulting RDF graph is serialized in the specified format.
    """
    mapping = load_mapping(mapping_file)
    graph = Graph()
    for url, html in extract_html_records(warc_file):
        metadata = extract_metadata(url, html)
        record_graph = Graph()
        map_metadata_to_graph(record_graph, url, metadata, mapping)
        logger.debug(f"# RDF for {url}")
        logger.debug(record_graph.serialize(format=rdf_format))
        graph += record_graph

    print(graph.serialize(format=rdf_format))


if __name__ == "__main__":
    cli()

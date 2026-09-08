import click
from loguru import logger
from rdflib import Graph

from .mapping import load_mapping
from .payload2rdf import payload2rdf


@click.command()
@click.argument("warc_file", type=click.Path(exists=True))
@click.option(
    "--mapping-file",
    type=click.Path(exists=True),
    default=None,
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
@click.option(
    "--record",
    "-r",
    default=None,
    help="Optional Provide the WARC-Record-ID (as it is written in the WARC file) of a record and only extract its metadata",
)
def cli(warc_file, mapping_file, rdf_format, record=None):
    """Extract metdata as RDF from a WARC file for each record using specified mapping rules.

    This command processes a WARC file, extracts metadata from the payload of each record, and maps the metadata to RDF using the provided mapping configuration.
    The resulting RDF graph is serialized in the specified format.
    """
    graph = Graph()
    with open(warc_file, "rb") as warc_file_stream:
        for record_id, uri, record_graph in payload2rdf(
            warc_file_stream, record, load_mapping(mapping_file)
        ):
            logger.debug(f"# RDF for {uri} from {record_id}")
            logger.debug(record_graph.serialize(format=rdf_format))
            graph += record_graph

    print(graph.serialize(format=rdf_format))


if __name__ == "__main__":
    cli()

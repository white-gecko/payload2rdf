from importlib import resources
from typing import Any

import yaml
from rdflib import Graph, Literal, URIRef
from rdflib.namespace import DC, DCTERMS, FOAF, DefinedNamespace, Namespace

MappingType = dict[str, dict[str, str]]

NAMESPACES = {
    "dc": DC,
    "dcterms": DCTERMS,
    "foaf": FOAF,
    "schema": Namespace("http://schema.org/"),
}


def load_mapping(yaml_path: str | None = None) -> MappingType:
    """
    Load mapping rules from a YAML file.

    This function loads mapping rules from a YAML file. If no path is provided, it defaults to the mappings.yaml file in the payload2rdf package.

    Args:
        yaml_path (str, optional): The path to the YAML file containing the mapping rules. Defaults to None.

    Returns:
        dict: A dictionary containing the mapping rules.
    """
    if not yaml_path:
        yaml_path = resources.files("payload2rdf").joinpath("mappings.yaml")
    with open(yaml_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def get_nested_value(data: dict[str, Any], key_path: str) -> Any:
    """
    Get a nested value from a dictionary using a key path.

    This function retrieves a value from a nested dictionary using a dot-separated key path.

    Args:
        data (dict): The dictionary to retrieve the value from.
        key_path (str): The dot-separated key path to the value.

    Returns:
        Any: The value at the specified key path, or None if the key path does not exist.
    """
    keys = key_path.split(".")
    for key in keys:
        if isinstance(data, dict) and key in data:
            data = data[key]
        else:
            return None
    return data


def map_metadata_to_graph(
    graph: Graph,
    uri: str,
    metadata_dict: dict[str, Any],
    mapping: MappingType | None = None,
    namespace_map: dict[str, Namespace | DefinedNamespace] = NAMESPACES,
) -> None:
    """
    Map metadata to an RDF graph using specified mapping rules.

    This function maps metadata from a dictionary to an RDF graph using the provided mapping rules.
    It iterates over the metadata and applies the mapping rules to create RDF triples.

    Args:
        graph (Graph): The RDF graph to add the triples to.
        uri (str): The URI of the resource.
        metadata_dict (dict): The dictionary containing the metadata to map.
        mapping (dict): The mapping rules to apply.
        namespace_map (dict, optional): A dictionary mapping namespace prefixes to namespace URIs. Defaults to NAMESPACES.

    Returns:
        None
    """
    page_uri = URIRef(uri)

    if not mapping:
        mapping = load_mapping()

    for syntax, rules in mapping.items():
        if syntax not in metadata_dict:
            continue

        for item in metadata_dict[syntax]:
            for source_key, target_uri in rules.items():
                value = get_nested_value(item, source_key)
                if value:
                    prefix = target_uri.split(":")[0]
                    predicate = namespace_map.get(prefix, URIRef(target_uri))[
                        target_uri.split(":")[1]
                    ]
                    graph.add((page_uri, predicate, Literal(value)))

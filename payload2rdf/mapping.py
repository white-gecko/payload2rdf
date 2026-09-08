import yaml
from rdflib import Literal, URIRef
from rdflib.namespace import DC, DCTERMS, FOAF, Namespace

NAMESPACES = {
    "dc": DC,
    "dcterms": DCTERMS,
    "foaf": FOAF,
    "schema": Namespace("http://schema.org/"),
}


def load_mapping(yaml_path):
    with open(yaml_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def get_nested_value(data, key_path):
    keys = key_path.split(".")
    for key in keys:
        if isinstance(data, dict) and key in data:
            data = data[key]
        else:
            return None
    return data


def map_metadata_to_graph(
    graph, uri, metadata_dict, mapping, namespace_map: dict = NAMESPACES
):
    page_uri = URIRef(uri)

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

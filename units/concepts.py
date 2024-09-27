from collections import defaultdict
from functools import partial
from itertools import groupby
from typing import Optional

import httpx
import structlog
from pydantic import BaseModel

from units.settings import get_settings

settings = get_settings()
logger = structlog.get_logger()


def remove_graph_namespaces(s: str) -> str:
    prefixes = (
        "http://qudt.org/schema/qudt/",
        "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "http://www.w3.org/2004/02/skos/core#",
    )

    for prefix in prefixes:
        if s.startswith(prefix):
            return s.replace(prefix, "")
    return s


def language_filter(o: dict, lang: str | None) -> bool:
    """Check if given element has the correct language, if one is given"""
    if not lang:
        return True
    if "xml:lang" in o and o["xml:lang"].lower().replace("_", "-")[: len(lang)] != lang:
        return False
    return True


def reformat_predicate_object(
    obj: dict, remove_namespaces: bool = True, strip_lang_codes: bool = False
) -> tuple:
    """Reformat the predicate and object to make them simpler and more standardized."""
    if remove_namespaces:
        formatted = (
            remove_graph_namespaces(obj["p"]["value"]),
            remove_graph_namespaces(obj["o"]["value"]),
        )
    else:
        formatted = (obj["p"]["value"], obj["o"]["value"])
    if "xml:lang" in obj["o"] and not strip_lang_codes:
        return formatted + (obj["o"]["xml:lang"].lower(),)
    return formatted


def get_qk_for_iri(iri: str) -> str | None:
    """Get the QUDT quantity key for a given unit IRI."""
    logger.debug("Using sparql endpoint url %s", settings.SPARQL_URL)

    QUERY = f"""
PREFIX qudt: <http://qudt.org/schema/qudt/>

JSON {{
    "this is ignored anyway": ?qk
}}
FROM <{settings.VOCAB_PREFIX}qudt/>
FROM <{settings.VOCAB_PREFIX}simapro/>
WHERE {{
    <{iri}> qudt:hasQuantityKind ?qk .
}}
    """

    logger.debug("Executing query %s", QUERY)
    response = httpx.post(settings.SPARQL_URL, data={"query": QUERY})
    response.raise_for_status()
    response = response.json()
    logger.info(f"Retrieved {len(response)} quantity kind results for iri {iri}")

    if not response:
        raise KeyError
    return response[0]["qk"]


def get_quantity_kinds(
    lang: str | None = None,
    remove_namespaces: bool = True,
) -> dict:
    """Get the all QUDT quantity kinds."""
    logger.debug("Using sparql endpoint url %s", settings.SPARQL_URL)

    QUERY = f"""
PREFIX qudt: <http://qudt.org/schema/qudt/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT ?s ?p ?o
FROM <{settings.VOCAB_PREFIX}qudt/>
where {{
    ?s ?p ?o
    FILTER (
      contains(STR(?s), "https://vocab.sentier.dev/qudt/quantity-kind/")
    )
    FILTER (
        ?p IN (skos:prefLabel, skos:altLabel, skos:exactMatch, skos:related, skos:definition, qudt:informativeReference)
    )
}}
    """

    logger.debug("Executing query %s", QUERY)
    response = httpx.post(settings.SPARQL_URL, data={"query": QUERY})
    response.raise_for_status()

    lang_checker = partial(language_filter, lang=lang.lower() if lang else None)
    data = [
        (
            obj["s"]["value"],
            reformat_predicate_object(
                obj, remove_namespaces=remove_namespaces, strip_lang_codes=True
            ),
        )
        for obj in response.json()["results"]["bindings"]
        if lang_checker(obj["o"])
    ]
    logger.info(f"Retrieved {len(data)} quantity kinds")

    results = {}

    # Sorry this is shit but I lost 30 mins fighting with groupby
    # and am too burned out to find a better way...
    for qk, elem in data:
        if qk not in results:
            results[qk] = defaultdict(list)
        if len(elem) == 2:
            results[qk][elem[0]].append(elem[1])
        else:
            results[qk][elem[0]].append(elem[1:])

    return {
        key: {a: (b[0] if len(b) == 1 else b) for a, b in value.items()}
        for key, value in results.items()
    }


def get_all_data_for_qk_iri(
    iri: str,
    lang: str | None = None,
    remove_namespaces: bool = True,
    graph_namespaces: list[str] = ["qudt", "simapro"],
) -> dict:
    """Get all data for a given quantity kind IRI."""
    logger.debug("Using sparql endpoint url %s", settings.SPARQL_URL)

    results = []

    for graph_namespace in graph_namespaces:
        QUERY = f"""
PREFIX qudt: <http://qudt.org/schema/qudt/>

SELECT ?s ?p ?o
FROM <{settings.VOCAB_PREFIX}{graph_namespace}/>
where {{
    ?s ?p ?o .
    ?s qudt:hasQuantityKind <{iri}>
}}
        """

        logger.debug("Executing query %s", QUERY)
        response = httpx.post(settings.SPARQL_URL, data={"query": QUERY})
        response.raise_for_status()
        response = response.json()["results"]["bindings"]
        logger.info(
            "Retrieved %s results for quantity kind %s in graph %s",
            len(response),
            iri,
            settings.VOCAB_PREFIX + graph_namespace,
        )
        results.extend(response)

    lang_checker = partial(language_filter, lang=lang.lower() if lang else None)

    return {
        key: {
            (
                remove_graph_namespaces(obj_key) if remove_namespaces else obj_key
            ): format_objects(obj, lang)
            for obj_key, obj in groupby(group, key=lambda x: x["p"]["value"])
        }
        for key, group in groupby(results, key=lambda x: x["s"]["value"])
    }


def format_objects(obj, lang: Optional[str] = None):
    l = list(
        map(
            lambda x: x["o"]["value"],
            filter(
                lambda x: "xml:lang" not in x["o"] or language_filter(x["o"], lang),
                obj,
            ),
        )
    )
    if len(l) == 0:
        return None
    return l if len(l) > 1 else l[0]

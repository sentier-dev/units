from functools import partial
from itertools import groupby

import structlog
import httpx

from units.settings import get_settings

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


def language_filter(o: dict, lang: str) -> dict:
    """Check if given element has the correct language, if one is given"""
    if "xml:lang" in o and lang not in o["xml:lang"].lower():
        return False
    return True


def get_qk_for_iri(iri: str) -> str | None:
    """Get the QUDT quantity key for a given unit IRI."""
    settings = get_settings()
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
    response = httpx.post(settings.SPARQL_URL, data={"query": QUERY}).json()
    logger.info(f"Retrieved {len(response)} quantity kind results for iri {iri}")
    return response[0]["qk"] if response else None


def get_all_data_for_qk_iri(
    iri: str,
    lang: str | None = None,
    remove_namespaces: bool = True,
    graph_namespaces: list[str] = ["qudt", "simapro"],
) -> dict:
    """Get all data for a given quantity kind IRI."""
    settings = get_settings()
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
        response = httpx.post(settings.SPARQL_URL, data={"query": QUERY}).json()[
            "results"
        ]["bindings"]
        logger.info(
            "Retrieved %s results for quantity kind %s in graph %s",
            len(response),
            iri,
            settings.VOCAB_PREFIX + graph_namespace,
        )
        results.extend(response)

    if remove_namespaces:
        formatter = remove_graph_namespaces
    else:
        formatter = lambda x: x

    if lang:
        o_checker = partial(language_filter, lang=lang.lower())
    else:
        o_checker = lambda _: True

    return {
        key: [
            (formatter(obj["p"]["value"]), formatter(obj["o"]["value"]))
            for obj in group
            if o_checker(obj["o"])
        ]
        for key, group in groupby(results, key=lambda x: x["s"]["value"])
    }

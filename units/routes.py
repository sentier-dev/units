from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi_versioning import version

from units.concepts import get_all_data_for_qk_iri, get_qk_for_iri, get_quantity_kinds
from units.schema import VersionResponse

router = APIRouter()


@router.get("/search")
@version(0, 1)
async def search(
    search_term: str,
    lang: str = "en",
) -> str:
    """Search concepts according to given expression.

    Args:
        search_term (str): The search term to filter the concepts.
        lang (str): The language to use for searching concepts. Defaults to "en".

    Returns:
        list[ConceptResponse]: The search results, if any.
    """
    return "{search_term} in {lang}"


@router.get("/unit")
@version(0, 1)
async def get_concept_data(
    iri: str,
    remove_namespaces: bool = True,
    lang: str | None = None,
) -> str:
    """
    Returns all concepts in the same QUDT quantity kind class as the unit `iri`. Data is formatted
    as a JSON `Map`, with keys of unit IRIs, and values of values of maps of `{key: value}`. Because
    the same key can be used more than once (e.g. a `prefLabel` can have values in different
    languages), the `value` can be either a single object or an array of objects.

    Pass `remove_namespaces` to control the verbosity of the response. By default, some common
    namespace prefixes of the predicates and objects are removed:

    * http://qudt.org/schema/qudt/
    * http://www.w3.org/1999/02/22-rdf-syntax-ns#
    * http://www.w3.org/2004/02/skos/core#

    Use `lang` to control what language codes are available in the response. Response data can
    include RDF literals with many languages, and the default is not to do any filtering. If you
    pass `lang`, then only RDF literals who explicitly provide a language code which starts the same
    as `lang` will be returned. In other words `lang='en'` will return object literals without a
    language code, with a `en` language code, with a `en_GB` language code, but not a `jp` code.

    """
    try:
        qk = get_qk_for_iri(iri)
    except KeyError:
        raise HTTPException(status_code=404, detail="Unit IRI not found")

    result = get_all_data_for_qk_iri(
        iri=qk, lang=lang, remove_namespaces=remove_namespaces
    )
    return JSONResponse(content=result)


@router.get("/quantity_kinds")
@version(0, 1)
async def get_quantity_kinds_data(
    remove_namespaces: bool = True,
    lang: str | None = None,
) -> str:
    """
    Returns all quantity kinds concepts. Data is formatted as a JSON `Map`, with keys of unit IRIs,
    and values of maps of `{key: value}`. Because the same key can be used more than once (e.g. a
    `prefLabel` can have values in different languages), the `value` can be either a single object
    or an array of objects.

    Pass `remove_namespaces` to control the verbosity of the response. By default, some common
    namespace prefixes of the predicates and objects are removed:

    * http://qudt.org/schema/qudt/
    * http://www.w3.org/1999/02/22-rdf-syntax-ns#
    * http://www.w3.org/2004/02/skos/core#

    Use `lang` to control what language codes are available in the response. Response data can
    include RDF literals with many languages, and the default is not to do any filtering. If you
    pass `lang`, then only RDF literals who explicitly provide a language code which starts the same
    as `lang` will be returned. In other words `lang='en'` will return object literals without a
    language code, with a `en` language code, with a `en_GB` language code, but not a `jp` code.

    """
    result = get_quantity_kinds(lang=lang, remove_namespaces=remove_namespaces)
    return JSONResponse(content=result)


@router.get("/version")
@version(0, 1)
async def get_version() -> VersionResponse:
    """Get the version of the server.

    Returns:
        VersionResponse: The version of the server.
    """
    return VersionResponse()

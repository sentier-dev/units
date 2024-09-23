from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi_versioning import version

from units.schema import VersionResponse
from units.concepts import get_qk_for_iri, get_all_data_for_qk_iri

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
    as a JSON `Map`, with keys of unit IRIs, and values of lists of `[predicate, object]`.

    We use lists because a given unit can share the same predicate relation with more than one
    object. For example, a unit could have multiple preferred labels in different languages.

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
    if lang and not len(lang) == 2:
        raise HTTPException(
            status_code=500, detail="Lang string must be exactly two letters long"
        )

    qk = get_qk_for_iri(iri)
    if not qk:
        raise HTTPException(status_code=404, detail="Unit IRI not found")

    result = get_all_data_for_qk_iri(
        iri=qk, lang=lang, remove_namespaces=remove_namespaces
    )
    return JSONResponse(content=result)


# https://vocab.sentier.dev/qudt/unit/M-SEC


@router.get("/version")
@version(0, 1)
async def get_version() -> VersionResponse:
    """Get the version of the server.

    Returns:
        VersionResponse: The version of the server.
    """
    return VersionResponse()

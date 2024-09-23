"""Routes for the units server."""

from fastapi import APIRouter, Depends, Request
from fastapi_versioning import version

# from units.auth import validate_api_key
from units.schema import VersionResponse

router = APIRouter()


@router.get("/search")
@version(0, 1)
def search(
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
def get_concept_scheme(
    iri: str,
    lang: str = "en",
) -> str:
    """
    Returns a concept scheme.

    Args:
        iri (str): The concept scheme IRI.
        lang (str): The language. Defaults to "en".

    Returns:
        FullConceptSchemeResponse: The concept scheme with member
            concepts and collections.
    """
    return controller.get_concept_scheme(concept_scheme_iri, lang=lang)


@router.get("/version")
@version(0, 1)
def get_version() -> VersionResponse:
    """Get the version of the server.

    Returns:
        VersionResponse: The version of the server.
    """
    return VersionResponse()

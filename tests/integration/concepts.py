import pytest

from units.concepts import get_all_data_for_qk_iri, get_qk_for_iri


def test_qk():
    assert (
        get_qk_for_iri("https://vocab.sentier.dev/qudt/unit/M-SEC")
        == "https://vocab.sentier.dev/qudt/quantity-kind/LengthTime"
    )
    assert get_qk_for_iri("w00t") is None


def test_gadfqi():
    result = get_all_data_for_qk_iri(
        "https://vocab.sentier.dev/qudt/quantity-kind/LengthTime"
    )
    assert "https://vocab.sentier.dev/qudt/unit/M-SEC" in result
    subset = result["https://vocab.sentier.dev/qudt/unit/M-SEC"]
    assert ("prefLabel", "Metre second") in subset


def test_gadfqi_empty():
    assert not get_all_data_for_qk_iri("https://vocab.sentier.dev/qudt/quantity-kind/L")


def test_gadfqi_error():
    with pytest.raises(ValueError):
        get_all_data_for_qk_iri(
            "https://vocab.sentier.dev/qudt/quantity-kind/LengthTime", lang="abc"
        )


def test_gadfqi_namespaces():
    result = get_all_data_for_qk_iri(
        "https://vocab.sentier.dev/qudt/quantity-kind/LengthTime",
        remove_namespaces=False,
    )
    assert "https://vocab.sentier.dev/qudt/unit/M-SEC" in result
    subset = result["https://vocab.sentier.dev/qudt/unit/M-SEC"]
    assert ("http://www.w3.org/2004/02/skos/core#prefLabel", "Metre second") in subset

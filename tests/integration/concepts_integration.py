import pytest

from units.concepts import get_all_data_for_qk_iri, get_qk_for_iri, get_quantity_kinds


def test_qk():
    assert (
        get_qk_for_iri("https://vocab.sentier.dev/qudt/unit/M-SEC")
        == "https://vocab.sentier.dev/qudt/quantity-kind/LengthTime"
    )
    with pytest.raises(KeyError):
        get_qk_for_iri("w00t")


def test_gadfqi():
    result = get_all_data_for_qk_iri(
        "https://vocab.sentier.dev/qudt/quantity-kind/LengthTime"
    )
    assert "https://vocab.sentier.dev/qudt/unit/M-SEC" in result
    subset = result["https://vocab.sentier.dev/qudt/unit/M-SEC"]
    assert ("prefLabel", "Metre second", "en-gb") in subset


def test_gadfqi_empty():
    assert not get_all_data_for_qk_iri("https://vocab.sentier.dev/qudt/quantity-kind/L")


def test_gadfqi_namespaces():
    result = get_all_data_for_qk_iri(
        "https://vocab.sentier.dev/qudt/quantity-kind/LengthTime",
        remove_namespaces=False,
    )
    assert "https://vocab.sentier.dev/qudt/unit/M-SEC" in result
    subset = result["https://vocab.sentier.dev/qudt/unit/M-SEC"]
    assert ("http://www.w3.org/2004/02/skos/core#prefLabel", "Metre second", "en-gb") in subset


def test_get_quantity_kinds():
    result = get_quantity_kinds(
        remove_namespaces=True,
    )
    assert "https://vocab.sentier.dev/qudt/quantity-kind/Acceleration" in result
    subset = result["https://vocab.sentier.dev/qudt/quantity-kind/Acceleration"]
    assert subset["informativeReference"] == "http://en.wikipedia.org/wiki/Acceleration"
    assert ("accélération", "fr") in subset["prefLabel"]
    assert len(subset["prefLabel"]) > 1

    subset = result["https://vocab.sentier.dev/qudt/quantity-kind/Enthalpy"]
    assert len(subset["prefLabel"]) > 1

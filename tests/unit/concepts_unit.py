import pytest

from units.concepts import (
    remove_graph_namespaces,
    language_filter,
    reformat_predicate_object,
)


def test_remove_graph_namespaces():
    assert (
        remove_graph_namespaces("http://www.w3.org/2004/02/skos/core#notation")
        == "notation"
    )
    assert remove_graph_namespaces("/skos/core#notation") == "/skos/core#notation"


def test_language_filter_right_side_bigger():
    assert not language_filter({"xml:lang": "en"}, "en-GB")


def test_language_filter_left_side_bigger():
    assert language_filter({"xml:lang": "en-GB"}, "en")


def test_language_filter_none():
    assert language_filter({"xml:lang": "en-GB"}, None)
    assert language_filter({}, None)


def test_language_filter_accept_no_lang_code():
    assert language_filter({}, "en-GB")


def test_reformat_predicate_object():
    given = {
        "p": {"value": "http://www.w3.org/2004/02/skos/core#notation"},
        "o": {"value": "w00t"},
    }
    expected = (
        "http://www.w3.org/2004/02/skos/core#notation",
        "w00t",
    )
    assert reformat_predicate_object(given, remove_namespaces=False) == expected


def test_reformat_predicate_object_remove_namespaces():
    given = {
        "p": {"value": "http://www.w3.org/2004/02/skos/core#notation"},
        "o": {"value": "w00t"},
    }
    expected = (
        "notation",
        "w00t",
    )
    assert reformat_predicate_object(given) == expected


def test_reformat_predicate_object_include_language():
    given = {
        "p": {"value": "http://www.w3.org/2004/02/skos/core#notation"},
        "o": {"value": "w00t", "xml:lang": "en-GB"},
    }
    expected = (
        "notation",
        "w00t",
        "en-gb"
    )
    assert reformat_predicate_object(given) == expected

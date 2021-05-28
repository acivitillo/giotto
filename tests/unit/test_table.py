import pytest
from dominate.tags import html_tag
from giotto.table import Body, Filters, Head, Pagination, Table

from ..conftest import clear_string


@pytest.fixture
def table_data():
    data = [
        {"id": 1, "name": "Jon", "surname": "Smith", "age": 19},
        {"id": 2, "name": "Kate", "surname": "Black", "age": 26},
        {"id": 3, "name": "Sandy", "surname": "Angel", "age": 30},
        {"id": 4, "name": "Matt", "surname": "Black", "age": 40},
    ]
    return data


@pytest.fixture
def table(table_data):
    table = Table(data=table_data)
    return table


def test_filters():
    filters = Filters()
    test_input = filters.__get__(None, None)
    assert isinstance(test_input, html_tag)
    assert "input" in test_input.render()


def test_head(table):
    head = Head()
    test_input = head.__get__(table, None)
    assert isinstance(test_input, html_tag)
    assert "thead" in test_input.render()
    assert "surname" in test_input.render()


def test_body(table):
    body = Body()
    test_input = body.__get__(table, None)
    assert isinstance(test_input, html_tag)
    assert "tbody" in test_input.render()
    assert "Sandy" in test_input.render()


def test_pagination(table):
    pagination = Pagination()
    test_input = pagination.__get__(table, None)
    assert isinstance(test_input, html_tag)
    assert "nav" in test_input.render()
    assert "button" in test_input.render()


def test_table_columns(table):
    expected = ["id", "name", "surname", "age"]
    test_input = table.columns
    assert test_input == expected


def test_table_total_rows(table):
    test_input = table.total_rows
    assert test_input == 4


def test_table_to_tag(table):
    expected = (
        '<div class="shadow" data-controller="table" data-table-max-page-rows-v'
        f'alue="1"> {table._filters.render()} <div class="overflow-x-auto">'
        f'<table class="w-full table-fixed"> {table._thead.render()} '
        f"{table._tbody.render()}</table></div>{table._pagination.render()}</div>"
    )
    test_input = table._to_tag().render()
    assert clear_string(test_input) == clear_string(expected)

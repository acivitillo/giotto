from dominate.svg import svg
from dominate.tags import div
import pytest

from giotto.elements import (
    Button,
    ClickableIcon,
    Column,
    ConnectedDropdowns,
    Input,
    MultiSelect,
    Row,
    Select,
    Text,
)
from giotto.icons import Icon
from ..conftest import clear_string


@pytest.fixture
def icon():
    class TestIcon(Icon):
        def _to_tag(self):
            return svg()

    return TestIcon()


def test_button_empty():
    partial = Button()
    expected = f'<button class="{partial._class}"><span>Submit</span></button>'
    test_input = partial.render()
    assert clear_string(test_input) == clear_string(expected)


def test_button_with_icon(icon):
    partial = Button(icon=icon)
    expected = f'<button class="{partial._class}"><svg></svg><span>Submit</span></button>'
    test_input = partial.render()
    assert clear_string(test_input) == clear_string(expected)


def test_clickable_icon(icon):
    partial = ClickableIcon(icon=icon)
    expected = f'<div class="{partial._class}"><svg></svg></div>'
    test_input = partial.render()
    assert clear_string(test_input) == clear_string(expected)


def test_column_empty():
    partial = Column(contents=[])
    expected = f'<div class="{partial._class}"></div>'
    test_input = partial.render()
    assert clear_string(test_input) == clear_string(expected)


def test_column_with_contents():
    partial = Column(contents=[Column(contents=[])])
    expected = f'<div class="{partial._class}"><div class="{partial._class}"></div></div>'
    test_input = partial.render()
    assert clear_string(test_input) == clear_string(expected)


def test_connected_dropdowns_filter_data():
    data = {"col1": ["Bob", "Bob", "Cole"], "col2": [1, 2, 3]}
    partial = ConnectedDropdowns(data=data, filters={"col1": "Bob"})
    test_input = partial.filter_data()
    expected = {"col1": ["Bob", "Bob", "Cole"], "col2": [1, 2]}
    assert test_input == expected


def test_connected_dropdowns_no_filter():
    data = {"col1": ["Bob", "Bob"], "col2": [1, 2]}
    partial = ConnectedDropdowns(data=data)
    select_1 = Select(options=["Bob"], name="col1")
    select_2 = Select(options=[1, 2], name="col2")
    expected = select_1.render() + select_2.render()
    test_input = partial.render()
    assert clear_string(test_input) == clear_string(expected)


def test_connected_dropdowns_with_filter():
    data = {"col1": ["Bob", "Bob", "Cole"], "col2": [1, 2, 3]}
    partial = ConnectedDropdowns(data=data, filters={"col1": "Cole"})
    select_1 = Select(options=["Bob", "Cole"], name="col1", selected="Cole")
    select_2 = Select(options=[3], name="col2")
    expected = select_1.render() + select_2.render()
    test_input = partial.render()
    assert clear_string(test_input) == clear_string(expected)


def test_connected_dropdowns_to_tag():
    data = {"col1": ["Bob", "Bob"], "col2": [1, 2]}
    partial = ConnectedDropdowns(data=data)
    assert partial.to_tag().render() == div(partial.to_tags()).render()


def test_input_empty():
    partial = Input()
    expected = f'<input class="{partial._class}" placeholder="" type="text">'
    test_input = partial.render()
    assert clear_string(test_input) == clear_string(expected)


def test_input_with_value():
    partial = Input(value="hello")
    expected = f'<input class="{partial._class}" placeholder="" type="text" value="hello">'
    test_input = partial.render()
    assert clear_string(test_input) == clear_string(expected)


def test_multiselect_empty():
    partial = MultiSelect(options=[])
    expected = (
        f'<select class="{partial._class}" multiple="multiple"><option value=""></option></select>'
    )
    test_input = partial.render()
    assert clear_string(test_input) == clear_string(expected)


def test_multiselect_with_options():
    partial = MultiSelect(options=["1", "2"])
    expected = (
        f'<select class="{partial._class}" multiple="multiple"><option value=""></option>'
        "<option>1</option><option>2</option></select>"
    )
    test_input = partial.render()
    assert clear_string(test_input) == clear_string(expected)


def test_multiselect_with_selected():
    partial = MultiSelect(options=["1", "2"], selected=["1", "2"])
    expected = (
        f'<select class="{partial._class}" multiple="multiple"><option value=""></option>'
        '<option selected="selected">1</option><option selected="selected">2</option></select>'
    )
    test_input = partial.render()
    assert clear_string(test_input) == clear_string(expected)


def test_row_empty():
    partial = Row(contents=[])
    expected = f'<div class="{partial._class}"></div>'
    test_input = partial.render()
    assert clear_string(test_input) == clear_string(expected)


def test_row_with_contents():
    partial = Row(contents=[Row(contents=[])])
    expected = f'<div class="{partial._class}"><div class="{partial._class}"></div></div>'
    test_input = partial.render()
    assert clear_string(test_input) == clear_string(expected)


def test_select_empty():
    partial = Select(options=[])
    expected = f'<select class="{partial._class}"><option value=""></option></select>'
    test_input = partial.render()
    assert clear_string(test_input) == clear_string(expected)


def test_select_with_options():
    partial = Select(options=["1", "2"])
    expected = (
        f'<select class="{partial._class}"><option value=""></option>'
        "<option>1</option><option>2</option></select>"
    )
    test_input = partial.render()
    assert clear_string(test_input) == clear_string(expected)


def test_select_with_selected():
    partial = Select(options=["1", "2"], selected="2")
    expected = (
        f'<select class="{partial._class}"><option value=""></option>'
        '<option>1</option><option selected="selected">2</option></select>'
    )
    test_input = partial.render()
    assert clear_string(test_input) == clear_string(expected)


def test_text_empty():
    partial = Text(value="")
    expected = f'<div class="{partial._class}"></div>'
    test_input = partial.render()
    assert clear_string(test_input) == clear_string(expected)


def test_text_markdown():
    partial = Text(value="## Header\n* point one", render_format="markdown")
    expected = f'<div class="{partial._class}"><h2>Header</h2><ul><li>point one</li></ul></div>'
    test_input = partial.render()
    assert clear_string(test_input) == clear_string(expected)


def test_text_html():
    partial = Text(value="<h2>Header</h2><ul><li>point one</li></ul>", render_format="html")
    expected = f'<div class="{partial._class}"><h2>Header</h2><ul><li>point one</li></ul></div>'
    test_input = partial.render()
    assert clear_string(test_input) == clear_string(expected)

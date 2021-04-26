from ..giotto.elements import Select, MultiSelect, Input


def clear_sting(s: str):
    return s.replace("\n", "").replace(" ", "")


def test_select_empty():
    partial = Select(options=[])
    expected = f'<select class="{Select._class}"><option value=""></option></select>'
    test_input = partial.render()
    assert clear_sting(test_input) == clear_sting(expected)


def test_select_with_options():
    partial = Select(options=["1", "2"])
    expected = (
        f'<select class="{Select._class}"><option value=""></option>'
        "<option>1</option><option>2</option></select>"
    )
    test_input = partial.render()
    assert clear_sting(test_input) == clear_sting(expected)


def test_select_with_selected():
    partial = Select(options=["1", "2"], selected="2")
    expected = (
        f'<select class="{Select._class}"><option value=""></option>'
        '<option>1</option><option selected="selected">2</option></select>'
    )
    test_input = partial.render()
    assert clear_sting(test_input) == clear_sting(expected)


def test_multiselect_empty():
    partial = MultiSelect(options=[])
    expected = (
        f'<select class="{Select._class}" multiple="multiple"><option value=""></option></select>'
    )
    test_input = partial.render()
    assert clear_sting(test_input) == clear_sting(expected)


def test_multiselect_with_options():
    partial = MultiSelect(options=["1", "2"])
    expected = (
        f'<select class="{Select._class}" multiple="multiple"><option value=""></option>'
        "<option>1</option><option>2</option></select>"
    )
    test_input = partial.render()
    assert clear_sting(test_input) == clear_sting(expected)


def test_multiselect_with_selected():
    partial = MultiSelect(options=["1", "2"], selected=["1", "2"])
    expected = (
        f'<select class="{Select._class}" multiple="multiple"><option value=""></option>'
        '<option selected="selected">1</option><option selected="selected">2</option></select>'
    )
    test_input = partial.render()
    assert clear_sting(test_input) == clear_sting(expected)


def test_input_empty():
    partial = Input()
    expected = f'<input class="{partial._class}" placeholder="" type="text">'
    test_input = partial.render()
    assert clear_sting(test_input) == clear_sting(expected)


def test_input_with_value():
    partial = Input(value="hello")
    expected = f'<input class="{partial._class}" placeholder="" type="text" value="hello">'
    test_input = partial.render()
    assert clear_sting(test_input) == clear_sting(expected)

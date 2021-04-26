from ..giotto.elements import Select


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

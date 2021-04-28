from dominate.tags import div
import pytest

from ..giotto.base import HXAction, Style
from .conftest import CustomPartial


params_hx_action_to_dict = [
    (dict(), dict()),
    (
        {"url": "/app_1", "confirm": "Are you sure you want to run this?"},
        {"data-hx-post": "/app_1", "data-hx-confirm": "Are you sure you want to run this?"},
    ),
]


@pytest.mark.parametrize("test_input,expected", params_hx_action_to_dict)
def test_hx_action_to_dict(test_input, expected):
    hx_action = HXAction(**test_input)
    assert hx_action.to_dict() == expected


params_style_apply = [
    (div(), dict(), div()),
    (div(), {"height": 12}, div(_class="h-12")),
    (div(), {"rounded": True}, div(_class="rounded-sm")),
    (div(), {"custom": "w-10"}, div(_class="w-10")),
    (div(_class="h-10"), {"width": 12, "margin": 3}, div(_class="h-10 w-12 m-3")),
    (div(_class="h-10 w-9"), {"custom": "w-10", "custom_remove": "w-9"}, div(_class="h-10 w-10")),
]


@pytest.mark.parametrize("initial_state,style,expected", params_style_apply)
def test_style_apply(initial_state, style, expected):
    style = Style(**style)
    style.apply(initial_state)
    assert initial_state.render() == expected.render()


def test_partial___eq__():
    assert CustomPartial() == CustomPartial()
    assert CustomPartial(id_="partial_1") != CustomPartial(id_="partial_2")


def test_partial___str__():
    partial = CustomPartial()
    assert str(partial) == "<div></div>"


def test_partial_to_tag():
    partial = CustomPartial()
    assert partial.to_tag().render() == div().render()


def test_partial_to_tags():
    partial = CustomPartial()
    html_list = [tag.render() for tag in partial.to_tags()]
    assert html_list == [div().render()]


def test_partial_render():
    partial = CustomPartial()
    assert partial.render() == "<div></div>"


def test_partial__repr_html_():
    partial = CustomPartial()
    assert partial._repr_html_() == "<div></div>"


params__update_tag = [
    (dict(id_="partial"), div(_id="partial")),
    (dict(name="partial"), div(name="partial")),
    (dict(action=HXAction(target="#my_frame")), div(data_hx_target="#my_frame")),
    (dict(style=Style(margin=3)), div(_class="m-3")),
]
ids__update_tag = ["id", "name", "action", "style"]


@pytest.mark.parametrize("test_input,expected", params__update_tag, ids=ids__update_tag)
def test_partial__update_tag(test_input, expected):
    partial = CustomPartial(**test_input)
    tag = div()
    partial._update_tag(tag)
    assert tag.render() == expected.render()
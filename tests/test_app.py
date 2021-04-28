from dominate.tags import html_tag
import pytest

from ..giotto.app import AppFunction, Frame, Site
from .conftest import clear_string


@pytest.fixture
def app_function():
    app_function = AppFunction(id_="my_func", func=lambda x: x, prefix="/test")
    return app_function


@pytest.fixture
def frame_func(partial):
    def frame_func(x: int = 1):
        return [partial]

    return frame_func


@pytest.fixture
def frame(frame_func):
    frame = Frame(id_="my_frame", func=frame_func, prefix="/test")
    return frame


@pytest.fixture
def site():
    site = Site()
    return site


def test_app_function_arguments(app_function):
    assert app_function.arguments == ["x"]


def test_app_function_run(app_function):
    assert app_function.run(x=1) == 1


def test_app_function_get_hx_action_without_func_kwargs(app_function):
    test_input = app_function.get_hx_action().dict()["url"]
    expected = "/test/receiver?func_name=my_func"
    assert test_input == expected


def test_app_function_get_hx_action_with_func_kwargs(app_function):
    test_input = app_function.get_hx_action(func_kwargs={"x": 1}).dict()["url"]
    expected = "/test/receiver?func_name=my_func&x=1"
    assert test_input == expected


def test_frame_run(frame):
    assert frame.run() == "<div></div>"


def test_frame_to_partials(frame_func, frame):
    assert frame.to_partials() == frame_func()
    assert frame.to_partials(x=2) == frame_func()


def test_frame_to_tag(frame):
    test_input = frame.to_tag().render()
    expected = (
        '<div autocomplete="off" class="flex flex-row items-center '
        'mb-2 shadow rounded" id="my_frame"><div></div></div>'
    )
    assert clear_string(test_input) == clear_string(expected)


def test_frame_to_tags(frame):
    test_input = [tag.render() for tag in frame.to_tags()]
    assert test_input == ["<div></div>"]


def test_site_body(site):
    test_input = site.body.render()
    expected = f"<body>{site.body_container.render()}</body>"
    assert clear_string(test_input) == clear_string(expected)


def test_site_body_container(site):
    test_input = site.body_container.render()
    main = '<main class="pt-8 px-8 overflow-x-auto flex-1"><div></div></main>'
    expected = f'<div class="flex" style="height: 95vh">{main}</div>'
    assert clear_string(test_input) == clear_string(expected)


def test_site_head(site):
    assert isinstance(site.head, html_tag)


def test_site_render(site):
    test_input = site.render()
    expected = (
        "<!DOCTYPEhtml><html><head><title>Giotto</title></head>"
        f"<body>{site.head.render()}{site.body.render()}</body></html>"
    )
    assert clear_string(test_input) == clear_string(expected)


def test_site_to_html(site):
    assert site.to_html() == site.render()
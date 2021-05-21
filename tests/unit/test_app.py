from typing import Callable

from dominate.tags import html_tag
from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest

from giotto.app import App, AppFunction, BaseApp, Frame, MainApp, Site
from ..conftest import clear_string


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
    frame = Frame(id_="frame_func", func=frame_func, prefix="/test")
    return frame


@pytest.fixture
def site():
    site = Site()
    return site


@pytest.fixture
def base_app_with_frame(frame):
    base_app = BaseApp(app=FastAPI(), frames={frame.id_: frame})
    return base_app


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


def test_app__init__():
    app = App(prefix="/my_app")
    test_input = [route.path for route in app.app.routes]
    expected = ["/my_app/receiver", "/my_app/"]
    assert test_input == expected


def test_base_app_render(base_app_with_frame, frame):
    test_input = base_app_with_frame.render()
    expected = frame.to_tag().render()
    assert test_input.startswith("<!DOCTYPE html>")
    assert clear_string(expected) in clear_string(test_input)


def test_base_app_to_html(base_app):
    assert base_app.to_html() == base_app.render()


def test_base_app_functions(base_app, base_app_with_frame, frame):
    assert base_app.functions == {}
    assert base_app_with_frame.functions == {frame.id_: frame}


def test_base_app_get_action(base_app_with_frame, frame):
    assert base_app_with_frame.get_action(name=frame.id_) == frame.get_hx_action()


def test_base_app_action(base_app):
    @base_app.action()
    def my_action():
        pass

    assert "my_action" in base_app.actions

    test_input = base_app.actions["my_action"].dict()
    assert test_input["id_"] == "my_action"
    assert test_input["prefix"] == ""
    assert isinstance(test_input["func"], Callable)


def test_base_app_frame(base_app, frame):
    base_app.frame()(frame.func)

    assert "frame_func" in base_app.frames

    test_input = base_app.frames["frame_func"].dict()
    assert test_input["id_"] == "frame_func"
    assert test_input["prefix"] == ""
    assert isinstance(test_input["func"], Callable)


def test_base_app_get_request(base_app):
    base_app.add_api_routes()
    client = TestClient(base_app.app)
    response = client.get("/")
    assert response.status_code == 200

    test_input = response.content.decode("utf-8")
    expected = base_app.to_html()
    assert test_input == expected


def test_base_app_post_request_action(base_app):
    @base_app.action()
    def my_action(msg):
        return msg

    base_app.add_api_routes()
    client = TestClient(base_app.app)
    response = client.post("/receiver?func_name=my_action&msg=hello")
    assert response.status_code == 200

    test_input = response.content.decode("utf-8")
    expected = "hello"
    assert test_input == expected


def test_base_app_post_request_frame(base_app_with_frame):
    base_app_with_frame.add_api_routes()
    client = TestClient(base_app_with_frame.app)
    response = client.post("/receiver?func_name=frame_func")
    assert response.status_code == 200

    test_input = response.content.decode("utf-8")
    expected = "<div></div>"
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
        'mb-2 shadow rounded" id="frame_func"><div></div></div>'
    )
    assert clear_string(test_input) == clear_string(expected)


def test_frame_to_tags(frame):
    test_input = [tag.render() for tag in frame.to_tags()]
    assert test_input == ["<div></div>"]


def test_main_app__init__single():
    app = MainApp()
    test_input = [route.path for route in app.app.routes]
    expected = [
        "/openapi.json",
        "/docs",
        "/docs/oauth2-redirect",
        "/redoc",
        "/receiver",
        "/",
        "/giotto-statics",
    ]
    assert test_input == expected


def test_main_app__init__with_subapp():
    subapp = App(prefix="/my_app")
    app = MainApp(apps=[subapp])
    test_input = [route.path for route in app.app.routes]
    expected = [
        "/openapi.json",
        "/docs",
        "/docs/oauth2-redirect",
        "/redoc",
        "/receiver",
        "/",
        "/my_app/receiver",
        "/my_app/",
        "/giotto-statics",
    ]
    assert test_input == expected


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
        "<!DOCTYPE html><html><head><title>Giotto</title></head>"
        f"<body>{site.head.render()}{site.body.render()}</body></html>"
    )
    assert clear_string(test_input) == clear_string(expected)


def test_site_to_html(site):
    assert site.to_html() == site.render()

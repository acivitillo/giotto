from ..giotto.app import AppFunction
import pytest


@pytest.fixture
def app_function():
    app_function = AppFunction(id_="my_func", func=lambda x: x, prefix="/test")
    return app_function


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

from fastapi import FastAPI
from dominate.tags import div
import pytest

from giotto.app import BaseApp
from giotto.base import Partial


def clear_string(s: str):
    return s.replace("\n", "").replace(" ", "")


class CustomPartial(Partial):
    def _to_tag(self):
        return div()


@pytest.fixture
def partial():
    return CustomPartial()


@pytest.fixture()
def base_app():
    base_app = BaseApp(app=FastAPI())
    return base_app

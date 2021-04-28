from dominate.tags import div
import pytest

from ..giotto.base import Partial


def clear_string(s: str):
    return s.replace("\n", "").replace(" ", "")


class CustomPartial(Partial):
    def _to_tag(self):
        return div()


@pytest.fixture
def partial():
    return CustomPartial()

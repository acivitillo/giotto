from giotto.icons import (
    IconHMenu,
    IconDownarrow,
    IconFiles,
    IconSearch,
    IconDetails,
    IconPlay,
    IconStop,
    IconBin,
    IconFirstPage,
    IconPreviousPage,
    IconNextPage,
    IconLastPage,
    IconRefresh,
)
import pytest
from dominate.tags import html_tag

icons = [
    IconHMenu,
    IconDownarrow,
    IconFiles,
    IconSearch,
    IconDetails,
    IconPlay,
    IconStop,
    IconBin,
    IconFirstPage,
    IconPreviousPage,
    IconNextPage,
    IconLastPage,
    IconRefresh,
]


@pytest.mark.parametrize("icon", icons)
def test_icon_to_tag(icon):
    test_input = icon()._to_tag()
    assert isinstance(test_input, html_tag)


@pytest.mark.parametrize("icon", icons)
def test_icon_contains_svg(icon):
    test_input = icon()._to_tag().render()
    assert "svg" in test_input


@pytest.mark.parametrize("icon", icons)
def test_icon_contains_path(icon):
    test_input = icon()._to_tag().render()
    assert "path" in test_input

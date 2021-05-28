import pytest
from dominate.tags import html_tag
from giotto.navigation import TopBar

from ..conftest import clear_string


@pytest.fixture
def top_bar():
    return TopBar()


def test_top_bar_ul_left(top_bar):
    test_input = top_bar._ul_left.render()
    expected = (
        '<ul class="flex items-center"><li class="h-6w-8"><a href="#"><svg fill'
        '="none" stroke="currentColor" viewBox="002428" xmlns="http://www.w3.or'
        'g/2000/svg"><path color="white" d="M46h16M412h16M418h16" stroke-lineca'
        'p="round" stroke-line join="round"></path></svg></a></li></ul>'
    )
    assert clear_string(test_input) == clear_string(expected)


def test_top_bar_ul_center(top_bar):
    test_input = top_bar._ul_center.render()
    expected = (
        '<ul class="flex items-center"><li><h1 class="pl-8 lg:pl-0 text-whitefo'
        'nt-bold">Site Name</h1></li></ul>'
    )
    assert clear_string(test_input) == clear_string(expected)


def test_top_bar_ul_right(top_bar):
    test_input = top_bar._ul_right.render()
    expected = (
        '<ul class="flex items-center"><li class="h-10w-10"><img alt="profile b'
        'oss" class="h-full w-full rounded-full mx-auto" src="https://avatars.g'
        "ithubusercontent.com/u/54931660?s=400&amp;u=dcf5550498aee3550f2b2f8353"
        '45d802fabe1833&amp;v=4&amp;_sm_au_=iNVf4trk1MFNLSNnVsBFjK664v423"></li'
        "></ul>"
    )
    assert clear_string(test_input) == clear_string(expected)


def test_top_bar_to_tag(top_bar):
    test_input = top_bar.to_tag()
    assert isinstance(test_input, html_tag)

    test_input = test_input.render()
    expected = (
        f'<div class="flex-1 flex flex-col overflow-hidden" style="height:5vh">'
        '<nav class="p-4 flex justify-between bg-dark h-full border-cgrey_200">'
        f"{top_bar._ul_left.render()} {top_bar._ul_center.render()}"
        f"{top_bar._ul_right.render()}</nav></div>"
    )
    assert clear_string(test_input) == clear_string(expected)

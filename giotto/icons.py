from typing import List


from dominate.tags import _input, a, div, option, select, button

from .base import Partial
from .utils import svg, path


class Icon(Partial):
    pass


class IconHMenu(Icon):
    def _to_tag(self):
        tag = svg(
            xmlns="http://www.w3.org/2000/svg",
            fill="none",
            viewBox="0 0 24 28",
            stroke="currentColor",
        )
        _path = path(
            color="white",
            strokeLinecap="round",
            strokeLinejoin="round",
            d="M4 6h16M4 12h16M4 18h16",
        )
        tag.add(_path)
        return tag


class IconDownarrow(Icon):
    def _to_tag(self):
        tag = svg(
            _class="w-2 h-2 absolute top-0 right-0 m-4 pointer-events-none",
            xmlns="http://www.w3.org/2000/svg",
            viewBox="0 0 412 232",
        )
        _path = path(
            d=(
                "M206 171.144L42.678 7.822c-9.763-9.763-25.592-9.763-35.355 0-9"
                ".763 9.764-9.763 25.592 0 35.355l181 181c4.88 4.882 11.279 7.3"
                "23 17.677 7.323s12.796-2.441 17.678-7.322l181-181c9.763-9.764 "
                "9.763-25.592 0-35.355-9.763-9.763-25.592-9.763-35.355 0L206 17"
                "1.144z"
            ),
            fill="#648299",
            fill_rule="nonzero",
        )
        tag.add(_path)
        return tag


class IconFiles(Icon):
    def _to_tag(self):
        tag = svg(
            _class="h-5 w-5", viewBox="0 0 24 24", fill="none", xmlns="http://www.w3.org/2000/svg"
        )
        _path = path(
            d=(
                "M19 11H5M19 11C20.1046 11 21 11.8954 21 13V19C21 20.1046 20.10"
                "46 21 19 21H5C3.89543 21 3 20.1046 3 19V13C3 11.8954 3.89543 1"
                "1 5 11M19 11V9C19 7.89543 18.1046 7 17 7M5 11V9C5 7.89543 5.89"
                "543 7 7 7M7 7V5C7 3.89543 7.89543 3 9 3H15C16.1046 3 17 3.8954"
                "3 17 5V7M7 7H17"
            ),
            stroke="currentColor",
            stroke_width="2",
            stroke_linecap="round",
            stroke_linejoin="round",
        )
        tag.add(_path)
        return tag


class IconSearch(Icon):
    def _to_tag(self):
        tag = svg(
            _class="w-4 h-5 absolute top-0 right-0 m-3 pointer-events-none",
            xmlns="http://www.w3.org/2000/svg",
            fill="none",
            viewBox="0 0 24 24",
            stroke="currentColor",
        )
        _path = path(
            strokeLinecap="round",
            strokeLinejoin="round",
            d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z",
        )
        tag.add(_path)
        return tag

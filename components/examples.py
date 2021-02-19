from typing import List


from dominate.tags import _input, a, div, option, select, button

from base import Partial
from utils import svg, path
from icons import Icon, IconSearch


class Select(Partial):
    options: List[str]

    def _to_tag(self):
        tag = div(_class="relative inline-flex")
        _svg = svg(
            _class="w-2 h-2 absolute top-0 right-0 m-4 pointer-events-none",
            xmlns="http://www.w3.org/2000/svg",
            viewBox="0 0 412 232",
        )
        d = (
            "M206 171.144L42.678 7.822c-9.763-9.763-25.592-9.763-35.355 0-9.763"
            " 9.764-9.763 25.592 0 35.355l181 181c4.88 4.882 11.279 7.323 17.677"
            " 7.323s12.796-2.441 17.678-7.322l181-181c9.763-9.764 9.763-25.592"
            " 0-35.355-9.763-9.763-25.592-9.763-35.355 0L206 171.144z"
        )
        _svg.add(path(d=d, fill="#648299", fill_rule="nonzero"))
        tag.add(_svg)
        _class = (
            "border border-gray-300 text-gray-600 h-10 pl-5 pr-10 bg-white"
            " hover:border-gray-400 focus:outline-none appearance-none"
        )
        _select = select(_class=_class)
        for text in self.options:
            _select.add(option(text))
        tag.add(_select)
        return tag


class Input(Partial):
    icon: Icon = IconSearch()

    def _to_tag(self):

        tag = div(_class="relative inline-flex")
        input_ = _input(
            type="search",
            _class=(
                "border border-gray-300 text-gray-600 h-10 pl-5 pr-10 bg-white"
                " hover:border-gray-400 focus:outline-none appearance-none"
            ),
            placeholder="Search by name...",
        )
        tag.add(input_)
        tag.add(self.icon.to_tag())
        return tag


class TableAction(Partial):
    action_name: str

    def _to_tag(self):
        tag = a(href="#", _class="text-blue-400 hover:text-blue-600 underline")
        return tag


class Button(Partial):
    value: str
    color: str = "blue"

    def _to_tag(self):
        tag = button(
            self.value,
            _class=(
                f"uppercase px-8 py-2 bg-{self.color}-500 text-blue-50"
                " max-w-max shadow-sm hover:shadow-lg"
            ),
        )
        return tag

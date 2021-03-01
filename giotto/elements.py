from __future__ import annotations
from typing import Any, Dict, List, Optional

from dominate.tags import (
    _input,
    a,
    button,
    div,
    h1,
    img,
    li,
    option,
    select,
    table,
    tbody,
    td,
    th,
    thead,
    tr,
    ul,
    p,
    span,
)
from dominate.util import raw
from markdown import markdown

from .base import Partial
from .icons import Icon, IconSearch
from .utils import path, svg, turbo_frame


class Select(Partial):
    options: List[str]

    def _to_tag(self):
        tag = div(_class="relative inline-flex")
        _svg = svg(
            _class="w-4 h-3 absolute top-0 right-0 m-4 pointer-events-none",
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
            "border border-gray-300 text-gray-600 h-10 pl-5 w-56 bg-white"
            " hover:border-gray-400 focus:outline-none appearance-none mt-1"
        )
        _select = select(_class=_class)
        for text in self.options:
            _select.add(option(text))
        tag.add(_select)
        return tag


class Input(Partial):
    placeholder: str = "Search by name..."
    icon: Icon = IconSearch()

    def _to_tag(self):

        tag = div(_class="relative inline-flex")
        input_ = _input(
            type="search",
            _class=(
                "border border-gray-300 text-gray-600 h-10 pl-5 w-56 bg-white"
                " hover:border-gray-400 focus:outline-none appearance-none mt-1"
            ),
            placeholder=self.placeholder,
        )
        tag.add(input_)
        tag.add(self.icon.to_tag())
        return tag


class Box(Partial):
    contents: List[Partial]

    def _to_tag(self):
        tag = div(_class="container")
        for item in self.contents:
            tag.add(item.to_tag())
        return tag


class Row(Partial):
    contents: List[Partial]

    def _to_tag(self):
        tag = div(_class="flex flex-row")
        for item in self.contents:
            tag.add(item.to_tag())
        return tag


class Column(Partial):
    contents: List[Partial]

    def _to_tag(self):
        tag = div(_class="flex flex-col")
        for item in self.contents:
            tag.add(item.to_tag())
        return tag


class TableAction(Partial):
    description: str

    def _to_tag(self):
        tag = a(self.description, href="#", _class="text-blue-400 hover:text-blue-600 underline")
        return tag


class Button(Partial):
    description: str = ""
    icon: Optional[Icon]
    color: str = "blue"
    action: str
    name: str = ""
    is_flex: bool = False
    target_frame: str = ""

    def _to_tag(self):
        size = "px-5 h-12 "
        if self.is_flex:
            size = ""
        tag = button(
            data_controller="swapurl",
            data_action=f"click->swapurl#{self.action}",
            data_swapurl_name_value=self.name,
            data_swapurl_frame_value=self.target_frame,
            _class=(
                f"uppercase mt-1 {size}rounded-lg bg-{self.color}-400"
                f" items-center font-medium text-black max-w-max shadow-sm cursor-pointer"
                f" focus:bg-{self.color}-600 focus:outline-none focus:text-white"
                f" hover:shadow-lg hover:bg-{self.color}-600 hover:text-white"
            ),
        )
        if self.icon:
            tag.add(self.icon.to_tag())
        # _desc = p(self.description, _class="font-semibold")
        tag.add(span(self.description))
        return tag


class Table(Partial):
    data: List[Dict]
    name: Optional[str]
    description: Optional[str]
    max_rows: int = 2

    def _to_tag(self):
        tag = div(
            _class="container overflow-x-auto mx-auto mt-2 shadow sm:rounded-lg",
            data_controller="table",
            data_table_entries_value=self.max_rows,
        )
        _thead = self._get_thead()
        _tbody = self._get_tbody()
        _table = table(_thead, _tbody)
        pagination = self._get_pagination()
        tag.add(_table, pagination)
        return tag

    def _get_thead(self):
        _thead = thead(_class="bg-primary border-l-2 border-r-2 border-gray-200 text-white")
        if self.data:
            _thr = tr(_class="bg-dark text-white border border-gray-200")
            for key in self.data[0].keys():
                _th = th(key, _class="whitespace-nowrap py-2 p-3")
                _thr.add(_th)
            _thead.add(_thr)
        return _thead

    def _get_tbody(self):
        _tbody = tbody()
        for counter, row in enumerate(self.data):
            bg = "" if counter % 2 == 0 else "bg-gray-50"
            _tr = tr(
                _class=f"{bg} hover:bg-gray-200 border border-gray-200",
                data_table_target="row",
            )
            for value in row.values():
                if isinstance(value, Partial):
                    _td = td(_class="text-center p-2 border-0")
                    _td.add(value.to_tag())
                else:
                    _td = td(str(value), _class="text-center p-2 border-0")
                _tr.add(_td)
            _tbody.add(_tr)
        return _tbody

    def _get_pagination(self):
        desc = Text(value=f"{len(self.data)} results").to_tag()
        hide_button = button("Hide", data_action="click->table#hide")
        unhide_button = button("Unhide", data_action="click->table#unhide")
        prev_button = button("Prev", data_action="click->table#prev")
        next_button = button("Next", data_action="click->table#next")
        buttons = div(hide_button, unhide_button, prev_button, next_button)
        _div = div(desc, buttons, _class="flex justify-between border-t border-gray-300 sm:px-6")
        return _div


class Text(Partial):
    value: str
    size: str = "base"
    weight: str = "normal"

    def _to_tag(self):
        tag = div(
            raw(markdown(self.value)),
            _class=f"text-{self.size} font-{self.weight} m-1",
        )
        return tag


class Tab(Partial):
    name: str
    body: Partial

    def _to_tag(self):
        return self.body._to_tag()


class TabContainer(Partial):
    tabs: List[Tab]
    ### NEEDS TO BE CALCULATED SOMEHOW
    clicked: Tab

    def _to_tag(self):
        _tag = div(_class="flex-1 w-44 ml-5 mt-10")
        _style = div(_style="border-bottom: 2px solid #eaeaea")
        _ul = ul(_class="flex cursor-pointer")
        # DEFAULT FIRST ONE CLICKED
        if self.clicked == None:
            self.clicked = self.tabs[0]
            clicked_id = 0
        else:
            clicked_id = self.tabs.index(self.clicked)
        for index, tab in enumerate(self.tabs):
            if clicked_id == index:
                _ul.add(li(tab.name, _class="py-2 px-6 bg-white rounded-t-lg"))
            else:
                _ul.add(
                    li(tab.name, _class="py-2 px-6 bg-white rounded-t-lg text-gray-500 bg-gray-200")
                )
        _style.add(_ul)
        _tag.add(_style)
        ###  WE NEED TO APPEND TURBO FRAME
        # _tag.add(turbo_frame(self.clicked, url=self.clicked.name))


# USER CODE
# tab_1 = Tab(name='apple', body=Table())
# tab_2 = Tab(name='orange', body=Table())
# tab_3 = Tab(name='banana', body=Hbox(values=[Button(name='add', color='green'),
#                                              Button(name='remove', color='red'),
#                                              Table()]))

# tab_container_1 = TabContainer(tabs=[tab1, tab2, tab3])

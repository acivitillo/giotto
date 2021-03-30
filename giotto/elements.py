from __future__ import annotations
from typing import Dict, List, Optional

from dominate.tags import (
    _input,
    a,
    button,
    div,
    li,
    nav,
    option,
    select,
    span,
    table,
    tbody,
    td,
    th,
    thead,
    tr,
    ul,
    label,
)
from dominate.util import raw
from markdown import markdown

from .base import Partial
from .icons import (
    Icon,
    IconDownarrow,
    IconFirstPage,
    IconLastPage,
    IconNextPage,
    IconPreviousPage,
    IconSearch,
)
from pydantic import validator


class Select(Partial):
    options: List[str]
    selected: str = ""

    def _to_tag(self):
        class_ = (
            "border border-gray-300 text-gray-600 h-10 pl-5 w-56 bg-white"
            " hover:border-gray-400 focus:outline-none m-2"
        )
        tag = select(_class=class_)
        tag.add(option("", value=""))
        for text in self.options:
            option_ = option(text)
            if text == self.selected:
                option_.attributes["selected"] = "selected"
            tag.add(option_)
        return tag


class MultiSelect(Partial):
    options: List[str]
    selected: List[str] = []

    def _to_tag(self):
        class_ = (
            "border border-gray-300 text-gray-600 h-20 pl-5 w-56 bg-white"
            " hover:border-gray-400 focus:outline-none m-2"
        )
        tag = select(_class=class_, multiple="multiple")
        tag.add(option(_class="hidden"))
        for text in self.options:
            option_ = option(text)
            if text in self.selected:
                option_.attributes["selected"] = "selected"
            tag.add(option_)
        return tag


class Input(Partial):
    placeholder: str = "Search by name..."
    value: str = ""
    type_: str = "text"

    def _to_tag(self):
        class_ = (
            "border border-gray-300 text-gray-600 h-10 pl-5 w-56 bg-white"
            " hover:border-gray-400 focus:outline-none m-2"
        )
        tag = _input(type=self.type_, _class=class_, placeholder=self.placeholder)
        if self.value:
            tag.attributes["value"] = self.value
        return tag


class Box(Partial):
    contents: List[Partial]
    centered: bool = False

    def _to_tag(self):
        style = "container"
        if self.centered:
            style += " mx-auto w-full 2xl:w-1/2"
        tag = div(_class=style)
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


class Button(Partial):
    description: str = ""
    icon: Optional[Icon]
    color: str = "blue"
    is_flex: bool = False
    height: int = 12

    def _to_tag(self):
        size = f"px-5 h-{self.height} "
        if self.is_flex:
            size = ""
        _class = (
            f"uppercase mt-1 {size}rounded-lg bg-{self.color}-400"
            f" items-center font-medium text-black max-w-max shadow-sm cursor-pointer"
            f" focus:bg-{self.color}-600 focus:outline-none focus:text-white"
            f" hover:shadow-lg hover:bg-{self.color}-600 hover:text-white"
        )
        tag = button(_class=_class)
        if self.icon:
            tag.add(self.icon.to_tag())
        tag.add(span(self.description))
        return tag


class ClickableIcon(Partial):
    icon: Icon

    def _to_tag(self):
        tag = div(
            _class="w-4 mr-2 transform hover:text-purple-500 hover:scale-110 cursor-pointer",
        )
        tag.add(self.icon.to_tag())
        return tag


class Table(Partial):
    data: List[Dict]
    description: Optional[str]
    max_rows: int = 1
    column_width: Dict = {}

    def _to_tag(self):
        tag = div(
            _class="mt-2 shadow sm:rounded-lg",
            data_controller="table",
            data_table_max_page_rows_value=self.max_rows,
        )
        filters = self.filters
        _div_table = div(_class="overflow-x-auto")
        _table = table(self.thead, self.tbody, _class="w-full table-fixed")
        _div_table.add(_table)
        pagination = self.pagination
        tag.add(filters, _div_table, pagination)
        return tag

    @property
    def filters(self):
        div_ = div(_class="relative inline-flex")
        input_ = _input(
            type="search",
            _class=(
                "border border-gray-300 text-gray-600 h-10 pl-5 w-56 bg-white"
                " hover:border-gray-400 focus:outline-none appearance-none mt-1"
            ),
            placeholder="Search",
            data_action="input->table#filter",
            data_table_target="input",
        )
        div_.add(input_)
        div_.add(IconSearch().to_tag())
        return div_

    @property
    def thead(self):
        _thead = thead(_class="bg-primary text-white")
        if self.data:
            _thr = tr(_class="bg-dark text-white")
            for key in self.data[0].keys():
                _span = span(key, _title=key)
                width = self.column_width.get(key)
                _style = "" if not width else f"width: {width}"
                _th = th(
                    _span, _class="whitespace-nowrap py-2 resize-x truncate min-w-2", _style=_style
                )
                _thr.add(_th)
            _thead.add(_thr)
        return _thead

    @property
    def tbody(self):
        _tbody = tbody()
        for counter, row in enumerate(self.data):
            bg = "" if counter % 2 == 0 else "bg-gray-50 "
            hidden = "" if counter < self.max_rows else " hidden"
            _tr = tr(
                _class=f"{bg}hover:bg-gray-200 border-b h-6 border-gray-200 truncate{hidden}",
                data_table_target="row",
            )
            for value in row.values():
                if isinstance(value, Partial):
                    _td = td(_class="flex item-center justify-center p-2 border-0")
                    _td.add(value.to_tag())
                else:
                    _span = span(str(value), _title=str(value))
                    _td = td(_span, _class="text-center p-2 border-0 truncate")
                _tr.add(_td)
            _tbody.add(_tr)
        return _tbody

    @property
    def pagination(self):
        total = span(len(self.data), data_table_target="total")
        desc = div(total, span(" results"), _class="text-gray-500")
        button_class = (
            "relative inline-flex items-center px-2 py-2 border border-gray-300"
            " bg-white text-gray-500 hover:bg-gray-50 focus:outline-none"
        )
        first_button = button(
            IconFirstPage().to_tag(),
            data_action="click->table#firstPage",
            _class=button_class + " rounded-l-md",
        )
        prev_button = button(
            IconPreviousPage().to_tag(),
            data_action="click->table#previousPage",
            _class=button_class,
        )
        next_button = button(
            IconNextPage().to_tag(), data_action="click->table#nextPage", _class=button_class
        )
        last_button = button(
            IconLastPage().to_tag(),
            data_action="click->table#lastPage",
            _class=button_class + " rounded-r-md",
        )
        buttons = nav(
            first_button,
            prev_button,
            next_button,
            last_button,
            _class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px",
        )
        _div = div(
            desc,
            buttons,
            _class="flex justify-between items-center sm:px-2 sm:py-2",
        )
        return _div


class Text(Partial):
    value: str

    def _to_tag(self):
        tag = div(
            raw(markdown(self.value, extensions=["fenced_code"])),
            _class="prose max-w-none",
        )
        return tag


class Tab(Partial):
    name: str
    body: Partial

    def _to_tag(self):
        return self.body._to_tag()


class TabContainer(Partial):
    tabs: List[Tab]
    # NEEDS TO BE CALCULATED SOMEHOW
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


# USER CODE
# tab_1 = Tab(name='apple', body=Table())
# tab_2 = Tab(name='orange', body=Table())
# tab_3 = Tab(name='banana', body=Hbox(values=[Button(name='add', color='green'),
#                                              Button(name='remove', color='red'),
#                                              Table()]))

# tab_container_1 = TabContainer(tabs=[tab1, tab2, tab3])

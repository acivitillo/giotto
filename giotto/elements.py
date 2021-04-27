from __future__ import annotations
from copy import deepcopy
from typing import Any, Dict, List, Literal, Optional

from dominate.tags import (
    _input,
    a,
    button,
    div,
    label,
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
)
from dominate.util import raw
from markdown import markdown

from .base import Partial
from .icons import (
    Icon,
    IconFirstPage,
    IconLastPage,
    IconNextPage,
    IconPreviousPage,
    IconSearch,
)


class Select(Partial):
    _class = (
        "border border-gray-300 text-gray-600 pl-5 bg-white"
        " hover:border-gray-400 focus:outline-none"
    )

    options: List[str]
    selected: str = ""

    def _to_tag(self):
        tag = select(_class=self._class)
        tag.add(option("", value=""))
        for text in self.options:
            option_ = option(text)
            if text == self.selected:
                option_.attributes["selected"] = "selected"
            tag.add(option_)
        return tag


class MultiSelect(Partial):
    _class = Select._class

    options: List[str]
    selected: List[str] = []

    def _to_tag(self):
        tag = select(_class=self._class, multiple="multiple")
        tag.add(option("", value=""))
        for text in self.options:
            option_ = option(text)
            if text in self.selected:
                option_.attributes["selected"] = "selected"
            tag.add(option_)
        return tag


class Input(Partial):
    _class = Select._class

    placeholder: str = ""
    value: str = ""
    type_: str = "text"

    def _to_tag(self):
        tag = _input(type=self.type_, _class=self._class, placeholder=self.placeholder)
        if self.value:
            tag.attributes["value"] = self.value
        return tag


class Row(Partial):
    _class = "flex flex-row items-center"

    contents: List[Partial]

    def _to_tag(self):
        tag = div(_class=self._class)
        for item in self.contents:
            tag.add(item.to_tag())
        return tag


class Column(Partial):
    _class = "flex flex-col"

    contents: List[Partial]

    def _to_tag(self):
        tag = div(_class=self._class)
        for item in self.contents:
            tag.add(item.to_tag())
        return tag


class Button(Partial):
    description: str = "Submit"
    icon: Optional[Icon]
    color: str = "blue"

    @property
    def _class(self) -> str:
        _class = (
            f"uppercase bg-{self.color}-400 px-5"
            f" items-center font-medium text-black max-w-max shadow-sm cursor-pointer"
            f" focus:bg-{self.color}-600 focus:outline-none focus:text-white"
            f" hover:shadow-lg hover:bg-{self.color}-600 hover:text-white"
        )
        return _class

    def _to_tag(self):
        tag = button(_class=self._class)
        if self.icon:
            tag.add(self.icon.to_tag())
        tag.add(span(self.description))
        return tag


class ClickableIcon(Partial):
    _class = "mr-2 transform hover:text-purple-500 hover:scale-110 cursor-pointer"

    icon: Icon

    def _to_tag(self):
        tag = div(_class=self._class)
        tag.add(self.icon.to_tag())
        return tag


class Table(Partial):
    data: List[Dict]
    max_rows: int = 1
    column_width: Dict = {}

    def _to_tag(self):
        tag = div(
            _class="shadow",
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
                " hover:border-gray-400 focus:outline-none appearance-none rounded-t"
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
            "relative inline-flex items-center px-2 py-1 border border-gray-200"
            " bg-white text-gray-500 hover:bg-gray-50 focus:outline-none"
        )
        first_button = button(
            IconFirstPage().to_tag(),
            data_action="click->table#firstPage",
            _class=button_class + " rounded-l",
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
            _class=button_class + " rounded-r",
        )
        buttons = nav(
            first_button,
            prev_button,
            next_button,
            last_button,
            _class="relative z-0 inline-flex shadow-sm -space-x-px",
        )
        _div = div(
            desc,
            buttons,
            _class="flex justify-between items-center px-2 py-2",
        )
        return _div


class Text(Partial):
    _class = "prose max-w-none"

    value: str
    render_format: Literal["markdown", "html"] = "markdown"

    def _to_tag(self):
        if self.render_format == "markdown":
            text = raw(markdown(self.value, extensions=["fenced_code"]))
        else:
            text = raw(self.value)
        tag = div(text, _class=self._class)
        return tag


class ConnectedDropdowns(Partial):
    data: Dict[str, Any]
    filters: Dict[str, Any] = {}

    def filter_data(self):
        data = deepcopy(self.data)
        if self.filters:
            from pandas import DataFrame

            df = DataFrame(data)

            for key in self.data.keys():
                data[key] = df.to_dict("list")[key]
                filter_value = self.filters.get(key)
                if filter_value:
                    values = [filter_value]
                    df = df.query(f"{key} in {values}")

        return data

    def _to_tag(self):
        return div(self._to_tags())

    def _to_tags(self):
        components = []
        data = self.filter_data()
        for name, values in data.items():
            options = sorted(list(set(values)))
            tag = Select(options=options, selected=self.filters.get(name, ""), name=name).to_tag()
            components.append(tag)
        return components
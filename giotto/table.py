# NOTE: I split and organized the code but it's still pretty hard to test

from __future__ import annotations
from typing import Any, Dict, List, Union

from dominate.tags import _input, button, div, html_tag, nav, span, table, tbody, td, th, thead, tr

from .base import Partial
from .icons import IconFirstPage, IconLastPage, IconNextPage, IconPreviousPage, IconSearch


class Filters:
    def __get__(self, obj: Any, objtype: Any = None) -> html_tag:
        tag = div(_class="relative inline-flex")
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
        icon = IconSearch().to_tag()
        tag.add(input_, icon)
        return tag


class Head:
    def __get__(self, obj: Table, objtype: Any = None) -> html_tag:
        thead_ = thead(_class="bg-primary text-white")
        if obj.columns:
            tr_ = tr(_class="bg-dark text-white")
            for column in obj.columns:
                span_ = span(column, _title=column)
                class_ = "whitespace-nowrap py-2 resize-x truncate min-w-2"
                width = obj.column_width.get(column)
                style = "" if not width else f"width: {width}"
                th_ = th(span_, _class=class_, _style=style)
                tr_.add(th_)
            thead_.add(tr_)
        return thead_


class Body:
    def __get__(self, obj: Table, objtype: Any = None) -> html_tag:
        tbody_ = tbody()
        for counter, row in enumerate(obj.data):
            bg = "" if counter % 2 == 0 else "bg-gray-50 "
            hidden = "" if counter < obj.max_rows else " hidden"
            tr_ = tr(
                _class=f"{bg}hover:bg-gray-200 border-b h-6 border-gray-200 truncate{hidden}",
                data_table_target="row",
            )
            for value in row.values():
                if isinstance(value, Partial):
                    td_ = td(value.to_tag(), _class="flex item-center justify-center p-2 border-0")
                else:
                    span_ = span(str(value), _title=str(value))
                    td_ = td(span_, _class="text-center p-2 border-0 truncate")
                tr_.add(td_)
            tbody_.add(tr_)
        return tbody_


class Pagination:
    def __get__(self, obj: Table, objtype: Any = None) -> html_tag:
        total = span(obj.total_rows, data_table_target="total")
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
            IconNextPage().to_tag(),
            data_action="click->table#nextPage",
            _class=button_class,
        )
        last_button = button(
            IconLastPage().to_tag(),
            data_action="click->table#lastPage",
            _class=button_class + " rounded-r",
        )
        class_ = "relative z-0 inline-flex shadow-sm -space-x-px"
        buttons = nav(first_button, prev_button, next_button, last_button, _class=class_)

        class_ = "flex justify-between items-center px-2 py-2"
        div_ = div(desc, buttons, _class=class_)
        return div_


class Table(Partial):
    data: List[Dict[str, Any]]
    max_rows: int = 1
    column_width: Dict[str, Union[int, str]] = {}

    _filters = Filters()
    _thead = Head()
    _tbody = Body()
    _pagination = Pagination()

    @property
    def columns(self) -> List[str]:
        return [] if not self.data else list(self.data[0].keys())

    @property
    def total_rows(self) -> int:
        return len(self.data)

    def _to_tag(self) -> html_tag:
        table_ = table(self._thead, self._tbody, _class="w-full table-fixed")
        div_table = div(table_, _class="overflow-x-auto")
        tag = div(
            self._filters,
            div_table,
            self._pagination,
            _class="shadow",
            data_controller="table",
            data_table_max_page_rows_value=self.max_rows,
        )
        return tag

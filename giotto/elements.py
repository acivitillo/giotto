from __future__ import annotations
from copy import deepcopy
from typing import Any, Dict, List, Literal, Optional

from dominate.tags import _input, button, div, option, select, span
from dominate.util import raw
from markdown import markdown

from .base import Partial
from .table import Table
from .icons import Icon


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

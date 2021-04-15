from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Dict, List, Optional

from dominate.tags import div, html_tag, label
from pydantic import BaseModel


class HXAction(BaseModel):
    url: Optional[str] = None
    get: Optional[str] = None
    trigger: Optional[str] = None
    target: Optional[str] = None
    confirm: Optional[str] = None
    swap: Optional[str] = None

    def to_dict(self) -> Dict[str, str]:
        kwargs = {
            "data-hx-get": self.get,
            "data-hx-post": self.url,
            "data-hx-trigger": self.trigger,
            "data-hx-target": self.target,
            "data-hx-confirm": self.confirm,
            "data-hx-swap": self.swap,
        }
        return {key: value for key, value in kwargs.items() if value is not None}


class Style(BaseModel):
    height: Optional[int] = None
    width: Optional[int] = None
    margin: Optional[int] = None
    rounded: bool = False
    custom: Optional[str] = None
    custom_remove: Optional[str] = None

    def apply(self, tag: html_tag):
        kwargs_1 = {
            "h": self.height,
            "w": self.width,
            "m": self.margin,
        }
        for key, value in kwargs_1.items():
            if value is not None:
                tag.attributes["class"] += f" {key}-{value}"
        kwargs_2 = {
            "rounded-sm": self.rounded,
        }
        for key, value in kwargs_2.items():
            if value:
                tag.attributes["class"] += f" {key}"

        if self.custom:
            if self.custom_remove:
                tag.attributes["class"] = tag.attributes["class"].replace(
                    self.custom_remove, self.custom
                )
            else:
                tag.attributes["class"] += f" {self.custom}"


class Partial(ABC, BaseModel):
    id_: Optional[str] = None
    name: Optional[str] = None
    action: Optional[HXAction] = None
    style: Optional[Style] = None
    label: Optional[str] = None

    def to_tag(self) -> html_tag:
        tag = self._to_tag()
        tag = self._update_tag(tag)
        return tag

    def to_tags(self) -> List[html_tag]:
        tags = []
        for tag in self._to_tags():
            tag = self._update_tag(tag)
            tags.append(tag)
        return tags

    @abstractmethod
    def _to_tag(self) -> html_tag:
        # abstract method, needs to be implemented in child
        pass

    def _to_tags(self) -> List[html_tag]:
        return [self._to_tag()]

    def _update_tag(self, tag: html_tag) -> html_tag:
        if self.id_:
            tag.attributes.update({"id": self.id_})
        if self.name:
            tag.attributes.update({"name": self.name})
        if self.action:
            tag.attributes.update(self.action.to_dict())
        if self.style:
            self.style.apply(tag)
        if self.label:
            tag = label(self.label, tag, _class="ml-2")
        return tag

    def render(self) -> str:
        return self.to_tag().render()

    def _repr_html_(self) -> str:
        return self.render()
        # return self.to_html_jj()

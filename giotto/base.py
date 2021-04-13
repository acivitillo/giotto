from typing import Any, Dict, Optional

from dominate.tags import div, label
from pydantic import BaseModel


class Action(BaseModel):
    url: Optional[str] = None
    get: Optional[str] = None
    trigger: Optional[str] = None
    target: Optional[str] = None
    confirm: Optional[str] = None
    swap: Optional[str] = None

    @property
    def hx_kwargs(self):
        kwargs = {
            "data-hx-get": self.get,
            "data-hx-post": self.url,
            "data-hx-trigger": self.trigger,
            "data-hx-target": self.target,
            "data-hx-confirm": self.confirm,
            "data-hx-swap": self.swap,
        }
        return {key: value for key, value in kwargs.items() if value is not None}


class Partial(BaseModel):
    id_: Optional[str] = None
    name: Optional[str] = None
    action: Optional[Action] = None
    label: str = ""

    @classmethod
    def from_api(cls, url):
        pass

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(**data)

    def _to_tag(self):
        # abstract method, needs to be implemented in child
        return div()

    def _to_tags(self):
        return [self._to_tag()]

    def to_tag(self):
        tag = self._to_tag()
        tag = self._update_tag(tag)
        return tag

    def to_tags(self):
        tags = []
        for tag in self._to_tags():
            tag = self._update_tag(tag)
            tags.append(tag)
        return tags

    def _update_tag(self, tag):
        if self.id_:
            tag.attributes.update({"id": self.id_})
        if self.name:
            tag.attributes.update({"name": self.name})
        if self.action:
            tag.attributes.update(self.action.hx_kwargs)
        if self.label:
            tag = label(self.label, tag, _class="ml-2")
        return tag

    def render(self):
        return self.to_tag().render()

    def _repr_html_(self):
        return self.render()
        # return self.to_html_jj()


class BaseView(BaseModel):
    data: Dict = {}
    url_prefix: str = ""

    def to_tag(self):
        return div()

    def to_html(self):
        return self.to_tag().render()
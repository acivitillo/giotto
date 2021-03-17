from typing import Any, Dict, Optional

from dominate.tags import div
from pydantic import BaseModel


class Action(BaseModel):
    url: Optional[str] = None
    trigger: Optional[str] = None
    target: Optional[str] = None
    confirm: Optional[str] = None

    @property
    def hx_kwargs(self):
        kwargs = {
            "data-hx-post": self.url,
            "data-hx-trigger": self.trigger,
            "data-hx-target": self.target,
            "data-hx-confirm": self.confirm,
            "data-hx-swap": "outerHTML",
        }
        return {key: value for key, value in kwargs.items() if value is not None}


class Partial(BaseModel):
    action: Optional[Action] = None

    @classmethod
    def from_api(cls, url):
        pass

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(**data)

    def _to_tag(self):
        # abstract method, needs to be implemented in child
        return div()

    def to_tag(self):
        tag = self._to_tag()
        if self.action:
            tag.attributes.update(self.action.hx_kwargs)
        return tag

    def render(self):
        return self.to_tag().render()

    def _repr_html_(self):
        return self.render()
        # return self.to_html_jj()

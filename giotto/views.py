from typing import Dict, Union

from dominate.tags import div, form, label

from .base import Action, BaseView, Partial
from .elements import Button, Input, Select, MultiSelect


class FiltersView(BaseView):
    data: Dict[str, Partial]
    id_: str = "test"

    def to_tag(self):
        f = form(
            action=self.url_prefix, method="post", _class="flex flex-row flex-wrap items-center"
        )
        for name, component in self.data.items():
            if isinstance(component, Input):
                action = {
                    "action": Action(
                        url=self.url_prefix,
                        target=f"#{self.id_}",
                        trigger="keyup changed delay:500ms",
                    )
                }
            elif isinstance(component, MultiSelect):
                action = {}
            else:
                action = {"action": Action(url=self.url_prefix, target=f"#{self.id_}")}
            new_component = component.__class__(**{**component.dict(), **action, "name": name})
            if isinstance(component, Button):
                d = div(new_component.to_tag())
            else:
                d = div(label(name.capitalize()), new_component.to_tag(), _class="items-center m-2")
            f.add(d)
        d = div(f, _id=self.id_)
        return d

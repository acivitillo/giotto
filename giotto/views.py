from typing import Dict, Union

from dominate.tags import div, form

from .base import Action, BaseView
from .elements import Button, Input, Select


class FiltersView(BaseView):
    data: Dict[str, Union[Select, Input]]
    id_: str = "test"

    def to_tag(self):
        f = form(action=self.url_prefix, method="post")
        for name, component in self.data.items():
            if isinstance(component, Input):
                action = Action(
                    url=self.url_prefix, target=f"#{self.id_}", trigger="keyup changed delay:500ms"
                )
            else:
                action = Action(url=self.url_prefix, target=f"#{self.id_}")
            component = component.__class__(**{**component.dict(), "action": action, "name": name})
            f.add(component.to_tag())

        # btn = Button(
        #     description="Clear",
        #     action=Action(url=f"{self.url_prefix}?refresh=true", target=f"#{self.id_}"),
        #     height=10,
        # )
        # f.add(btn.to_tag())
        d = div(f, _id=self.id_)
        return d

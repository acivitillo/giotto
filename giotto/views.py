from typing import Dict, Union, Any, Optional

from dominate.tags import div, form, label

from .base import Action, BaseView, Partial
from .elements import Button, Input, Select, MultiSelect
from pandas import DataFrame


class FiltersView(BaseView):
    data: Dict[str, Partial]
    id_: str = "test"

    def to_tag(self):
        f = form(
            action=self.url_prefix, method="post", _class="flex flex-row flex-wrap items-center"
        )
        for name, component in self.data.items():
            component.action = self._get_action(component)
            component.name = name
            f.add(component.to_tag())
        d = div(f, _id=self.id_)
        return d

    def _get_action(self, component: Partial) -> Union[None, Action]:
        if isinstance(component, Input):
            action = Action(
                url=self.url_prefix,
                target=f"#{self.id_}",
                trigger="keyup changed delay:500ms",
            )

        elif isinstance(component, MultiSelect):
            action = None
        else:
            action = Action(url=self.url_prefix, target=f"#{self.id_}")
        return action


class NewFiltersView(BaseView):
    data: Dict[str, Any]
    filters: Optional[Dict[str, Any]]
    id_: str = "test"

    def filter_data(self):
        if self.filters:
            df = DataFrame(self.data)
            for key, values in self.filters.items():
                if values:
                    values = [values] if isinstance(values, str) else list(values)
                    df = df.query(f"{key} in {values}")
            self.data = df.to_dict("list")

    @property
    def components(self):
        components = {}
        for name, values in self.data.items():
            print(list(set(values)))
            components[name] = Select(
                options=list(set(values)), selected=self.filters[name], label=name.capitalize()
            )
        return components

    @property
    def reset_button(self):
        from dominate.tags import button

        onclick_list = [
            f'document.forms["{self.id_}"]["{name}"].value=""' for name in self.data.keys()
        ]
        onclick = "; ".join(onclick_list)

        btn = Button(description="Reset", height=10, action=self._get_action(Button())).to_tag()
        btn.attributes["onclick"] = onclick
        return btn

    def to_tag(self):
        self.filter_data()
        f = form(
            _id=self.id_,
            action=self.url_prefix,
            method="post",
            _class="flex flex-row flex-wrap items-center",
        )
        for name, component in self.components.items():
            component.action = self._get_action(component)
            component.name = name
            f.add(component.to_tag())

        f.add(self.reset_button)
        # d = div(f, _id=self.id_)
        # return d
        return f

    def _get_action(self, component: Partial) -> Union[None, Action]:
        if isinstance(component, Input):
            action = Action(
                url=self.url_prefix,
                target=f"#{self.id_}",
                trigger="keyup changed delay:500ms",
            )

        elif isinstance(component, MultiSelect):
            action = None
        else:
            action = Action(url=self.url_prefix, target=f"#{self.id_}")
        return action
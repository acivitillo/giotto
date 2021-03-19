from typing import List

from dominate.tags import div
from pydantic import BaseModel

from giotto.base import Action, BaseView
from giotto.elements import Row, Row, Select


class SourceDropdown(BaseView):
    def to_tag(self):

        tag = Select(options=self.data)
        return tag


class Dropdown(BaseModel):
    options: List[str] = []
    selected: str = ""


class DropdownData(BaseModel):
    sources: Dropdown
    schemas: Dropdown = Dropdown()
    tables: Dropdown = Dropdown()


class DropdownView(BaseView):
    data: DropdownData

    def to_tag(self):
        tag = div(_id="source_dropdowns")
        sources = Select(
            **self.data.sources.dict(),
            name="source",
            action=Action(
                get=self.url_prefix,
                target="#source_dropdowns",
            ),
        )
        schemas = Select(
            **self.data.schemas.dict(),
            id_="schemas",
            name="schema",
            action=Action(
                get=(f"{self.url_prefix}?source={self.data.sources.selected}"),
                target="#source_dropdowns",
            ),
        )
        tables = Select(**self.data.tables.dict(), id_="tables", name="table")
        row = Row(contents=[sources, schemas, tables])
        tag.add(row.to_tag())
        return tag

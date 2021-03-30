import os

from dominate.tags import div
from fastapi import APIRouter, Form
from fastapi.responses import HTMLResponse

from giotto.elements import Text
from giotto.navigation import Sidebar
from giotto.templates import AppSite
from giotto.views import NewFiltersView

from .. import mockapis

domain = os.getenv("API_DOMAIN")

prefix = "/crosstab"
router = APIRouter(prefix=prefix)


@router.get("/", response_class=HTMLResponse)
def index():
    site = AppSite(
        title="ACOE",
        sidebar=Sidebar(
            items=mockapis.sidebar_items, selected={"lev1": "ACOE", "lev2": "Crosstab"}
        ),
    )
    dropdowns = generate_filters(source="", schema="", table="", column="")
    site.content = div(dropdowns)
    return site.to_html()


@router.post("/dropdowns", response_class=HTMLResponse, tags=["Crosstab"])
def select_table(
    source: str = Form(""),
    schema: str = Form(""),
    table: str = Form(""),
    column: str = Form(""),
):
    f = generate_filters(source=source, schema=schema, table=table, column=column)
    return f.render()


def get_data():
    return mockapis.sources


def generate_filters(**user_input):
    data = get_data()
    view = NewFiltersView(data=data, filters=user_input, url_prefix=f"{prefix}/dropdowns").to_tag()
    text = Text(value=f"input: {list(user_input.values())}").to_tag()
    return div(view, text)

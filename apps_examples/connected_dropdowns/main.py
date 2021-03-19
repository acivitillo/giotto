import os

from dominate.tags import div
from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from giotto.navigation import Sidebar
from giotto.templates import AppSite

from .. import mockapis
from .views import DropdownView

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
    sources = get_sources()
    dropdowns = DropdownView(
        data={"sources": {"options": sources}}, url_prefix=f"{prefix}/dropdowns"
    )
    site.content = div(dropdowns.to_tag())
    return site.to_html()


@router.get("/dropdowns", response_class=HTMLResponse, tags=["Crosstab"])
def select_table(source: str, schema: str = None):
    sources = get_sources()
    schemas = get_schemas(source=source)

    if not schema:
        data = {
            "sources": {"options": sources, "selected": source},
            "schemas": {"options": schemas},
        }
    else:
        tables = get_tables(source=source, schema=schema)
        data = {
            "sources": {"options": sources, "selected": source},
            "schemas": {"options": schemas, "selected": schema},
            "tables": {"options": tables},
        }
    view = DropdownView(data=data, url_prefix=f"{prefix}/dropdowns")
    return view.to_html()


def get_sources():
    return list(mockapis.sources.keys())


def get_schemas(source: str):
    return list(mockapis.sources.get(source, {}).keys())


def get_tables(source: str, schema: str):
    return mockapis.sources.get(source, {}).get(schema, [])
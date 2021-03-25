import os
from typing import List

from dominate.tags import div
from fastapi import APIRouter, Form
from fastapi.responses import HTMLResponse

from giotto.elements import Input, MultiSelect, Select, Button
from giotto.navigation import Sidebar
from giotto.templates import AppSite
from giotto.views import FiltersView

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
    dropdowns = generate_filters()
    site.content = div(dropdowns)
    return site.to_html()


def generate_filters(
    source: str = "",
    schema: str = "",
    table: str = "",
    message: str = "",
    dimensions: List[str] = [],
    measures: List[str] = [],
):
    sources = get_sources()
    schemas = [] if not source else get_schemas(source=source)
    tables = [] if not schemas else get_tables(source=source, schema=schema)
    all_columns = [] if not tables else get_columns(source=source, schema=schema, table=table)

    # Cleaning old cached arguments
    schema = schema if schema in schemas else ""
    table = table if table in tables else ""
    dimensions = dimensions if set(dimensions).issubset(set(all_columns)) else []
    measures = measures if set(measures).issubset(set(all_columns)) else []

    filters = {
        "source": Select(options=sources, selected=source),
        "schema": Select(options=schemas, selected=schema),
        "table": Select(options=tables, selected=table),
        "dimensions": MultiSelect(options=all_columns, selected=dimensions),
        "measures": MultiSelect(options=all_columns, selected=measures),
        "message": Input(placeholder="Add your message", value=message),
        "generate": Button(description="Submit"),
    }

    view = FiltersView(data=filters, url_prefix=f"{prefix}/dropdowns").to_tag()
    view.add(div(f"input: {source} {schema} {table} {dimensions} {measures} {message}"))
    if dimensions and measures:
        view.add(div("Hurray !!! I'm able to produce a table now :D"))
    return view


@router.post("/dropdowns", response_class=HTMLResponse, tags=["Crosstab"])
def select_table(
    source: str = Form(""),
    schema: str = Form(""),
    table: str = Form(""),
    message: str = Form(""),
    dimensions: List[str] = Form([]),
    measures: List[str] = Form([]),
):
    f = generate_filters(source, schema, table, message, dimensions, measures)
    return f.render()


def get_sources():
    return list(mockapis.sources.keys())


def get_schemas(source: str):
    return list(mockapis.sources.get(source, {}).keys())


def get_tables(source: str, schema: str):
    return list(mockapis.sources.get(source, {}).get(schema, {}).keys())


def get_columns(source: str, schema: str, table: str):
    return mockapis.sources.get(source, {}).get(schema, {}).get(table, [])

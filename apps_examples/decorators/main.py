from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from lib import App, Select

from dominate.tags import div, p, ul, li, button

app = FastAPI()
webapp = App(app=app)
webapp.register()


@webapp.input(
    frame_name="inp_cascading_selects",
    target="inp_cascading_selects",
    out_target="out_cascading_selects",
)
def inp_cascading_selects(dd_tables: str = "", dd_fruits: str = "", independents: str = ""):
    options = ["agrumi", "vegetables", "nuts"]
    fruits = []
    independent = ["movies", "books", "etc"]
    sel1 = Select.from_list("dd_tables", options)
    if dd_tables != "":
        fruits = {
            "agrumi": ["oranges", "lemons"],
            "vegetables": ["lettuce"],
            "nuts": ["walnuts", "whatever"],
        }
        fruits = fruits[dd_tables]
        sel1.selected = dd_tables
    sel1 = sel1.to_tag()
    sel2 = Select.from_list("dd_fruits", fruits)
    if dd_fruits != "":
        sel2.selected = dd_fruits
    sel2 = sel2.to_tag()
    sel3 = Select.from_list("independents", independent)
    if independents != "":
        sel3.selected = independents
    sel3 = sel3.to_tag()
    return [sel1, sel2, sel3]


@webapp.output(frame_name="out_cascading_selects")
def out_cascading_selects(dd_tables: str = "", dd_fruits: str = "", independents: str = ""):
    _ul = ul()
    _ul.add(li(p(f"You selected table: {dd_tables}")))
    _ul.add(li(p(f"You selected fruit: {dd_fruits}")))
    _ul.add(li(p(f"You selected independent: {independents}")))
    return [_ul]


@webapp.input(frame_name="addtwo", target="out_addtwo")
def dd_values():
    vals1 = [1, 2, 3]
    vals2 = [1, 2, 3]
    sel1 = Select.from_list("vals1", vals1).to_tag()
    sel2 = Select.from_list("vals2", vals2).to_tag()
    return [sel1, sel2]


@webapp.output(frame_name="out_addtwo")
def out_addtwo(vals1: int = 0, vals2: int = 0):
    s = int(vals1) + int(vals2)
    return [p(f"The sum of your selected values is {s}")]

from dominate.tags import li, p, ul
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from giotto.elements import Select, ConnectedDropdowns, Input, Text, Column
from giotto.navigation import Sidebar
from giotto.templates import App
import mockapis

app = FastAPI()
app.mount("/giotto-statics", StaticFiles(packages=["giotto"]))
webapp = App(
    app=app,
    sidebar=Sidebar(
        items=mockapis.sidebar_items,
        selected={"lev1": "ACOE", "lev2": "Scheduler"},
    ),
)
webapp.register()


@webapp.input(target="inp_cascading_selects", out_target="out_cascading_selects_1")
def inp_cascading_selects(table: str = "", fruit: str = "", city: str = "", independent: str = ""):
    data = {
        "table": ["agrumi", "agrumi", "vegetables", "nuts", "nuts"],
        "fruit": ["oranges", "lemons", "lettuce", "walnuts", "whatever"],
        "city": ["london", "london", "london", "krakow", "krakow"],
    }
    independents = ["movies", "books", "etc"]

    sel1 = ConnectedDropdowns(
        data=data, filters={"table": table, "fruit": fruit, "city": city}
    ).to_tag()
    sel3 = Select(name="independent", options=independents, selected=independent).to_tag()
    return [*sel1, sel3]


@webapp.input(out_target="out_cascading_selects_2", class_="flex flex-col m-4 border")
def out_cascading_selects_1(table: str = "", fruit: str = "", independent: str = ""):
    text = (
        f"You selected table: {table}<br>"
        f"You selected fruit: {fruit}<br>"
        f"You selected independent: {independent}"
    )
    text = Text(value=text).to_tag()
    inp = Input(placeholder="Add your comment", name="comment").to_tag()
    return [text, inp]


@webapp.output()
def out_cascading_selects_2(comment: str = ""):
    if comment:
        tag = p(f'Your comment: "{comment}" has been saved.')
    else:
        tag = p()
    return [tag]


@webapp.input(out_target="out_addtwo")
def inp_addtwo():
    vals1 = [1, 2, 3]
    vals2 = [1, 2, 3]
    sel1 = Select(name="x", options=vals1).to_tag()
    sel2 = Select(name="y", options=vals2).to_tag()
    return [sel1, sel2]


@webapp.output()
def out_addtwo(x: int = 0, y: int = 0):
    s = int(x) + int(y)
    return [p(f"The sum of your selected values is {s}")]


@webapp.output()
def hello():
    return [p("Hello :) This is a static frame!")]

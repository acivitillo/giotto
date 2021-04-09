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


@webapp.frame(autorefresh=True, target="out_cascading_selects_1", type_="form")
def inp_cascading_selects(table: str = "", fruit: str = "", city: str = "", independent: str = ""):
    data = {
        "table": ["agrumi", "agrumi", "vegetables", "nuts", "nuts"],
        "fruit": ["oranges", "lemons", "lettuce", "walnuts", "whatever"],
        "city": ["london", "london", "london", "krakow", "krakow"],
    }
    independents = ["movies", "books", "etc"]

    sel1 = ConnectedDropdowns(data=data, filters={"table": table, "fruit": fruit, "city": city})
    sel3 = Select(name="independent", options=independents, selected=independent)
    return [sel1, sel3]


@webapp.frame(target="out_cascading_selects_2", class_="flex flex-col m-4 border", type_="form")
def out_cascading_selects_1(table: str = "", fruit: str = "", independent: str = ""):
    text = (
        f"You selected table: {table}<br>"
        f"You selected fruit: {fruit}<br>"
        f"You selected independent: {independent}"
    )
    text = Text(value=text)
    inp = Input(placeholder="Add your comment", name="comment")
    return [text, inp]


@webapp.frame()
def out_cascading_selects_2(comment: str = ""):
    if comment:
        text = Text(value=f'Your comment: "{comment}" has been saved.')
    else:
        text = Text(value="")
    return [text]


@webapp.frame(target="out_addtwo", type_="form")
def inp_addtwo():
    vals1 = [1, 2, 3]
    vals2 = [1, 2, 3]
    sel1 = Select(name="x", options=vals1)
    sel2 = Select(name="y", options=vals2)
    return [sel1, sel2]


@webapp.frame()
def out_addtwo(x: int = 0, y: int = 0):
    s = int(x) + int(y)
    return [Text(value=f"The sum of your selected values is {s}")]


@webapp.frame()
def hello():
    return [Text(value="Hello :) This is a static frame!")]

from giotto.elements import ConnectedDropdowns, Input, Select, Text
from giotto.templates import App
from giotto.navigation import Sidebar

from . import mockapis


webapp = App(prefix="/frames", sidebar=Sidebar(items=mockapis.sidebar_items))


@webapp.frame(autorefresh=True, target="out_cascading_selects_1", type_="form")
def inp_cascading_selects(
    source: str = "", schema: str = "", table: str = "", column: str = "", independent: str = ""
):
    data = mockapis.sources
    independents = ["movies", "books", "etc"]

    sel1 = ConnectedDropdowns(
        data=data, filters={"source": source, "schema": schema, "table": table, "column": column}
    )
    sel3 = Select(name="independent", options=independents, selected=independent)
    return [sel1, sel3]


@webapp.frame(target="out_cascading_selects_2", class_="flex flex-col m-4 border", type_="form")
def out_cascading_selects_1(source: str = "", schema: str = "", independent: str = ""):
    text = (
        f"You selected source: {source}<br>"
        f"You selected schema: {schema}<br>"
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

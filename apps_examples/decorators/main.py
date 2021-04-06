from dominate.tags import li, p, ul
from fastapi import FastAPI
from lib import App, Select

app = FastAPI()
webapp = App(app=app)
webapp.register()


@webapp.input(target="inp_cascading_selects", out_target="out_cascading_selects")
def inp_cascading_selects(table: str = "", fruit: str = "", independent: str = ""):
    data = {
        "agrumi": ["oranges", "lemons"],
        "vegetables": ["lettuce"],
        "nuts": ["walnuts", "whatever"],
    }
    tables = list(data.keys())
    fruits = data.get(table, [])
    independents = ["movies", "books", "etc"]

    sel1 = Select.from_list("table", tables, table).to_tag()
    sel2 = Select.from_list("fruit", fruits, fruit).to_tag()
    sel3 = Select.from_list("independent", independents, independent).to_tag()
    return [sel1, sel2, sel3]


@webapp.output()
def out_cascading_selects(table: str = "", fruit: str = "", independent: str = ""):
    _ul = ul()
    _ul.add(li(p(f"You selected table: {table}")))
    _ul.add(li(p(f"You selected fruit: {fruit}")))
    _ul.add(li(p(f"You selected independent: {independent}")))
    return [_ul]


@webapp.input(out_target="out_addtwo")
def inp_addtwo():
    vals1 = [1, 2, 3]
    vals2 = [1, 2, 3]
    sel1 = Select.from_list("x", vals1).to_tag()
    sel2 = Select.from_list("y", vals2).to_tag()
    return [sel1, sel2]


@webapp.output()
def out_addtwo(x: int = 0, y: int = 0):
    s = int(x) + int(y)
    return [p(f"The sum of your selected values is {s}")]


@webapp.output()
def hello():
    return [p("Hello :) This is a static frame!")]

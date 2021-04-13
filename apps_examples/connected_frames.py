from giotto.elements import ConnectedDropdowns, Input, Select, Text, Button
from giotto.templates import App
from giotto.navigation import Sidebar

from . import mockapis


webapp = App(prefix="/frames", sidebar=Sidebar(items=mockapis.sidebar_items))

# FRAMES
# ------


@webapp.frame(autorefresh=True, type_="form")
def inp_cascading_selects(
    source: str = "", schema: str = "", table: str = "", column: str = "", independent: str = ""
):
    data = mockapis.sources
    independents = ["movies", "books", "etc"]

    sel1 = ConnectedDropdowns(
        data=data, filters={"source": source, "schema": schema, "table": table, "column": column}
    )
    sel3 = Select(name="independent", options=independents, selected=independent)
    btn = Button(description="Submit", action=webapp.get_action("out_cascading_selects_1"))
    return [sel1, sel3, btn]


@webapp.frame(class_="flex flex-col m-4 border", type_="form")
def out_cascading_selects_1(source: str = "", schema: str = "", independent: str = ""):
    text = (
        f"You selected source: {source}<br>"
        f"You selected schema: {schema}<br>"
        f"You selected independent: {independent}"
    )
    text = Text(value=text)
    inp = Input(placeholder="Add your comment", name="comment")
    btn = Button(
        description="Submit",
        action=webapp.get_action("out_cascading_selects_2", func_kwargs={"schema": schema}),
    )
    return [text, inp, btn]


@webapp.frame()
def out_cascading_selects_2(schema: str = "", comment: str = ""):
    if comment and schema:
        text = Text(value=f'Your comment: "{comment}" with schema "{schema}" has been saved.')
    else:
        text = Text(value="Please choose a schema and add comment first.")
    return [text]


@webapp.frame(type_="form")
def inp_addtwo():
    vals1 = [1, 2, 3]
    vals2 = [1, 2, 3]
    sel1 = Select(name="x", options=vals1)
    sel2 = Select(name="y", options=vals2)
    btn = Button(description="Submit", action=webapp.get_action("out_addtwo"))
    return [sel1, sel2, btn]


@webapp.frame()
def out_addtwo(x: int = 0, y: int = 0):
    s = int(x) + int(y)
    return [Text(value=f"The sum of your selected values is {s}")]


@webapp.frame()
def hello():
    return [Text(value="Hello :) This is a static frame!")]


@webapp.frame()
def buttons():
    job_name = "kasias_job"
    btn1 = Button(
        description="Run", action=webapp.get_action("run", func_kwargs={"job_name": job_name})
    )
    btn2 = Button(description="Delete", action=webapp.get_action("delete"))
    return [btn1, btn2]


@webapp.frame()
def notification(message: str = ""):
    return [Text(value=message)]


# ACTIONS
# -------


@webapp.action(target="notification")
def run(job_name: str):
    msg = f"Running {job_name}..."
    return webapp.frames["notification"].run(message=msg)


@webapp.action(target="notification")
def delete():
    msg = "Deleting job..."
    return webapp.frames["notification"].run(message=msg)
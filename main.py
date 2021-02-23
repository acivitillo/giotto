from typing import Any, List

from dominate import document as doc
from dominate.tags import body, div, h1, head, link, main, script
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from giotto.elements import Box, Button, Input, Select, Text
from giotto.navigation import Sidebar, TopBar
from giotto.templates import AppLayout, FrameTemplate
from giotto.utils import turbo_frame
import mockapis
from apps_examples.scheduler import SchedulerAppLayout

app = FastAPI()

btn1 = Button(description="Step 1", action="swap", name="start")
btn2 = Button(description="Step 2", action="swap", name="step2")
btn_back = Button(description="go back", action="reset")
sel_fruit = Select(options=["oranges"])
text = Text(
    value="Everything inside the border is a frame. Click the button to see how the frame works"
)
explain_frame = Box(contents=[text])
inp = Input()
inp2 = Input()

# Frame
class FiltersFrame(FrameTemplate):
    route = "/someurl"
    content: List[BaseModel] = [sel_fruit, inp, inp2, explain_frame]

    def to_html(self, name: str = "", route: str = ""):
        if route == "":
            route = self.route
        tag = turbo_frame(_id="frametest", src=route)
        if name == "start":
            el = Select(options=["Apples"]).to_tag()
            tag.add(el)
            text = Text(
                value=f"the button was clicked and the name is {name}."
                " Note how we can change everything, including"
                " the select on the left."
            ).to_tag()
            tag.add(text)
            return tag.render()
        elif name == "step2":
            text = Text(
                value="You see? Now we changed the frame again - only this text ;)"
            ).to_tag()
            tag.add(text)
            return tag.render()
        else:
            tag = turbo_frame(_id="frametest")
            for item in self.content:
                tag.add(item.to_tag())
            return tag.render()


# Page
class TestAppLayout(AppLayout):
    route = "/testapp"
    sidebar = Sidebar(items=mockapis.sidebar_items)
    content: List[BaseModel] = [FiltersFrame(), btn1, btn2, btn_back]


app.add_api_route(**TestAppLayout().to_register())
app.add_api_route(**FiltersFrame().to_register())
app.add_api_route(**SchedulerAppLayout().to_register())
app.mount("/assets/dist", StaticFiles(directory="assets/dist"), name="assets")
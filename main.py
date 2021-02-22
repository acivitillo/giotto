from fastapi import FastAPI

from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Any
from dominate.tags import head, body, script, link, div, h1, main
from dominate import document as doc
from giotto.elements import Select, Button, Input, Box
from giotto.navigation import TopBar, Sidebar
from giotto.utils import turbo_frame

from giotto.templates import FrameTemplate, AppLayout
import mockapis

app = FastAPI()

btn1 = Button(value="Step 1", action="swap", name="start")
btn2 = Button(value="Step 2", action="swap", name="step2")
btn_back = Button(value="go back", action="reset")
sel_fruit = Select(options=["oranges"])
explain_frame = Box(
    contents=[
        h1("Everything inside the border is a frame. Click the button to see how the frame works")
    ]
)
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
            tag.add(
                h1(
                    f"""the button was clicked and the name is {name}. 
                        Note how we can change everything, including
                        the select on the left.""",
                    _class="relative inline-flex",
                )
            )
            return tag.render()
        elif name == "step2":
            tag.add(h1("You see? Now we changed the frame again - only this text ;)"))
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
app.mount("/assets/dist", StaticFiles(directory="assets/dist"), name="assets")
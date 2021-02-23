from typing import List

from pydantic import BaseModel

from giotto.elements import Box, Input, Text
from giotto.navigation import Sidebar
from giotto.templates import AppLayout
import mockapis


title = Text(value="Scheduler App")
inp = Input(placeholder="Search Job...")
content = Box(contents=[title, inp])


# Page
class SchedulerAppLayout(AppLayout):
    route = "/scheduler"
    sidebar = Sidebar(items=mockapis.sidebar_items)
    content: List[BaseModel] = [content]
    site_name = "Scheduler App"
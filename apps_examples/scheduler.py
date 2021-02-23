from typing import List

from pydantic import BaseModel

from giotto.elements import Box, Input, Text, Table
from giotto.navigation import Sidebar
from giotto.templates import AppLayout
import mockapis


title = Text(value="Scheduler App")
inp = Input(placeholder="Search Job...")
table = Table(data=mockapis.jobs['data'])
content = Box(contents=[title, inp, table])



# Page
class SchedulerAppLayout(AppLayout):
    route = "/scheduler"
    sidebar = Sidebar(items=mockapis.sidebar_items)
    content: List[BaseModel] = [content]
    site_name = "Scheduler App"
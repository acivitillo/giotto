from typing import Any, Dict, List

from pydantic import BaseModel

from giotto.elements import Box, Input, Table, Text, Button
from giotto.navigation import Sidebar
from giotto.templates import AppLayout
from giotto.transformers import Transformer
from giotto.icons import IconSearch, IconDetails, IconStop, IconPlay
import mockapis

inp = Input(placeholder="Search Job...")
run_btn = Button(description="", color="green", icon=IconPlay(), action="swap", is_flex=True)
stop_btn = Button(description="", color="red", icon=IconStop(), action="swap", is_flex=True)


def transform_data(data: Dict):
    data = data["data"]

    def remove_first_and_last(x):
        return str(x)[1:-1]

    cols_for_strip = ["func_args", "crons", "upstream", "downstream", "func_kwargs"]
    formatter = {
        "created_at": lambda x: x[:10],
        **{k: remove_first_and_last for k in cols_for_strip},
    }
    new_data = []
    for row in data:
        new_row = dict()
        # new_row['action'] = Button(description)
        for key, value in row.items():
            new_key = key.replace("_", " ").title()
            new_row[new_key] = value
            if key in formatter:
                new_row[new_key] = formatter[key](value)
        new_data.append(new_row)
    return new_data


data = Transformer.from_dict(mockapis.jobs).apply(transform_data).data

table = Table(data=data, actions=[run_btn, stop_btn])
content = Box(contents=[inp, table])

# Page
class SchedulerAppLayout(AppLayout):
    route = "/scheduler"
    sidebar = Sidebar(items=mockapis.sidebar_items)
    content: List[BaseModel] = [content]
    site_name = "Scheduler App"

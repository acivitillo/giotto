from typing import Any, List

from dominate import document as doc
from dominate.tags import body, div, h1, head, link, main, script
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from giotto.elements import Box, Button, Input, Select, Text, Column
from giotto.navigation import Sidebar, TopBar
from giotto.utils import turbo_frame
import mockapis

app = FastAPI()

app.mount("/giotto-statics", StaticFiles(packages=["giotto"]))


from apps_examples.scheduler import router as example_scheduler

app.include_router(example_scheduler)
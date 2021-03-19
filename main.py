from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from giotto.templates import AppSite
from giotto.elements import Text, Box
from giotto.navigation import Sidebar

from apps_examples.scheduler.scheduler import router as example_scheduler
from apps_examples.ghpages import router as ghpages
from apps_examples.connected_dropdowns.main import router as connected_dropdowns
from apps_examples import mockapis

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
def index():
    site = AppSite(sidebar=Sidebar(items=mockapis.sidebar_items))
    text = "### Index page needs improvement, but sidebar links work ;)"
    site.content = Box(contents=[Text(value=text)], centered=True).to_tag()
    return site.to_html()


app.mount("/giotto-statics", StaticFiles(packages=["giotto"]))


app.include_router(example_scheduler)
app.include_router(ghpages)
app.include_router(connected_dropdowns)

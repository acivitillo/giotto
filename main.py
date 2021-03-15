from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from apps_examples.scheduler import router as example_scheduler

app = FastAPI()

app.mount("/giotto-statics", StaticFiles(packages=["giotto"]))


app.include_router(example_scheduler)

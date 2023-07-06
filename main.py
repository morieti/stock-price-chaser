import logging
from pathlib import Path

import app as application
import app.routers as base_routers

from fastapi import FastAPI, Depends

THIS_DIR = Path(__file__).parent

logging.basicConfig(level=logging.ERROR)

app = FastAPI(
    title="Stock Prices based on Dollar",
    description="""A Morieti Project""",
    version="1.0.0",
    docs_url="/swagger"
)

app.include_router(base_routers.router)

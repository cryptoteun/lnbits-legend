import asyncio

from fastapi import APIRouter, FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.routing import Mount

from lnbits.db import Database
from lnbits.helpers import template_renderer
from lnbits.tasks import catch_everything_and_restart

db = Database("ext_copilot")


copilot_static_files = [
    {
        "path": "/copilot/static",
        "app": StaticFiles(directory="lnbits/extensions/copilot/static"),
        "name": "copilot_static",
    }
]
copilot_ext: APIRouter = APIRouter(
    prefix="/copilot",
    tags=["copilot"]
    # "lnurlp", __name__, static_folder="static", template_folder="templates"
)


def copilot_renderer():
    return template_renderer(
        [
            "lnbits/extensions/copilot/templates",
        ]
    )


from .views_api import *  # noqa
from .views import *  # noqa
from .tasks import wait_for_paid_invoices
from .lnurl import *  # noqa


def copilot_start():
    loop = asyncio.get_event_loop()
    loop.create_task(catch_everything_and_restart(wait_for_paid_invoices))

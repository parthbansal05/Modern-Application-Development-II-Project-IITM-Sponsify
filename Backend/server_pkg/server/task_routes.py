from celery.result import AsyncResult
from flask import Blueprint
from flask import request

from . import tasks

bp = Blueprint("tasks", __name__, url_prefix="/tasks")


@bp.get("/result/<id>")
def result(id: str):
    print(id)
    result = AsyncResult(id)
    ready = result.ready()
    return {
        "ready": ready,
        "successful": result.successful() if ready else None,
        "value": result.get() if ready else result.result,
    }


@bp.get("/sponsor_export/<id>")
def sponsor_export(id: int):
    result = tasks.sponsor_export.delay(id)
    return {"result_id": result.id}
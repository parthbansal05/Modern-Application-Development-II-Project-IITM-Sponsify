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


@bp.post("/add")
def add():
    a = request.form.get("a", type=int)
    b = request.form.get("b", type=int)
    a=5
    b=7
    print(a, b)
    result = tasks.add.delay(a, b)
    return {"result_id": result.id}
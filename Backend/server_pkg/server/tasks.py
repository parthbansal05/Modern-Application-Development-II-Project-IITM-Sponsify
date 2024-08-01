import time
from celery import shared_task, Task

@shared_task(ignore_result=False)
def add(a: int, b: int) -> int:
    time.sleep(5)
    return a + b


# scheduled tasks
@shared_task
def daily_task():
    print("This task runs every day.")

@shared_task
def monthly_task():
    print("This task runs at the start of every month.")

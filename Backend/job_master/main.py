from fastapi import FastAPI
from celery import Celery
from celery.result import AsyncResult

app = FastAPI()
celery = Celery(
    "tasks",
    broker="redis://redis:6379/0",  # URL de conexión a Redis
    backend="redis://redis:6379/0"  # URL de conexión a Redis
)


@app.get("/job/{job_id}")
def get_job(job_id: str):
    result = AsyncResult(job_id, app=celery)
    if result.ready():
        return {"status": "completed", "result": result.result}
    else:
        return {"status": "pending"}


@app.post("/job")
def create_job(data: dict):
    result = celery.send_task("process_job", args=[data])
    # se crea y se retorna un job_id
    return {"job_id": result.id}


@app.get("/heartbeat")
def get_heartbeat():
    return {"status": "true"}

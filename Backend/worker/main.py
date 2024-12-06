import json
import requests
from celery import Celery
from hashlib import sha256

celery = Celery(
    "tasks",
    broker="redis://redis:6379/0",  # URL de conexión a Redis
    backend="redis://redis:6379/0"  # URL de conexión a Redis
)


@celery.task(name="process_job")
def process_job(challenges):
    result = {
        "deposit_token": challenges["deposit_token"],
        "challenges": []
    }

    for challenge in challenges["challenges"]:
        dt = challenges["deposit_token"]
        for secret in range(1, 500001):
            ci = challenge["challenge_id"]
            ch = challenge["challenge_hash"]
            test = sha256(
                f"deposit_token={dt}&challenge_id={ci}&secret={secret}".encode(
                    'utf-8')).hexdigest()
            if test == ch:
                result["challenges"].append({"challenge_id": ci, "secret": secret})
                break

    # guardar el resultado en el broker
    print(f"Json enviado a payments {json.dumps(result)}")
    answer = requests.post('https://api.legit.capital/v1/challenges/solution', data=json.dumps(result))
    print(answer.status_code)

    return "Job processed successfully"

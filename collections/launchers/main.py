from bottle import route, run
from psycopg import connect
from psycopg.rows import dict_row
from kafka import KafkaProducer
from os import getenv
from uuid import uuid4
from time import time


def load_tasks_to_run() -> list[dict[str,str]]:
    url = getenv('DBCONF_URL')
    result = list()
    with connect(url, row_factory=dict_row) as connection:
        with connection.cursor() as cursor:
            cursor.execute("select * from collections.dynamic_next_launch")
            row = cursor.fetchone()
            while row is not None:
                task_processor = row.get("processor")
                task_url = row.get("url")
                task_keywords = row.get("keywords")
                result.append({"task_processor": task_processor, "task_url": task_url, "task_keywords": task_keywords})
                # then, move to next element
                row = cursor.fetchone()
    return result 


@route('/launch')
def launch():
    tasks = load_tasks_to_run()
    size = len(tasks)
    bootstrap_url = getenv('MESSAGES_URL')
    producer = KafkaProducer(bootstrap_servers=bootstrap_url)
    for task in tasks:
        task_id = str(uuid4())
        topic = task["task_processor"]
        now = round(time() * 1000)
        producer.send(topic = topic, value='test',key=task_id,  timestamp_ms=now)
    return f"Should launch {size} tasks"


@route('/simulate')
def simulate():
    tasks = load_tasks_to_run()
    size = len(tasks)
    return f"SIMULATION: should launch {size} tasks"


if __name__ == '__main__':
    run(host='0.0.0.0', port=8080)

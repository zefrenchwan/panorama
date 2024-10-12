from os import getenv
from kafka import KafkaConsumer
from json import loads
import logging 
from db import upsert_task
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

logger = logging.getLogger(__name__)

topic_name = getenv('TOPIC_NAME')
# by definition
processor_name = topic_name
bootstrap_url = getenv('MESSAGES_URL')
consumer = KafkaConsumer(topic_name, bootstrap_servers=[bootstrap_url],value_deserializer=lambda message: loads(message.decode('utf-8')))


for message in consumer:
    task_id = message["taskId"]
    sources = message.get("sources")
    keywords = message.get("keywords")
    if sources is None:
        logger.error(f"no source provided for task {task_id}")
        # log failure, deal with retry 
        continue
    starting = datetime.datetime.now(datetime.timezone.utc)
    try:
        upsert_task(task_id, processor_name, starting, None, None)
    except Exception as e:
        logger.error(f"Error during processing of {task_id}")
        logger.error(e)
        
from os import getenv
from kafka import KafkaConsumer
from json import loads
import logging 

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

logger = logging.getLogger(__name__)

topic_name = getenv('TOPIC_NAME')
bootstrap_url = getenv('MESSAGES_URL')
consumer = KafkaConsumer(topic_name, bootstrap_servers=[bootstrap_url],value_deserializer=lambda message: loads(message.decode('utf-8')))


for message in consumer:
    logger.info(message)
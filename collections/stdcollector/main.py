from os import getenv
from kafka import KafkaConsumer

topic_name = getenv('TOPIC_NAME')
bootstrap_url = getenv('MESSAGES_URL')
consumer = KafkaConsumer(topic_name,
                         group_id='stdcollector',
                         bootstrap_servers=[bootstrap_url])

for message in consumer:
    print(message)
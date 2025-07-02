# data-pipeline/consumer.py

import os
import json
from kafka import KafkaConsumer
from dotenv import load_dotenv

load_dotenv()

KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:9092")
TOPIC = os.getenv("TOPIC_NAME", "polygon.stocks")

consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    auto_offset_reset='latest',
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    group_id="finance-consumers"
)

print(f"📡 Listening to topic: {TOPIC}")
for message in consumer:
    data = message.value
    print("✅ Received:", data)

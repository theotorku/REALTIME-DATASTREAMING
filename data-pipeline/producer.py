# data-pipeline/producer.py

import os
import json
import time
import random
from datetime import datetime
from kafka import KafkaProducer
from dotenv import load_dotenv

load_dotenv()

KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:9092")
TOPIC = os.getenv("TOPIC_NAME", "polygon.stocks")

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)


def simulate_trade():
    return {
        "ev": "T",               # event type = trade
        "sym": "AAPL",           # symbol
        "p": round(random.uniform(190, 210), 2),   # price
        "s": random.randint(10, 1000),             # size (shares)
        "t": int(datetime.utcnow().timestamp() * 1000),  # timestamp (ms)
    }


print(f"📡 Simulating AAPL trades to Kafka topic: {TOPIC}")

try:
    while True:
        trade = simulate_trade()
        producer.send(TOPIC, value=trade)
        print("📤 Sent:", trade)
        time.sleep(1)  # simulate 1-second trade interval
except KeyboardInterrupt:
    print("🛑 Simulation stopped.")

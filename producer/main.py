from producer.extract import connect_to_api, extract_json
from producer.producer_setup import kafka_producer, topic
import time

def main():
    producer = kafka_producer()

    while True:
        response = connect_to_api(symbol="IBM")
        data = extract_json(response, symbol="IBM")

        for stock in data:
            producer.send(topic, stock)

        producer.flush()

        print(f"Sent {len(data)} messages to {topic}")
        time.sleep(75)

if __name__ == "__main__":
    main()
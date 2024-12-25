# from kafka import KafkaConsumer
# import json


# def consume_messages():
#     print(20 * "___")

#     consumer = KafkaConsumer(
#         "message_topic",  # Kafka topic to consume messages from
#         bootstrap_servers="localhost:9092",  # Kafka broker
#         group_id="message_group",  # Consumer group ID
#         value_deserializer=lambda m: json.loads(m.decode("utf-8")),
#     )
#     for message in consumer:
#         print(f"Received message: {message.value}")
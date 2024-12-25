# from kafka import KafkaProducer
# import json

# # Initialize Kafka producer
# producer = KafkaProducer(
#     bootstrap_servers=["localhost:9092"],
#     value_serializer=lambda v: json.dumps(v).encode("utf-8"),
# )


# # Function to send message to Kafka
# def send_message_to_kafka(message):
#     producer.send("message_topic", message)
#     producer.flush()

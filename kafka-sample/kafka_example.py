from kafka import KafkaProducer, KafkaConsumer
from kafka.admin import KafkaAdminClient, NewTopic

# Kafka broker address
bootstrap_servers = ['localhost:9092']


# Create a topic
def create_topic(topic_name):
    admin_client = KafkaAdminClient(bootstrap_servers=bootstrap_servers)
    topic = NewTopic(name=topic_name, num_partitions=1, replication_factor=1)
    admin_client.create_topics([topic])
    print(f"Topic '{topic_name}' created successfully")


# Send a message to a topic
def send_message(topic_name, message):
    producer = KafkaProducer(bootstrap_servers=bootstrap_servers)
    producer.send(topic_name, message.encode('utf-8'))
    producer.flush()
    print(f"Message sent to topic '{topic_name}': {message}")


# Read messages from a topic
def read_messages(topic_name):
    consumer = KafkaConsumer(topic_name, bootstrap_servers=bootstrap_servers, auto_offset_reset='earliest')
    print(f"Reading messages from topic '{topic_name}':")
    for message in consumer:
        print(f"Received: {message.value.decode('utf-8')}")


if __name__ == "__main__":
    topic_name = "my-topic"

    # Create a topic
    create_topic(topic_name)

    # Send messages
    send_message(topic_name, "Hello, Kafka!")
    send_message(topic_name, "This is a test message")

    # Read messages
    read_messages(topic_name)

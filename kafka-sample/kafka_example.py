from kafka import KafkaProducer, KafkaConsumer
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError, UnknownTopicOrPartitionError

# Kafka broker address
bootstrap_servers = ['localhost:9092']


# Create a topic
def create_topic(topic_name, num_partitions=1, replication_factor=1):
    admin_client = KafkaAdminClient(bootstrap_servers=bootstrap_servers)
    topic = NewTopic(name=topic_name, num_partitions=num_partitions, replication_factor=replication_factor)
    try:
        admin_client.create_topics([topic])
        print(f"Topic '{topic_name}' created successfully")
    except TopicAlreadyExistsError:
        print(f"Topic '{topic_name}' already exists")


# List all topics
def list_topics():
    admin_client = KafkaAdminClient(bootstrap_servers=bootstrap_servers)
    topics = admin_client.list_topics()
    print("Existing topics:")
    for topic in topics:
        print(f"- {topic}")
    return topics


# Send a message to a topic
def send_message(topic_name, message):
    producer = KafkaProducer(bootstrap_servers=bootstrap_servers)
    producer.send(topic_name, message.encode('utf-8'))
    producer.flush()
    print(f"Message sent to topic '{topic_name}': {message}")


# Read messages from a topic
def read_messages(topic_name, timeout_ms=10000):
    consumer = KafkaConsumer(
        topic_name,
        bootstrap_servers=bootstrap_servers,
        auto_offset_reset='earliest',
        consumer_timeout_ms=timeout_ms
    )
    print(f"Reading messages from topic '{topic_name}':")
    for message in consumer:
        print(f"Received: {message.value.decode('utf-8')}")
    print("No more messages to read")


# Delete a topic
def delete_topic(topic_name):
    admin_client = KafkaAdminClient(bootstrap_servers=bootstrap_servers)
    try:
        admin_client.delete_topics([topic_name])
        print(f"Topic '{topic_name}' deleted successfully")
    except UnknownTopicOrPartitionError:
        print(f"Topic '{topic_name}' does not exist")


if __name__ == "__main__":
    topic_name = "my-topic"

    # List existing topics
    print("Initial topic list:")
    list_topics()

    # Create a topic
    create_topic(topic_name)

    # List topics again to confirm creation
    print("\nAfter creating new topic:")
    list_topics()

    # Send messages
    send_message(topic_name, "Hello, Kafka!")
    send_message(topic_name, "This is a test message")

    # Read messages
    read_messages(topic_name)

    # Delete the topic
    delete_topic(topic_name)

    # List topics one last time to confirm deletion
    print("\nAfter deleting the topic:")
    list_topics()

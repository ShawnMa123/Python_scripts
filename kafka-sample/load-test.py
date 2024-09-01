import time
import threading
from concurrent.futures import ThreadPoolExecutor
from kafka import KafkaProducer, KafkaAdminClient
from kafka.admin import NewTopic
from kafka.errors import TopicAlreadyExistsError

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


# Send messages for load testing
def send_messages(producer, topic_name, num_messages, message_size):
    message = b'X' * message_size
    for _ in range(num_messages):
        producer.send(topic_name, message)
    producer.flush()


# Load test function
def load_test(topic_name, num_messages, message_size, num_threads):
    producer = KafkaProducer(bootstrap_servers=bootstrap_servers,
                             batch_size=65536,
                             linger_ms=1,
                             acks=0)

    messages_per_thread = num_messages // num_threads
    start_time = time.time()

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(send_messages, producer, topic_name, messages_per_thread, message_size)
                   for _ in range(num_threads)]

        for future in futures:
            future.result()

    end_time = time.time()
    duration = end_time - start_time
    messages_per_second = num_messages / duration
    mb_per_second = (num_messages * message_size) / (1024 * 1024 * duration)

    print(f"Sent {num_messages} messages in {duration:.2f} seconds")
    print(f"Throughput: {messages_per_second:.2f} messages/second")
    print(f"Throughput: {mb_per_second:.2f} MB/second")


if __name__ == "__main__":
    topic_name = "load-test-topic"
    num_messages = 1_000_000  # Total number of messages to send
    message_size = 100  # Size of each message in bytes
    num_threads = 10  # Number of threads to use

    # Create the topic
    create_topic(topic_name, num_partitions=8, replication_factor=1)

    # Run the load test
    load_test(topic_name, num_messages, message_size, num_threads)

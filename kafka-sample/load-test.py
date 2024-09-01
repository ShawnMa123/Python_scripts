import time
import threading
from concurrent.futures import ThreadPoolExecutor
from kafka import KafkaProducer, KafkaConsumer, KafkaAdminClient
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


# Load test function (Producer)
def load_test_produce(topic_name, num_messages, message_size, num_threads):
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


# Consumer function
def consume_messages(topic_name, group_id, consumer_id, stop_event):
    consumer = KafkaConsumer(
        topic_name,
        bootstrap_servers=bootstrap_servers,
        group_id=group_id,
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        max_poll_records=500
    )

    message_count = 0
    start_time = time.time()

    while not stop_event.is_set():
        messages = consumer.poll(timeout_ms=100)
        for _, records in messages.items():
            message_count += len(records)

    duration = time.time() - start_time
    print(f"Consumer {consumer_id} in group {group_id} consumed {message_count} messages in {duration:.2f} seconds")
    consumer.close()
    return message_count, duration


# Load test function (Consumer)
def load_test_consume(topic_name, group_id, num_consumers, duration_seconds):
    stop_event = threading.Event()
    with ThreadPoolExecutor(max_workers=num_consumers) as executor:
        futures = [executor.submit(consume_messages, topic_name, group_id, i, stop_event)
                   for i in range(num_consumers)]

        time.sleep(duration_seconds)
        stop_event.set()

        total_messages = 0
        total_duration = 0
        for future in futures:
            messages, duration = future.result()
            total_messages += messages
            total_duration += duration

    avg_duration = total_duration / num_consumers
    messages_per_second = total_messages / avg_duration
    print(f"\nConsumer group {group_id} stats:")
    print(f"Total messages consumed: {total_messages}")
    print(f"Average throughput: {messages_per_second:.2f} messages/second")


if __name__ == "__main__":
    topic_name = "load-test-topic"
    num_messages = 1_000_000  # Total number of messages to send
    message_size = 100  # Size of each message in bytes
    num_producer_threads = 10  # Number of producer threads
    num_partitions = 8  # Number of partitions for the topic

    # Consumer group settings
    group_id = "test-consumer-group"
    num_consumers = 4  # Number of consumers in the group
    consume_duration = 60  # Duration to run consumers (in seconds)

    # Create the topic
    create_topic(topic_name, num_partitions=num_partitions, replication_factor=1)

    # Run the producer load test
    print("Starting producer load test...")
    load_test_produce(topic_name, num_messages, message_size, num_producer_threads)

    # Run the consumer load test
    print("\nStarting consumer load test...")
    load_test_consume(topic_name, group_id, num_consumers, consume_duration)

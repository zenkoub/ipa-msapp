import os
import pika
from dotenv import load_dotenv

load_dotenv()

def produce(host, body):

    rabbitmq_user = os.getenv("RABBITMQ_DEFAULT_USER")
    rabbitmq_pass = os.getenv("RABBITMQ_DEFAULT_PASS")

    credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_pass)
    parameters = pika.ConnectionParameters(host, credentials=credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    channel.exchange_declare(exchange="jobs", exchange_type="direct")
    channel.queue_declare(queue="router_jobs")
    channel.queue_bind(
        queue="router_jobs", exchange="jobs", routing_key="check_interfaces"
    )

    channel.basic_publish(exchange="jobs", routing_key="check_interfaces", body=body)
    print(f" [x] Sent: {body}")

    connection.close()

if __name__ == "__main__":
    produce("localhost", "192.168.1.44")

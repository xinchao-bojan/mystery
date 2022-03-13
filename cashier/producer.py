import pika

credentials = pika.PlainCredentials('rabbitmq', 'rabbitmq')
params = pika.ConnectionParameters('rabbitmq', 5672, '/', credentials)
connection = pika.BlockingConnection(params)
channel = connection.channel()


def publish(key, body):
    channel.basic_publish(exchange='', routing_key=key, body=body)

import pika

credentials = pika.PlainCredentials('rabbitmq', 'rabbitmq')
params = pika.ConnectionParameters('rabbitmq', 5672, '/', credentials)
connection = pika.BlockingConnection(params)
channel = connection.channel()


def publish(key, method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key=key, body=body, properties=properties)

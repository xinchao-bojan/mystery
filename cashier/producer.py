import pika

credentials = pika.PlainCredentials('rabbitmq', 'rabbitmq')
params = pika.ConnectionParameters('rabbitmq', 5672, '/', credentials)


def publish(key, body):
    try:
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        channel.basic_publish(exchange='', routing_key=key, body=body)
    except:
        print('error')
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        channel.basic_publish(exchange='', routing_key=key, body=body)

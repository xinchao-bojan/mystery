import pika, os, django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'riddle_tree.settings')
django.setup()
from main_app.models import CustomUser

credentials = pika.PlainCredentials('rabbitmq', 'rabbitmq')
params = pika.ConnectionParameters('rabbitmq', 5672, '/', credentials)
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='get_promocode')
channel.queue_declare(queue='post_promocode')


def get_callback(channel, method, properties, body):
    print('get_callback')


def post_callback(channel, method, properties, body):
    print('post_callback')


channel.basic_consume(queue='get_promocode', on_message_callback=get_callback, auto_ack=True)
channel.basic_consume(queue='post_promocode', on_message_callback=post_callback, auto_ack=True)

print('Started consuming')

channel.start_consuming()
channel.close()

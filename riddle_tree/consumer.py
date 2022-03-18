import pika, os, django, json, qrcode
from io import BytesIO
from django.core.files.images import ImageFile

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'riddle_tree.settings')
django.setup()
from main_app.models import Promocode


def generate_qr(channel, method, properties, body):
    data = json.loads(body)
    promocode = Promocode.objects.filter(active=True, text=data.get('promocode'))
    if promocode:
        promocode = promocode.last()
        service_url = f'https://vk.com/rtuitlab?promocode={promocode.text}&slug={promocode.sale.slug}'

        buf = BytesIO()
        qr = qrcode.QRCode()
        qr.add_data(service_url)
        qr.make()
        img_qr = qr.make_image()
        img_qr.save(buf, format='PNG')

        promocode.qr = ImageFile(buf, name=f'{promocode.user.email}.jpg')
        promocode.active = False
        promocode.save()
    return promocode


def main():
    credentials = pika.PlainCredentials('rabbitmq', 'rabbitmq')
    params = pika.ConnectionParameters('rabbitmq', 5672, '/', credentials)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.queue_declare(queue='generate_qr')

    channel.basic_consume(queue='generate_qr', on_message_callback=generate_qr, auto_ack=True)

    print('Started consuming')

    channel.start_consuming()
    channel.close()


if __name__ == '__main__':
    while True:
        try:
            main()
            break
        except:
            pass

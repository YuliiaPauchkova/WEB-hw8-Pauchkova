import pika
from time import sleep
from mongoengine import connect
from models import Contact

connect(
    db='database',
    host='mongodb+srv://new1:2312@database.9kdee0f.mongodb.net/',
)

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='email_queue')

def send_email(contact_id):
    contact = Contact.objects.get(id=contact_id)
    print(f"Sending email to {contact.name} at {contact.email}")
    contact.email_sent = True
    contact.save()

def callback(ch, method, properties, body):
    print(f"Received message: {body}")
    send_email(body.decode())
    print("Email sent successfully")
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='email_queue', on_message_callback=callback)

print('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()

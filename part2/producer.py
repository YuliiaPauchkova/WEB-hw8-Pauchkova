import pika
from faker import Faker
from mongoengine import connect
from models import Contact

fake = Faker()

connect(
    db='database',
    host='mongodb+srv://new1:2312@database.9kdee0f.mongodb.net/',
)
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='email_queue')

for _ in range(10): 
    name = fake.name()
    email = fake.email()
    contact = Contact(name=name, email=email)
    contact.save()
    channel.basic_publish(exchange='', routing_key='email_queue', body=str(contact.id))
    print(f"Contact {name} added to the queue")

connection.close()

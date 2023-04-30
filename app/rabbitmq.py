import pika
import os
import json

'''
    function for publishing message to rabbitmq
'''


def publish(cmd):
    # Set up connection parameters
    credentials = pika.PlainCredentials('guest', 'guest')
    parameters = pika.ConnectionParameters('rabbitmq1', 5672, '/', credentials)

    # Connect to RabbitMQ server
    connection = pika.BlockingConnection(parameters)

    # Create a channel
    channel = connection.channel()

    # Declare a queue
    channel.queue_declare(queue='backup-data')

    # Publish a message
    channel.basic_publish(
        exchange='', routing_key='backup-data', body=json.dumps(cmd))

    # Close the connection
    connection.close()
    print(" ___ Sent: %s" % cmd)


'''
    function for creating queue in rabbitmq server
'''


def create_queue():
    # Set up connection parameters
    credentials = pika.PlainCredentials('guest', 'guest')
    parameters = pika.ConnectionParameters('rabbitmq1', 5672, '/', credentials)

    # Connect to RabbitMQ server
    connection = pika.BlockingConnection(parameters)

    # Create a channel
    channel = connection.channel()

    # Declare a queue
    channel.queue_declare(queue='backup-data')

    # Close the connection
    connection.close()

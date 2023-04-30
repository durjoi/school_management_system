import pika
import pymongo
import json

# Database connection
client = pymongo.MongoClient("mongodb://admin:password@mongodb2:8012/smsystem")
db = client["smsystem"]

# RabbitMQ connection
credentials = pika.PlainCredentials('guest', 'guest')
parameters = pika.ConnectionParameters('rabbitmq2', 5672, '/', credentials)

connection = pika.BlockingConnection(parameters)
channel = connection.channel()

channel.queue_declare(queue='backup-data', durable=False)

'''
    function for consuming message from rabbitmq
'''


def callback(ch, method, properties, body):
    print("Received message:", body.decode())

    data = json.loads(body.decode())

    print(data)

    if (data['type'] == "user"):
        if (data['action'] == "create"):
            db.users.insert_one(data['data'])
        elif (data['action'] == "update"):
            db.users.update_one({"_id": data['data']['_id']}, {
                                "$set": data['data']})
    elif (data['type'] == "subject"):
        if (data['action'] == "create"):
            db.subjects.insert_one(data['data'])
        elif (data['action'] == "update"):
            db.subjects.update_one({"_id": data['data']['_id']}, {
                                   "$set": data['data']})
    elif (data['type'] == "class"):
        if (data['action'] == "create"):
            db.classes.insert_one(data['data'])
        elif (data['action'] == "update"):
            db.classes.update_one({"_id": data['data']['_id']}, {
                                  "$set": data['data']})
            # delete from marks table where class id is the current class id and subject id is not in the subjects list
            db.marks.delete_many(
                {"class_id": data['data']['_id'], "subject_id": {"$nin": data['data']['subjects']}})
            # update class name on students table
            db.students.update_many({"class._id": data['data']['_id']}, {
                "$set": {"class.name": data['data']['name']}})
    elif (data['type'] == "student"):
        if (data['action'] == "create"):
            db.students.insert_one(data['data'])
        elif (data['action'] == "update"):
            student = db.students.find_one({"_id": data['data']['_id']})
            if (student['class']['_id'] != data['data']['class']['_id']):
                db.marks.delete_many(
                    {"student._id": data['data']['_id']})
            db.students.update_one({"_id": data['data']['_id']}, {
                                   "$set": data['data']})
    elif (data['type'] == "marks"):
        if (data['action'] == "create"):
            db.marks.insert_one(data['data'])

    db.message.insert_one({"message": data})


channel.basic_consume(
    queue='backup-data', on_message_callback=callback, auto_ack=True)

print('Listening to queue "test". Press Ctrl+C to stop.')
channel.start_consuming()

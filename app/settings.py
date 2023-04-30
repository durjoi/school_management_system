import pymongo

# Database
client = pymongo.MongoClient("mongodb://admin:password@mongodb1:8011/smsystem")
db = client["smsystem"]

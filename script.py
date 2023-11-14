from settings import *
from mongo_config import weather_data_collection
from mongo_config import pollution_data_collection

def insert_to_mongo():
  print("inserting into mongo")
  weather_data_collection.insert_one({'weather2':'cold'})
  print("done inserting!!!")

insert_to_mongo()
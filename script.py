from settings import *
from mongo_config import weather_data_collection, pollution_data_collection
from timeloop import Timeloop
from datetime import timedelta
import requests
import json

tl = Timeloop()

def get_weather_data():
	""" get weather data from climacell """
	url = "https://api.tomorrow.io/v4/weather/realtime?location=beijing&units=metric&apikey=67t7rBMPnWRiBvP4raM1091eUdSNtDDJ"
	headers = {"accept": "application/json"}
	response = requests.get(url, headers=headers)
	return response.json()
	#url = "https://api.climacell.co/v3/weather/realtime"
	#querystring = {"lat":"39.9042","lon":"116.4074","unit_system":"us","fields":"precipitation,wind_gust,humidity,wind_direction,precipitation_type,visibility,cloud_cover,cloud_base,cloud_ceiling,weather_code,feels_like,temp","apikey":CLIMACELL_API_KEY}
	#weather_response = requests.request("GET", url, params=querystring)
	#return weather_response.json()

# def get_air_pollution_data():
# 	""" get air quality data from climacell """
# 	url = "https://api.climacell.co/v3/weather/realtime"
# 	#querystring = {"lat":"39.9042","lon":"116.4074","unit_system":"us","fields":"o3,so2,co,no2,pm10,pm25","apikey":CLIMACELL_API_KEY}
# 	air_pollution_response = requests.request("GET", url, params=querystring)
# 	return air_pollution_response.json()

@tl.job(interval=timedelta(seconds=5))
def sample_job_every_120s():
	weather_response = get_weather_data()
	#air_pollution_data = get_air_pollution_data()
	insert_to_mongo(weather_response)
	#insert_to_mongo(weather_response, air_pollution_data))

def insert_to_mongo(weather_data):
#def insert_to_mongo(weather_data, air_pollution_data):
	""" insert weather data and traffic data to the proper collections """
	weather_data_collection.insert_one(weather_data)
	#pollution_data_collection.insert_one(air_pollution_data)

def main():
	sample_job_every_120s()

if __name__ == "__main__":
	tl.start(block=True)
	main()
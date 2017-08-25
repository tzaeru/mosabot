import pyowm
from concurrent.futures import ThreadPoolExecutor
import asyncio
import datetime
import config

"""owm = pyowm.OWM(config.owm_key)  # You MUST provide a valid API key
	obs = owm.weather_at_place(location)
	w = obs.get_weather()

	# Meta
	formatted += "Time: " + w.get_reference_time(timeformat='iso') + "\n"
	formatted += "City: " + obs.get_location().get_name() + "\n\n"

	# Weather
	formatted += "0h" + " - wind: " + str(w.get_wind()["speed"]) + " - humidity: " + str(w.get_humidity()) + " - temperature: " + str(w.get_temperature(unit='celsius')["temp"])

"""

from apixu.client import ApixuClient, ApixuException
api_key = config.apixu_key
client = ApixuClient(api_key)

def parse_weather_data(weather):
	parsed = ""
	if "time" in weather:
		parsed += " (" + str(weather["time"]) + ")"
	parsed += " - Condition: " + str(weather["condition"]["text"])
	parsed += " - Wind: " + str(weather["wind_kph"]) + "kmh"
	parsed += " - Humidity: " + str(weather["humidity"]) + "%"
	parsed += " - Clouds: " + str(weather["cloud"]) + "%"
	parsed += " - Precipitation: " + str(weather["precip_mm"]) + "mm"
	parsed += " - Temperature: " + str(weather["temp_c"]) + "C"
	parsed += " - Feels like: " + str(weather["feelslike_c"]) + "C"
	return parsed

def get_weather(location):
	formatted = ""

	current = client.getForecastWeather(q=location, days=2)
	
	# Meta
	formatted += current["location"]["country"] + " - " + current["location"]["region"] + " - " + current["location"]["name"] + " - " + current["current"]["last_updated"] + "\n\n"
	# Now
	# Real now
	formatted += "**Now:** " + " (" + str(current["current"]["last_updated"]) + ")" + parse_weather_data(current["current"]) + "\n\n"
	# Fake now
	#formatted += "Now: " + parse_weather_data(current['forecast']['forecastday'][0]['hour'][datetime.datetime.now().hour]) + '\n'

	day = 0
	hour = datetime.datetime.now().hour + 3
	if hour > 23:
		day = 1
		hour = 0 + hour - 24
	formatted += "**3h:** " + parse_weather_data(current['forecast']['forecastday'][day]['hour'][hour]) + '\n'

	hour = datetime.datetime.now().hour + 6
	if hour > 23:
		day = 1
		hour = 0 + hour - 24
	formatted += "**6h:** " + parse_weather_data(current['forecast']['forecastday'][day]['hour'][hour]) + '\n'

	hour = datetime.datetime.now().hour + 12
	if hour > 23:
		day = 1
		hour = 0 + hour - 24
	formatted += "**12h:** " + parse_weather_data(current['forecast']['forecastday'][day]['hour'][hour]) + '\n'

	hour = datetime.datetime.now().hour + 24
	if hour > 23:
		day = 1
		hour = 0 + hour - 24
	formatted += "**24h:** " + parse_weather_data(current['forecast']['forecastday'][day]['hour'][hour]) + '\n'

	icon = current["current"]["condition"]["icon"]

	return (formatted, icon)
# -*- coding: utf-8 -*-
'''
pip install weather-api
'''
from weather import Weather, Unit
import translator
weather = Weather(unit=Unit.CELSIUS)
'''
w = Weather(Unit.CELSIUS)
lookup = w.lookup_by_latlng(53.3494,-6.2601)
condition = lookup.condition
print(condition.text)
'''
location = weather.lookup_by_location('หนองคาย')
forecasts = location.forecast
def get_now_day():
	text="พยากรณ์อากาศวันนี้ \n"+"สภาพอากาศ : "+translator.translator_to_thai(forecasts[0].text)+"\nมีอุณหภูมิสูงสุด : "+forecasts[0].high+" C\nและมีอุณหภูมิต่ำสุด : "+forecasts[0].low+" C"
	return text
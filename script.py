# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 08:55:16 2024

@author: Nilay Patel
"""
from sinch import SinchClient
from pyowm import OWM
from pyowm.utils import timestamps
from datetime import datetime, timedelta

owm = OWM('OWM API')
mgr = owm.weather_manager()

weekdayArray = []

observation = mgr.forecast_at_id("Enter City ID", "3h")

for i in range(1, 6):
    current_date = datetime.now().date()
    tomorrow_date = current_date + timedelta(days=i)
    tomorrow_noon = datetime.combine(tomorrow_date, datetime.strptime("12:00:00", "%H:%M:%S").time())
    
    weather = observation.get_weather_at(tomorrow_noon)
    
    message = "WEATHER\n" + str(weather.temperature("fahrenheit")["temp_max"]) + '\n' + str(weather.detailed_status)  + '\n' + str(weather.clouds) + "\n" + str(weather.reference_time(timeformat="iso"))
    print(message + "\n")
    weekdayArray.append([tomorrow_noon, weather.temperature("fahrenheit")["temp_max"], weather.detailed_status, ])


sinch_client = SinchClient(
    key_id="Sinch Key ID",
    key_secret="Sinch Key Secret",
    project_id="Sinch Project ID"
)

final = ""
final += """======WEEKDAY======\n=  """ + str(current_date.month).zfill(2) + "/" + str(current_date.day).zfill(2) + " - " + str(tomorrow_date.month).zfill(2) + "/" + str(tomorrow_date.day).zfill(2) + "  =\n=======SCORE=======\n=                 =\n"

dayArray = []

for day in range(1, len(weekdayArray) + 1):
    tomorrow_date = current_date + timedelta(days=day)
    tomorrow_noon = datetime.combine(tomorrow_date, datetime.strptime("12:00:00", "%H:%M:%S").time())
    
    weather = observation.get_weather_at(tomorrow_noon)
    
    if bool(weather.visibility()):    
        vis = -round((0.005 * (10000 - weather.visibility())), 2)
    else:
        vis = 0
    temp = -round(0.5 * (abs(75 - weather.temperature("fahrenheit")["temp_max"])), 2)
    cloud = -round(weather.clouds/10, 2)
    print(bool(weather.rain))
    if bool(weather.rain):
        rain = -round(30 * weather.rain["3h"], 2)
    else:
        rain = 0
        
    score = 100 + vis + temp + cloud
        
    
    final += "=      " + str(weekdayArray[day-1][0].month).zfill(2) + "/" + str(weekdayArray[day-1][0].day).zfill(2)+"      =\n"
    final += "=      " + str(score)[0:5].ljust(5, "0")+"      =\n"
    final += "=                 =\n"
    
final += "==================="

send_batch_response = sinch_client.sms.batches.send(
    body=final,
    to=["My Phone #"],
    from_="Sinch Phone #",
    delivery_report="none")

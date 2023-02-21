import os

import requests
from twilio.rest import Client
from twilio.http.http_client import  TwilioHttpClient

proxy_client = TwilioHttpClient()
proxy_client.session.proxies = {'https': os.environ['https_proxy']}

OWM_Endpoint = 'https://api.openweathermap.org/data/2.5/onecall'
API_KEY = '00939fb66db62bfd0da9329559973448'

# Twilio
account_sid = 'AC**************'
auth_token = 'your_auth_token'



WEATHER_PARAMS = {
    'lat':  51.507351,
    'lon': -0.127758,
    'exclude': 'current,minutely,daily',
    'appid': API_KEY
}

response = requests.get(OWM_Endpoint, params=WEATHER_PARAMS)
print(response.status_code)
weather_data = response.json()
weather_slice = weather_data['hourly'][:12]

will_rain = False

for hour_data in weather_slice:
    condition_code = hour_data['weather'][0]['id']
    if int(condition_code) < 700:
        will_rain = True

if will_rain:
    client = Client(account_sid, auth_token, http_client=proxy_client)
    message = client.messages.create(
        body='It\'s going to rain today remeber to bring an umbrella',
        from_='+150',
        to='+155',
    )
    print(message.sid)


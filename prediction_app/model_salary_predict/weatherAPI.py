import requests


def weather(location):
    url = "https://api.tomorrow.io/v4/weather/realtime?location="+location+"&apikey=wG5zAl00vCIM9Hb1YkJZzqOi8DwO7XdC"

    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers)

    return response.json()
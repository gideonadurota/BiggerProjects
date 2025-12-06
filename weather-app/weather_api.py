import json
from model import Coordinates
from model import Weather, dt
import requests
import credentials

base_url = f"https://api.openweathermap.org/data/2.5/forecast"
geo_base_url = f"http://api.openweathermap.org/geo/1.0/direct"

def get_coordinates(api_key: str, city_name: str, country_code: str) -> Coordinates | None:
    query_value = f"{city_name},{country_code}"
    payload: dict = {'q': query_value, 'appid': api_key }
    response = requests.get(geo_base_url, params=payload)
    if response.status_code == 200:
        data: dict = response.json()
        if not data:
            print(f"Error: No location data found for '{query_value}'.")
            return None
        latitude: float = data[0]['lat']
        longitude: float = data[0]['lon']
        print(f"Successfully retrieved coordinates: ({latitude}, {longitude})")
        return Coordinates(latitude, longitude)
    else:
        print(f"API Request Failed with status code: {response.status_code}")
        # Optional: print the error message from the API if available
        print(f"API Message: {response.json().get('message', 'N/A')}")
        return None

def get_weather_json(api_key: str, lat: float, lon: float, mock: bool=True) -> dict:
    if mock:
        with open("weather.json", "r") as file:
            return json.load(file)

    payload: dict = {'lat': lat, 'lon': lon, 'appid': api_key, }
    request = requests.get(base_url, params=payload)
    data: dict = request.json()
    if not mock:
        with open("weather.json", "w") as file:
            json.dump(data, file, indent=4)
    return data

def get_weather_details(weather_json: dict) -> list[Weather]:
    days: list[dict] = weather_json.get('list')

    if not days:
        raise Exception(f"Problem with json '{weather_json}'.")

    list_of_weather: list[Weather] = []
    for day in days:
        w: Weather = Weather(date=dt.fromtimestamp(day.get('dt')),
                             details=(details := day.get('main')),
                             temp=details.get('temp'),
                             weather=(weather := day.get('weather')),
                             description=weather[0].get('description'))
        list_of_weather.append(w)

    return list_of_weather

def main():
    api_key = credentials.API_KEY
    city_name: str = input("Enter City: ")
    country_code: str = input("Enter Country Code: ")
    coordinates = get_coordinates(api_key, city_name, country_code)
    longitude: float = coordinates.longitude
    latitude: float = coordinates.latitude
    weather_json = get_weather_json(api_key, latitude, longitude)

    list_of_weather: list[Weather] = get_weather_details(weather_json)

    # for w in list_of_weather:
    #     print(w)

    dfmt: str = '%d/%m/%y'
    days: list[str] = sorted(list({f'{date.date:{dfmt}}' for date in list_of_weather}))

    for day in days:
        print(day)
        print('---')

        grouped: list[Weather] = [current for current in list_of_weather if f'{current.date:{dfmt}}' == day]
        for element in grouped:
            print(element)

        print('')


# get_coordinates(api_key='2025cb112bfeb1b370c0fa7f57180ee5', city_name='tokyo', country_code='JPN', )
# weather_json = get_weather_json(api_key='2025cb112bfeb1b370c0fa7f57180ee5', lat=35.6768601, lon=139.7638947)
# get_weather_details(weather_json)

if __name__ == "__main__":
    main()
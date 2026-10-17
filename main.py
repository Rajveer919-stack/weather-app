# ========== IMPORTS ==========
import requests   # to fetch data from the internet


# ========== 1. API LINKS (free, no key needed) ==========
GEO_URL = "https://geocoding-api.open-meteo.com/v1/search"   # city -> location
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"       # location -> weather


# ========== 2. MEANING OF WEATHER CODES ==========
WEATHER_CODES = {
    0: "Clear sky",
    1: "Mostly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    61: "Light rain",
    63: "Rain",
    65: "Heavy rain",
    95: "Thunderstorm",
}


# ========== 3. FIND THE LOCATION OF A CITY ==========
def get_location(city):
    params = {"name": city, "count": 1}
    response = requests.get(GEO_URL, params=params, timeout=10)
    data = response.json()

    # If the city is not found, the "results" key is missing
    if "results" not in data:
        return None

    place = data["results"][0]
    return place["latitude"], place["longitude"], place["name"], place.get("country", "")


# ========== 4. GET THE CURRENT WEATHER ==========
def get_weather(lat, lon):
    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": True,
    }
    response = requests.get(WEATHER_URL, params=params, timeout=10)
    return response.json()["current_weather"]


# ========== 5. SHOW THE RESULT ==========
def show_weather(city):
    location = get_location(city)

    if location is None:
        print("City not found, please check the spelling.")
        return

    lat, lon, name, country = location
    weather = get_weather(lat, lon)

    # Look up the weather code, use "Unknown" if it is not in the list
    condition = WEATHER_CODES.get(weather["weathercode"], "Unknown")

    print(f"\nCity: {name}, {country}")
    print(f"Temperature: {weather['temperature']} °C")
    print(f"Wind speed: {weather['windspeed']} km/h")
    print(f"Condition: {condition}")


# ========== 6. MAIN PROGRAM ==========
while True:
    city = input("\nEnter a city name (q to quit): ").strip()

    if city.lower() == "q":
        print("Bye!")
        break

    # Do not crash if there is no internet or the API is down
    try:
        show_weather(city)
    except requests.exceptions.RequestException:
        print("Network or API problem, please try again.")
# ========== IMPORTS ==========
import requests   # internet se data lene ke liye


# ========== 1. API LINKS (free, key nahi chahiye) ==========
GEO_URL = "https://geocoding-api.open-meteo.com/v1/search"   # city -> location
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"       # location -> mausam


# ========== 2. WEATHER CODE KA MATLAB ==========
WEATHER_CODES = {
    0: "Saaf aasman",
    1: "Zyadatar saaf",
    2: "Thode badal",
    3: "Badal chhaye hue",
    45: "Kohra",
    61: "Halki baarish",
    63: "Baarish",
    65: "Tez baarish",
    95: "Toofan",
}


# ========== 3. CITY KA LOCATION NIKALNA ==========
def get_location(city):
    params = {"name": city, "count": 1}
    response = requests.get(GEO_URL, params=params, timeout=10)
    data = response.json()

    # Agar city nahi mili to "results" key hoti hi nahi
    if "results" not in data:
        return None

    place = data["results"][0]
    return place["latitude"], place["longitude"], place["name"], place.get("country", "")


# ========== 4. MAUSAM NIKALNA ==========
def get_weather(lat, lon):
    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": True,
    }
    response = requests.get(WEATHER_URL, params=params, timeout=10)
    return response.json()["current_weather"]


# ========== 5. RESULT DIKHANA ==========
def show_weather(city):
    location = get_location(city)

    if location is None:
        print("City nahi mili, spelling check karo.")
        return

    lat, lon, name, country = location
    weather = get_weather(lat, lon)

    # Code ka matlab dhundo, na mile to "Unknown"
    condition = WEATHER_CODES.get(weather["weathercode"], "Unknown")

    print(f"\nShehar: {name}, {country}")
    print(f"Temperature: {weather['temperature']} °C")
    print(f"Hawa ki speed: {weather['windspeed']} km/h")
    print(f"Halat: {condition}")


# ========== 6. MAIN PROGRAM ==========
while True:
    city = input("\nCity ka naam likho (exit ke liye q): ").strip()

    if city.lower() == "q":
        print("Bye!")
        break

    # Internet na ho ya API band ho to program crash na ho
    try:
        show_weather(city)
    except requests.exceptions.RequestException:
        print("Internet ya API mein problem hai, dobara try karo.")
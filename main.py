import requests
import datetime
import heapq
import logging
from collections import OrderedDict

# Configure standard logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

#Configuration
API_KEY = "0eafccb5f140b072ea670ecf30bd35ed"
CACHE_EXPIRY_MINUTES = 10
MAX_CACHE_SIZE = 10

class WeatherCache:
    def __init__(self, capacity: int = MAX_CACHE_SIZE):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, city: str):
        city = city.lower().strip()
        if city not in self.cache:
            return None
        
        entry = self.cache[city]
        if datetime.datetime.now() - entry["timestamp"] > datetime.timedelta(minutes=CACHE_EXPIRY_MINUTES):
            logging.warning("API_CACHE_EXPIRED: Serving stale data for '%s', evicting.", city)
            del self.cache[city]
            return None
        
        self.cache.move_to_end(city)
        return entry["data"]

    def put(self, city: str, data: dict):
        city = city.lower().strip()
        if city in self.cache:
            del self.cache[city]
        elif len(self.cache) >= self.capacity:
            evicted, _ = self.cache.popitem(last=False)
            logging.info("CACHE_EVICTION: Capacity full, evicted '%s'", evicted)
            
        self.cache[city] = {
            "timestamp": datetime.datetime.now(),
            "data": data
        }


class AnalyticsEngine:
    def __init__(self):
        self.min_heap = []
        self.max_heap = []

    def add_record(self, city_name: str, temp: float):
        heapq.heappush(self.min_heap, (temp, city_name))
        heapq.heappush(self.max_heap, (-temp, city_name))

    def get_coldest(self):
        if not self.min_heap:
            return None
        temp, city = self.min_heap[0]
        return {"city": city, "temp": temp}

    def get_hottest(self):
        if not self.max_heap:
            return None
        neg_temp, city = self.max_heap[0]
        return {"city": city, "temp": -neg_temp}


weather_cache = WeatherCache()
analytics = AnalyticsEngine()


def fetch_weather(city_name: str, api_key: str = API_KEY):
    # 1. Cache Hit
    cached_data = weather_cache.get(city_name)
    if cached_data:
        logging.info("CACHE_HIT: Returning data for '%s'", city_name)
        return cached_data

    # 2. Cache Miss
    logging.info("CACHE_MISS: Fetching fresh data from API for '%s'", city_name)
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            weather_info = {
                "city": data["name"],
                "country": data["sys"]["country"],
                "temp": data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "wind_speed": data["wind"]["speed"],
                "description": data["weather"][0]["description"]
            }
            weather_cache.put(city_name, weather_info)
            analytics.add_record(weather_info["city"], weather_info["temp"])
            return weather_info
        else:
            logging.error("API_FAILURE: Received status code %s for '%s'", response.status_code, city_name)
            return None
    except requests.exceptions.RequestException as e:
        logging.error("NETWORK_ERROR: Failed to connect to OpenWeatherMap: %s", e)
        return None


if __name__ == "__main__": 
    while True:
        print("\n--- Menu ---")
        print("1. Fetch Weather")
        print("2. View Analytics (Hottest & Coldest queried cities)")
        print("3. Exit")
        
        choice = input("Enter choice (1-3): ").strip()
        if choice == "1":
            user_city = input("Enter city name: ").strip()
            if user_city:
                result = fetch_weather(user_city)
                if result:
                    print(result)
        elif choice == "2":
            coldest = analytics.get_coldest()
            hottest = analytics.get_hottest()
            if coldest and hottest:
                print(f"\n[ANALYTICS] Coldest: {coldest['city']} ({coldest['temp']} °C)")
                print(f"[ANALYTICS] Hottest: {hottest['city']} ({hottest['temp']} °C)")
            else:
                print("\nNo analytics data available yet.")
        elif choice == "3":
            break





"""data = weather.json()
print("city",city)
print("country",data["sys"]["country"])
print("Temprature",data['main']['temp'])
print("Humidity",data['main']['humidity'])
print("Wind Speed",data['wind']['speed'])
print("Weather",data['weather'][0]['description'])"""

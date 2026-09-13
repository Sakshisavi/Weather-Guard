# Weather Analytics & Caching Engine 🌤️

A high-performance Python/Flask web application designed to fetch real-time weather metrics via the OpenWeatherMap API. The system incorporates custom low-level data structures for in-memory caching and real-time analytical tracking, minimizing API consumption and optimizing response times.

---

## 🚀 Features

* **Real-Time Weather Data**: Fetches real-time temperature, humidity, wind speed, and weather conditions.
* **Custom LRU Cache (`WeatherCache`)**: Uses an `OrderedDict` structure to cache API queries up to a set capacity (`MAX_CACHE_SIZE = 10`) with automatic expiration tracking (`CACHE_EXPIRY_MINUTES = 10`).
* **Analytics Engine (`AnalyticsEngine`)**: Uses Min/Max Heaps (`heapq`) to track the coldest and hottest queried cities in $O(1)$ time complexity.
* **Flask Web Interface**: Interactive user interface with dynamic weather GIFs tailored to real-time conditions.
* **CLI Mode**: Interactive terminal interface running side-by-side with the web backend.
* **Automated Testing Suite**: Full test coverage using `pytest` for unit testing caching behavior, heap operations, and Flask routes.

---

## 🛠️ Tech Stack

* **Backend Framework**: Python, Flask, Jinja2
* **Data Structures**: Min/Max Heaps (`heapq`), `OrderedDict`
* **External API**: OpenWeatherMap API
* **Testing & Tools**: Pytest, Pytest-Cov, Requests

---

## 📋 Installation & Setup

1. **Clone the Repository**:
   ```bash
   git clone [https://github.com/your-username/weather-engine.git](https://github.com/your-username/weather-engine.git)
   cd weather-engine
3. **Create & Activate a Virtual Environment (Optional)**:

Bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
3. **Install Dependencies**:

Bash
pip install -r requirements.txt
4. **Run the Application**:

 **Web Server**:

 Bash
 python api.py
 Navigate to http://127.0.0.1:5000 in your web browser.

 **CLI Interface**:

 Bash
 python main.py
5. **Run Unit Tests**:

  Bash
  pytest test_weather.py
  
**📊 System Architecture**
[ User Interface (Flask / CLI) ]
               │
               ▼
      [ WeatherCache ]  ──(Cache Hit)──► Return Stored Weather Data
               │
          (Cache Miss)
               │
               ▼
    [ OpenWeatherMap API ]
               │
               ├──► Store Result in WeatherCache (LRU Eviction)
               └──► Update AnalyticsEngine (Min/Max Heaps)


**1st Page You'll See** 
<img width="1912" height="955" alt="1st" src="https://github.com/user-attachments/assets/286daef5-4f85-4f33-8aef-3f5b9a650a1f" />

**2nd Enter Your City**
<img width="1911" height="960" alt="city" src="https://github.com/user-attachments/assets/bcbe0276-ee14-4e2a-a9a7-37170fa1ed0c" />

**3rd Your Weather Report According To City**
<img width="1911" height="965" alt="ur_weather" src="https://github.com/user-attachments/assets/a8ec30af-1875-4a2b-8981-4fe2e0067ede" />


**Your Weather Report of Different city(example)**
<img width="1898" height="963" alt="ur_weather2" src="https://github.com/user-attachments/assets/2da2a7f8-d34d-439d-8174-e7796910ed1b" />

**5th Analytics Page : It will show Analytics according to your Query**
<img width="1907" height="961" alt="anal" src="https://github.com/user-attachments/assets/37b8ef87-028f-48f5-ac36-fe2669163488" />


import pytest
from main import WeatherCache, AnalyticsEngine, fetch_weather
from api import app

def test_cache_put_and_get():
    """Test if fetching a city populates and retrieves from cache correctly."""
    cache = WeatherCache(capacity=2)
    mock_data = {"city": "Delhi", "temp": 30.0}
    
    cache.put("Delhi", mock_data)
    result = cache.get("Delhi")
    
    assert result is not None
    assert result["city"] == "Delhi"
    assert result["temp"] == 30.0

def test_cache_hit():
    """Test that querying an existing city triggers a cache hit."""
    cache = WeatherCache(capacity=2)
    mock_data = {"city": "London", "temp": 15.0}
    
    cache.put("London", mock_data)
    # First lookup
    assert cache.get("London") == mock_data
    # Second lookup should still be present
    assert cache.get("London") == mock_data

def test_cache_eviction():
    """Test that the cache evicts the oldest item when capacity is exceeded."""
    cache = WeatherCache(capacity=2)
    cache.put("Delhi", {"temp": 30})
    cache.put("Mumbai", {"temp": 32})
    
    # Adding a 3rd city should evict 'Delhi'
    cache.put("Tokyo", {"temp": 10})
    
    assert cache.get("Delhi") is None  # Evicted
    assert cache.get("Mumbai") is not None
    assert cache.get("Tokyo") is not None

def test_analytics_heap():
    """Test if min/max heaps accurately track coldest and hottest cities."""
    analytics = AnalyticsEngine()
    analytics.add_record("Delhi", 35.0)
    analytics.add_record("Reykjavik", -2.0)
    analytics.add_record("London", 15.0)
    
    coldest = analytics.get_coldest()
    hottest = analytics.get_hottest()
    
    assert coldest["city"] == "Reykjavik"
    assert coldest["temp"] == -2.0
    assert hottest["city"] == "Delhi"
    assert hottest["temp"] == 35.0

def test_invalid_city_input():
    """Test edge cases such as invalid city inputs gracefully returning None."""
    result = fetch_weather("invalid_city_name_xyz_12345")
    assert result is None

 



def test_analytics_min_max_heap():
    analytics = AnalyticsEngine()
    
    analytics.add_record("Delhi", 32.5)
    analytics.add_record("London", 12.0)
    analytics.add_record("Tokyo", 18.2)
    
    coldest = analytics.get_coldest()
    hottest = analytics.get_hottest()
    
    assert coldest["city"] == "London"
    assert coldest["temp"] == 12.0
    
    assert hottest["city"] == "Delhi"
    assert hottest["temp"] == 32.5

def test_empty_analytics():
    analytics = AnalyticsEngine()
    assert analytics.get_coldest() is None
    assert analytics.get_hottest() is None   



@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_route(client):
    response = client.get('/')
    assert response.status_code == 200

def test_city_route(client):
    response = client.get('/city')
    assert response.status_code == 200

def test_analytics_route(client):
    response = client.get('/Analytics')
    assert response.status_code == 200

def test_exit_route(client):
    response = client.get('/exit')
    assert response.status_code == 200    

def test_get_weather_post_missing_city(client):
    # Test POST request with an empty form (redirects to /city)
    response = client.post('/get_weather', data={'city_name': ''})
    assert response.status_code == 302
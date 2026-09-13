from flask import Flask, render_template, request, redirect, url_for
from main import fetch_weather, weather_cache, analytics, API_KEY

app = Flask(__name__)

WEATHER_GIFS = {
    "Clear": "https://i.gifer.com/origin/45/454ba38b4ce5b3fdc8796ed710769e69.gif",
    "cloud": "https://i.pinimg.com/originals/2c/73/10/2c7310e053c7118e69182ab7baf1347a.gif",
    "rain": "https://i.pinimg.com/originals/8e/06/fa/8e06fa349b64a02cb9932114d386289c.gif",
    "drizzle": "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExYnJmbmdjczVwdjdyZXgwdWw0aDFxOHFqczU5bmM5ZjNveDNpZHJ2ciZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/t7Qb8655Z1VfBGr5XB/giphy.gif",
    "thunderstorm": "https://www.bing.com/th/id/OGC.958b3928314daf1b7caafc3244ee8052?r=0&o=7&pid=1.7&rm=3&rurl=https%3a%2f%2fi.pinimg.com%2foriginals%2f4b%2fe7%2f37%2f4be737504643b5fef459fc49b6188c1a.gif&ehk=Sek0drEi8L1hwDALFwWK2g41egsXzQIhK%2bq2%2bZMlyto%3d",
    "snow": "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExMnAxdWZ0aGlwYWp0azEyczRhOXd2dHpqbzFiMHpmaXdrMHExMnMzaCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/XiXv44X2ZtFT75XryH/giphy.gif",
    "default": "https://64.media.tumblr.com/6d6afbffe62151952716c70846531b93/tumblr_pygacdGt1j1yw5xa3o1_640.gifv"
}

@app.route('/')
def index():
    return render_template('Index.html')

@app.route('/city')
def city():
    return render_template('city.html')

@app.route('/get_weather', methods=['POST'])
def get_weather():
    city_name = request.form.get('city_name')
    if not city_name:
        return redirect(url_for('city'))
        
    weather_data = fetch_weather(city_name, API_KEY)
    if not weather_data:
        return "<h3>City not found or API error. <a href='/city'>Try Again</a></h3>"
        
    # Partial word match (e.g. "scattered clouds" matches "cloud")
    desc = weather_data['description'].lower()
    selected_gif = WEATHER_GIFS["default"]
    
    for key, gif_url in WEATHER_GIFS.items():
        if key in desc:
            selected_gif = gif_url
            break
            
    return render_template('Your_Weather.html', weather=weather_data, bg_gif=selected_gif)

@app.route('/Analytics')
def show_analytics():
    # Fetch coldest and hottest records from AnalyticsEngine heaps
    coldest = analytics.get_coldest()
    hottest = analytics.get_hottest()
    return render_template('Analytics.html', coldest=coldest, hottest=hottest)


@app.route('/exit')
def exit():
    return render_template('exit.html')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
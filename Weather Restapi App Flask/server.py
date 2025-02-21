from flask import Flask, render_template, request
from weather import get_weather
from waitress import serve

app = Flask(__name__)


@app.route("/")
@app.route("/index")
def index():

    return render_template("index.html")

@app.route("/weather")
def weather():
    city = request.args.get("city")

    if not city.strip():
        city = "Pune"

    data = get_weather(city)

    if data["cod"] == '404':

        return render_template("error.html")
    
    else:

        return render_template(
            "weather.html",
            title = data['name'],
            status = data['weather'][0]['description'].capitalize(),
            temp = f"{data['main']['temp'] - 273.15:.1f}°C",
            feels_like = f"{data['main']['feels_like'] - 273.15:.1f}°C"

        )

if __name__ == "__main__":
    app.run(host="0.0.0.0",port = 8000)
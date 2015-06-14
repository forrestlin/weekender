import datetime
from flask import Flask, render_template, redirect, request, flash, session, jsonify, json
from jinja2 import StrictUndefined
from flask_debugtoolbar import DebugToolbarExtension
from keys import amadeus_token
from keys import instagram_token
import requests
import pprint

app = Flask(__name__)

app.secret_key = "ABC"

app.jinja_env.undefined = StrictUndefined

@app.route('/')
def go_home():
	"""Homepage."""
	result = get_flights_list('SFO', 2)
	print result
	return render_template("base.html")

@app.route('/flight-results')
def get_flight_results():
	flight = "flight 1"
	price = "price"
	departure_time = "departure_time"
	arrival_time = "arrival_time"
	flight_results = [flight, price, departure_time, arrival_time]

	return render_template("/flight_results.html", flight=flight, price=price, departure_time=departure_time, arrival_time=arrival_time, flight_results=flight_results)

@app.route('/my-flight')
def media_search():
	api = requests.get('https://api.instagram.com/v1/media/search?lat=48.858844&lng=2.294351&access_token={token}'.format(token=instagram_token))

	pics_json = api.json()
	data_list = pics_json.get("data")
	pics = []
	for item in data_list:
		images = item.get("images")
		image_info = images.get("standard_resolution")
		url = image_info.get("url")
		pics.append(url)

	return render_template("/my_flight.html", url=pics[:6])

def get_flights_list(origin, duration):
	today = datetime.date.today() + datetime.timedelta(days=1) # this is a hack because amadeus sucks
	tomorrow = today + datetime.timedelta(days=1)

	departure_date_str = '--'.join([today.isoformat(), tomorrow.isoformat()])

	api = requests.get(
		'http://api.sandbox.amadeus.com/v1.2/flights/inspiration-search?origin={origin}'
		'&departure_date={departure}&duration={duration}&max_price=1500&apikey={token}'.format(
			origin=origin,
			departure=departure_date_str,
			duration=duration,
			token=amadeus_token
		)
	)

	response_json = api.json()
	return response.get("results")


if __name__ == "__main__":
	app.debug = True
	DebugToolbarExtension(app)
	app.run()
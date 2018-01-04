from flask import Flask
from flask import request, redirect
import flask

from twilio.rest import TwilioRestClient
import twilio.twiml

import re   # for input sanitation

# Input credentials
account_sid = "ACf891c28f724f2659c5d9fd4a492a389f"
auth_token = "cf0c3455631abb460684cc1f56cf02c9"
client = TwilioRestClient(account_sid, auth_token)



app = Flask(__name__)


#Doesn't require anything
#Mainly the introduction after a successful connection
@app.route('/', methods=['GET', 'POST'])
def index():
	response = twilio.twiml.Response()
	response.say("Welcome")

	# input listener
	with response.gather(action="/fizz", method="POST", timeout="3") as r:
		r.say("Enter any number on the key and wait a moment to play Phone Buzz.")

	return flask.render_template('index.html')

#doesn't require anything beforehand
#Creates the necessary information before sending the request
#POST onto /play
@app.route("/call", methods=['POST'])
def phone():
	phone_number = request.form['phone']
	call = client.calls.create(to=phone_number,
                           from_="+16042650572",
                           url="https://phonebuzzing.herokuapp.com/play")

	return redirect('/')

# regex wouldn't pick up edge cases such as +1 (xxx) - xxx - xxx
# checking in html instead
#
# def checker(phone_number):
# 	match_number = re.match('^(?:(?:\+?1\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?$', phone_number)
#
# 	if len(str(match_number.group())) == 10:
# 		return "1" + match_number.group()
# 	elif len(str(match_number.group())) == 11:
# 		return match_number.group()
# 	else:
# 		return "error"


#Requires a number to start FizzBuzz
#Returns fizzbizz through /fizz
@app.route("/play", methods=['GET', 'POST'])
def play():
	# Greet user
	response = twilio.twiml.Response()
	response.say("Hey")

	# Listen for caller to press keys for number
	with response.gather(action="/fizz", method="POST", timeout="5") as r:
		r.say("Enter a number on your keypad and wait to start PhoneBuzz.")

	return str(response)

#requires a POST to be made beforehand
# calculates the fizzbuzz to the desired number
#returns a str as a response
@app.route("/fizz", methods=['GET', 'POST'])
def fizz():
	digits = request.values.get('Digits', None)
	values = fizzbuzz(int(digits))
	response = twilio.twiml.Response()
	response.say("starting Phonebuzz")

	for v in values:
		response.pause(length=1)
		response.say(v)

	response.pause(length=3)
	response.say("PhoneBuzz is all done. Thanks for playing.")

	return str(response)

#Requres Nothing
#Plays fizzbuzz by first trying to see if the desired number, n, is valid
#returns a string array
def fizzbuzz(n):
	values = []

	try:
		n = int(n)
	except:
		return"invalid number. Try again"
	for i in range(1, n + 1):
		if i % 5 == 0 and i % 3 == 0:
			values.append("fizz buzz")
		elif i % 3 == 0:
			values.append("fizz")
		elif i % 5 == 0:
			values.append("buzz")
		else:
			values.append(str(i))

	return values
if __name__ == "__main__":
    app.run(debug=True)

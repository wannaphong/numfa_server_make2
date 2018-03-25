# -*- coding: utf-8 -*-
from flask import Flask
from datetime import datetime
import os
app = Flask(__name__)

@app.route('/')
def homepage():
    the_time = datetime.now().strftime("%A, %d %b %Y %l:%M %p")

    return """
    <h1>Hello heroku</h1>
    <p>It is currently {time}.</p>

    <img src="http://loremflickr.com/600/400" />
    """.format(time=the_time)

if __name__ == '__main__':
	#port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', debug=True)
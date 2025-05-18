from flask import Flask, render_template
from gpiozero import LED
import time

r = LED(14)
r = LED(15)
b = LED(18)

while True:
	b.off()
	
# app = Flask(__name__)

# @app.route('/')
# def home():
    # return render_template('index.html')

# if __name__ == '__main__':
    # app.run(host="0.0.0.0", debug=True)

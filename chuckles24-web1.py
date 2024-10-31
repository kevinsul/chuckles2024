# Description: This is the main python file for the web server that controls the GPIO pins on the Raspberry Pi.

# Import the necessary libraries
import os
import sys
import time
import random
from flask import Flask, render_template, request
import gpiod
import time

#Configure access to GPIO stuff.
chip = gpiod.Chip('gpiochip4')

#set up smoke pin...
# GPIO 8 is where I have the relay connected to the RPi that turns the smoke machine on and off.
smoke_pin = 8
smoke_line = chip.get_line(smoke_pin)
smoke_line.request(consumer="LED", type=gpiod.LINE_REQ_DIR_OUT)

#set up fire pin...
# GPIO 7 is where I have the relay connected to the RPi that turns the fire machine on and off.
fire_pin = 7
fire_line = chip.get_line(fire_pin)
fire_line.request(consumer="LED", type=gpiod.LINE_REQ_DIR_OUT)

#set up horn pin...
# GPIO 9 is where I have the relay connected to the RPi that turns the horn on and off.
horn_pin = 9
horn_line = chip.get_line(horn_pin)
horn_line.request(consumer="LED", type=gpiod.LINE_REQ_DIR_OUT)

# Create an instance of the Flask class
app = Flask(__name__)

# Define the home route
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        input_text = request.form["input"]
        # Do something with input_text here
    return render_template("home.html")

# Define the firebutton route
@app.route('/firebutton', methods=['POST'])
def firebutton():
    if request.method == 'POST':
        # Do something here
        fire_line.set_value(1)
        time.sleep(1)
        fire_line.set_value(0)
        pass
    return render_template("home.html")

# Define the smokebutton route
@app.route('/smokebutton', methods=['POST'])
def smokebutton():
    if request.method == 'POST':
        # Do something here
        smoke_line.set_value(1)
        time.sleep(4)
        smoke_line.set_value(0)
        pass
    return render_template("home.html")

# Define the hornbutton route
@app.route('/hornbutton', methods=['POST'])
def hornbutton():
    if request.method == 'POST':
        # Do something here
        horn_line.set_value(1)
        time.sleep(1.5)
        horn_line.set_value(0)
        pass
    return render_template("home.html")

# Define the donotpressbutton route
@app.route('/donotpressbutton', methods=['POST'])
def donotpressbutton():
    if request.method == 'POST':
        # Do something here
        pass
    return render_template("home.html")

# Run the app
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)


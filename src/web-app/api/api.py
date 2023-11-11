from flask import Flask
import time

app = Flask(__name__)

@app.route('/')
def hello2():
    return "Hello ghazaly"
def hello1():
    return "Hello albert"

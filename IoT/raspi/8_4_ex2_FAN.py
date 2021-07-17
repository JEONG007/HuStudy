'''FAN 타이머 작동
1) "fan on for X second(s)" 명령에 대해 X초 동안 작동하도록 구현
2) X는 {1, 2, 3} 중 하나'''

import RPi.GPIO as GPIO
from time import sleep

from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return "hello world"

@app.route('/fan/<second>')
def ledonfoff(second):
    if second == "one":
        print("FAN 1")
        GPIO.output(18, 1)
        sleep(1)
        GPIO.output(18, 0)
        return "one"

    elif second == "two":
        print("FAN 2")
        GPIO.output(18, 1)
        sleep(2)
        GPIO.output(18, 0)
        return "two"

    elif second == "three":
        print("FAN 3")
        GPIO.output(18, 1)
        sleep(3)
        GPIO.output(18, 0)
        return "three"

if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.OUT, initial=GPIO.LOW)
    app.run(host='0.0.0.0', port=5000, debug=True)
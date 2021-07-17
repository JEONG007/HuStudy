import RPi.GPIO as GPIO
from time import sleep

'''LED 발광 모드 변경
1) LED가 모두 꺼진 초기(initial) 상태
2) "Turn on LED"/ "Turn off LED" 명령에 맞춰 전체 LED ON/OFF
3) LED가 모두 켜진 상황에서, "Party mode"를 명령하면 0.5초 간격으로 전체 LED 점멸'''

from flask import Flask
app = Flask(__name__)

onoff_flag = 0
ledTable = [4,5,14,15]

@app.route('/')
def hello():
    return "hello world"

@app.route('/led/<onoff>')
def ledonfoff(onoff):
    global onoff_flag
    if onoff == "on":
        print("LED Turn on")
        onoff_flag = 1
        GPIO.output(ledTable, 1)
        return "LED on"

    elif onoff == "off":
        print("LED Turn off")
        onoff_flag = 0
        GPIO.output(ledTable, 0)
        return "LED off"

    elif onoff == "party":
        if onoff_flag == 1:
            onoff_flag = 0
            print("LED party mode")
            for i in range(5):
                GPIO.output(ledTable, 0)
                sleep(0.5)
                GPIO.output(ledTable, 1)
                sleep(0.5)
        return "LED party mode"

if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(ledTable, GPIO.OUT, initial=GPIO.LOW)
    app.run(host='0.0.0.0', port=5000, debug=True)
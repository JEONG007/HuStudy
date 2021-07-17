'''온도 및 습도 조건에 따른 팬 구동
1) DHT11에서 온도와 습도를 1초마다 측정
2) 온도가 28도 이상이거나(or) 습도가 60% 이상일 시, FAN 구동
3) 다시 온도와 습도가 일정치 이하로 내려가면, FAN OFF'''

import board
import adafruit_dht
import RPi.GPIO as GPIO
from time import sleep

FAN_PIN1 = 18
dhtDevice = adafruit_dht.DHT11(board.D17)

def main():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(FAN_PIN1, GPIO.OUT, initial=False)
    print("main() program")
    while True:
        try:
            temperature_c = dhtDevice.temperature
            humidity = dhtDevice.humidity
            print(f"Temp: {temperature_c:.1f} Humidity: {humidity}")
        except RuntimeError as error:
            print(error.args[0])
        sleep(1.0)

        if (humidity >= 60) or (temperature_c >= 28):
            GPIO.output(FAN_PIN1, GPIO.HIGH)
        else:
            GPIO.output(FAN_PIN1, GPIO.LOW)

if __name__ == '__main__':
    main()
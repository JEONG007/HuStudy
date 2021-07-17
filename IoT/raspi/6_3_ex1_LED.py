'''LED 순차 점등 제어
1) 0개의 LED가 켜진 초기(initial) 상태
2) 0.5초 간격으로 1개의 LED가 차례로 점등(ON)
3) 4개의 LED가 켜졌을 때, 1개씩 차례로 소등(OFF)
4) 1-3의 과정이 반복'''

import RPi.GPIO as GPIO
from time import sleep

LED_1 = 4
LED_2 = 5
LED_3 = 14
LED_4 = 15

def main():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    print("main() program running...")
    
    GPIO.setup(LED_1, GPIO.OUT, initial=False)
    GPIO.setup(LED_2, GPIO.OUT, initial=False)
    GPIO.setup(LED_3, GPIO.OUT, initial=False)
    GPIO.setup(LED_4, GPIO.OUT, initial=False)

    try:
        while True:
            sleep(0.5)
            GPIO.output(LED_1, GPIO.HIGH)
            sleep(0.5)
            GPIO.output(LED_2, GPIO.HIGH)
            sleep(0.5)
            GPIO.output(LED_3, GPIO.HIGH)
            sleep(0.5)
            GPIO.output(LED_4, GPIO.HIGH)
            sleep(0.5)
            GPIO.output(LED_4, GPIO.LOW)
            sleep(0.5)
            GPIO.output(LED_3, GPIO.LOW)
            sleep(0.5)
            GPIO.output(LED_2, GPIO.LOW)
            sleep(0.5)
            GPIO.output(LED_1, GPIO.LOW)
            sleep(0.5)

    except KeyboardInterrupt:
        GPIO.cleanup()

if __name__ == '__main__':
    main()
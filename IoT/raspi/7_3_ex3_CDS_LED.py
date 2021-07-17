'''CDS 광량 측정에 따른 LED 제어
1) CDS 측정 voltage 또는 측정 CDS value를 4단계 threshold로 구분
2) Threshold 범위에 따라 LED 점등 개수 결정
3) 가장 어두운 광량 범위: 4개의 LED 점등
가장 밝은 광량 범위: 0개의 LED 점등'''

import RPi.GPIO as GPIO
from time import sleep
import spidev

LED_1 = 4
LED_2 = 5
LED_3 = 14
LED_4 = 15
LEDs = [LED_1, LED_2, LED_3, LED_4]

spi = spidev.SpiDev()
CDS_CHANNEL = 0

def initMcp3208():
    spi.open(0, 0)
    spi.max_speed_hz = 1000000
    spi.mode = 3

def buildReadComman(channel):
    startBit = 0x04
    singleEnded = 0x08

    configBit = [startBit | ((singleEnded | (channel & 0x07)) >> 2),
                 (channel & 0x07) << 6, 0x00]

    return configBit

def processAddcValue(result):
    byte2 = (result[1] & 0x0f)
    return (byte2 << 8) | result[2]

def analogRead(channel):
    if (channel > 7) or (channel < 0):
        return -1

    r = spi.xfer2(buildReadComman(channel))
    adc_out = processAddcValue(r)
    return adc_out

def controlMcp3208(channel):
    analogVal = analogRead(channel)
    return analogVal

def readSensor(channel):
    return controlMcp3208(channel)

def main():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(LEDs, GPIO.OUT, initial = False)
    initMcp3208()
    print("Setup pin as outputs")

    try:
        while True:
            readVal = readSensor(CDS_CHANNEL)

            voltage = readVal * 4.096/ 4096
            if readVal < 800:
                GPIO.output(LEDs, GPIO.HIGH)
            elif 800 < readVal < 1600:
                GPIO.output(LEDs[0:3], GPIO.HIGH)
                GPIO.output(LEDs[3:], GPIO.LOW)
            elif 1600 < readVal < 2400:
                GPIO.output(LEDs[0:2], GPIO.HIGH)
                GPIO.output(LEDs[2:], GPIO.LOW)
            elif 2400 < readVal < 3200:
                GPIO.output(LEDs[0], GPIO.HIGH)
                GPIO.output(LEDs[1:], GPIO.LOW)
            elif 3200 < readVal:
                GPIO.output(LEDs, GPIO.LOW)
            print("CDS Val=%d\tVoltage=%f" % (readVal, voltage))
            sleep(0.05)
    except KeyboardInterrupt:
        GPIO.cleanup()
        spi.close()

if __name__ == '__main__':
    main()
# python3 exercise4.py
# ./ngrok http 5000
# googlesamples-assistant-pushtotalk

# if display error:
# export DISPLAY=:0.0
# xhost +local:root
# xhost +localhost

# smarthome module
# from typing import get_origin
import RPi.GPIO as GPIO
import GPIO_EX
import adafruit_dht
import board
import digitalio
import adafruit_character_lcd.character_lcd as character_lcd
import spidev
import GPIO_EX

# flask module
from flask import Flask

# AI module
import numpy as np
import cv2
import pickle
import threading

# ETC
from time import sleep, time

# =================================================================================================
# Raspiberry Sensor
cdsVal = 0
temperature = 0
humidity = 0
gasVal = 0


# Get all Values
def get_sensor_values():
    global cdsVal, temperature, humidity, gasVal
    cdsVal = readSensor(CDS_CHANNEL)
    temperature = dhtDevice.temperature
    humidity = dhtDevice.humidity
    gasVal = readSensor(GAS_CHANNEL)


# DHT 11
dhtDevice = adafruit_dht.DHT11(board.D17,use_pulseio=False)

# CDS, GAS
spi = spidev.SpiDev()
CDS_CHANNEL = 0
GAS_CHANNEL = 1


def initMcp3208():
    spi.open(0, 0)  # open(bus, device), device0 - GPIO8, device1 - GPIO7
    spi.max_speed_hz = 1000000
    spi.mode = 3


def buildReadCommand(channel):
    startBit = 0x04
    singleEnded = 0x08
    configBit = [startBit | ((singleEnded | (channel & 0x07)) >> 2), (channel & 0x07) << 6, 0x00]
    return configBit


def processAdcValue(result):
    byte2 = (result[1] & 0x0F)
    return (byte2 << 8) | result[2]


def analogRead(channel):
    if (channel > 7) or (channel > 0):
        return -1
    r = spi.xfer2(buildReadCommand(channel))
    adc_out = processAdcValue(r)
    return adc_out


def controlMcp3208(channel):
    analogVal = analogRead(channel)
    return analogVal


def readSensor(channel):
    return controlMcp3208(channel)


# =================================================================================================


# =================================================================================================
# Thread1 - Face Detection

is_Obama = 0  # 오바마 얼굴 인식 flag
is_Hillary = 0  # 힐러리 얼굴 인식 flag


def face_detect():
    global is_Obama, is_Hillary

    face_cascade = cv2.CascadeClassifier(
        '../../OpenCV-Python-Series/src/cascades/data/haarcascade_frontalface_alt2.xml')
    # eye_cascade = cv2.CascadeClassifier('../../OpenCV-Python-Series/src/cascades/data/haarcascade_eye.xml')
    # smile_cascade = cv2.CascadeClassifier('../../OpenCV-Python-Series/src/cascades/data/haarcascade_smile.xml')

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("../../OpenCV-Python-Series/src/recognizers/face-trainner.yml")

    labels = {"person_name": 1}
    with open("../../OpenCV-Python-Series/src/pickles/face-labels.pickle", 'rb') as f:
        og_labels = pickle.load(f)
        labels = {v: k for k, v in og_labels.items()}

    cap = cv2.VideoCapture(0)

    while (True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
        for (x, y, w, h) in faces:
            # print(x,y,w,h)
            roi_gray = gray[y:y + h, x:x + w]  # (ycord_start, ycord_end)
            roi_color = frame[y:y + h, x:x + w]

            # recognize? deep learned model predict keras tensorflow pytorch scikit learn
            id_, conf = recognizer.predict(roi_gray)
            if conf >= 4 and conf <= 85:
                # print(5: #id_)
                # print(labels[id_])
                font = cv2.FONT_HERSHEY_SIMPLEX
                name = labels[id_]
                color = (255, 255, 255)
                stroke = 2
                cv2.putText(frame, name, (x, y), font, 1, color, stroke, cv2.LINE_AA)

                # added code
                if name != 'obama':
                    is_Obama = 0
                else:
                    is_Obama = 1
                if name != 'clinton':
                    is_Hillary = 0
                else:
                    is_Hillary = 1
                # added code - end

            img_item = "7.png"
            cv2.imwrite(img_item, roi_color)

            color = (255, 0, 0)  # BGR 0-255
            stroke = 2
            end_cord_x = x + w
            end_cord_y = y + h
            cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), color, stroke)
            # subitems = smile_cascade.detectMultiScale(roi_gray)
            # for (ex,ey,ew,eh) in subitems:
            #   cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

        # Display the resulting frame
        cv2.imshow('frame', frame)
        if cv2.waitKey(20) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()


# ====================================================================================================
# Thread2 - Smart Home Control
isFace = False  # Face 인증 flag
isOpen = False  # 스마트 홈 인증 flag

# LED
LED_1 = 4
LED_2 = 5
LED_3 = 14
LED_4 = 15
LEDs = [LED_1, LED_2, LED_4, LED_3]

# LCD
# Raspberry Pi pin setup
lcd_rs = digitalio.DigitalInOut(board.D22)
lcd_en = digitalio.DigitalInOut(board.D24)
lcd_d7 = digitalio.DigitalInOut(board.D21)
lcd_d6 = digitalio.DigitalInOut(board.D26)
lcd_d5 = digitalio.DigitalInOut(board.D20)
lcd_d4 = digitalio.DigitalInOut(board.D19)

lcd_columns = 16
lcd_rows = 2

lcd = character_lcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows)

# KEYPAD
ROW0_PIN = 0
ROW1_PIN = 1
ROW2_PIN = 2
ROW3_PIN = 3
COL0_PIN = 4
COL1_PIN = 5
COL2_PIN = 6

COL_NUM = 3
ROW_NUM = 4

g_preData = 0

colTable = [COL0_PIN, COL1_PIN, COL2_PIN]
rowTable = [ROW0_PIN, ROW1_PIN, ROW2_PIN, ROW3_PIN]

# PIR
PIR_PIN = 7
pirState = 0
pirTime = 0

# BUZZER
BUZZER_PIN = 7
scale = [261, 294, 329, 349, 392, 440, 493, 523]
melodyList = [4, 4, 5, 5, 4, 4, 2]  # 4, 4, 4, 2, 2, 1, 4, 4, 5, 5, 4, 4, 2, 4, 2, 1, 2, 0]
noteDurations = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 1]
#  0.5, 0.5, 0.5, 0.5, 1,
#  0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 1, 0.5, 0.5, 0.5, 0.5, 1]
noteDurations1 = [1, 1, 1, 1]

# FAN
FAN_PIN1 = 18
FAN_PIN2 = 27

# flag on flask request
led_on = False
fan_on = False
buzzer_on = False
printLCD = False
auto_on = False


# auto
def led_auto():
    global cdsVal

    if cdsVal < 800:
        GPIO.output(LEDs, GPIO.HIGH)
    elif 800 < cdsVal < 1600:
        GPIO.output(LEDs[0:3], GPIO.HIGH)
        GPIO.output(LEDs[3:], GPIO.LOW)
    elif 1600 < cdsVal < 2400:
        GPIO.output(LEDs[0:2], GPIO.HIGH)
        GPIO.output(LEDs[2:], GPIO.LOW)
    elif 2400 < cdsVal < 3200:
        GPIO.output(LEDs[0], GPIO.HIGH)
        GPIO.output(LEDs[1:], GPIO.LOW)
    elif 3200 < cdsVal:
        GPIO.output(LEDs, GPIO.LOW)

def fan_auto():
    global temperature, humidity
    if (humidity >= 60) or (temperature >= 28):
        GPIO.output(FAN_PIN1, GPIO.HIGH)
    else:
        GPIO.output(FAN_PIN1, GPIO.LOW)

# lcd
def print_LCD():
    global printLCD, temperature, humidity, cdsVal, gasVal
    if printLCD:
        lcd.clear()
        displayText(f"T:{temperature:.1f}C", 0, 0)
        displayText(f"H:{humidity}%", 8, 0)
        displayText(f"CDS:{cdsVal:1f}", 0, 1)
        displayText(f"GAS:{gasVal}", 8, 1)
    else:
        lcd.clear()


# led
def turn_led():
    global led_on
    if led_on:
        GPIO.output(LEDs, 1)
    else:
        GPIO.output(LEDs, 0)


# fan
def fanControl():
    global fan_on
    if fan_on:
        GPIO.output(18, 1)
    else:
        GPIO.output(18, 0)


# buzzer
def buzzerControl():
    global buzzer_on
    if buzzer_on:
        playBuzzer(melodyList, noteDurations)


# lcd
def initTextlcd():
    lcd.clear()
    lcd.home()
    lcd.cursor_position(0, 0)
    sleep(1.0)


def displayText(text=' ', col=0, row=0):
    lcd.cursor_position(col, row)
    lcd.message = text


# keypad
def initKeypad():
    for i in range(0, COL_NUM):
        GPIO_EX.setup(colTable[i], GPIO_EX.IN)
    for i in range(0, ROW_NUM):
        GPIO_EX.setup(rowTable[i], GPIO_EX.OUT)


def selectRow(rowNum):
    for i in range(0, ROW_NUM):
        if rowNum == (i + 1):
            GPIO_EX.output(rowTable[i], GPIO_EX.HIGH)
            sleep(0.001)
        else:
            GPIO_EX.output(rowTable[i], GPIO_EX.LOW)
            sleep(0.001)
    return rowNum


def readCol():
    keypadstate = -1
    for i in range(0, COL_NUM):
        inputKey = GPIO_EX.input(colTable[i])
        if inputKey:
            keypadstate = keypadstate + (i + 2)
            sleep(0.5)
    return keypadstate


def readKeypad():
    global g_preData
    keyData = -1

    runningStep = selectRow(1)
    row1Data = readCol()
    selectRow(0)
    sleep(0.001)
    if (row1Data != -1):
        keyData = row1Data

    if runningStep == 1:
        if keyData == -1:
            runningStep = selectRow(2)
            row2Data = readCol()
            selectRow(0)
            sleep(0.001)
            if (row2Data != -1):
                keyData = row2Data + 3
        if keyData == -1:
            runningStep = selectRow(3)
            row3Data = readCol()
            selectRow(0)
            sleep(0.001)
            if (row3Data != -1):
                keyData = row3Data + 6
        if keyData == -1:
            runningStep = selectRow(4)
            row4Data = readCol()
            selectRow(0)
            sleep(0.001)
            if (row4Data != -1):
                keyData = row4Data + 9

    if keyData == -1:
        return -1
    if g_preData == keyData:
        g_preData = -1
        return -1
    g_preData = keyData

    return keyData


# pir
def readPir():
    global pirState
    global pirTime
    global isFace  # 얼굴 인증 flag
    global isOpen  # 스마트 홈 인증 flag
    global is_Obama  # 오바마 얼굴 인식 flag
    global is_Hillary  # 힐러리 얼굴 인식 flag
    input_state = GPIO_EX.input(PIR_PIN)

    if is_Hillary == 1:
        lcd.clear()
        displayText("ACCESS DENIED", 0, 1)
        is_Hillary = 0

    if not isFace:
        if input_state == True:  # 동작 감지
            if pirState == 0:  # flag 1로 변환
                print("\r\nMotion Detected.")
                pirTime = time()
                pirState = 1
                return 1

        if pirState == 1:  # 동작 감지 시 아래 동작
            print(time() - pirTime)
            sleep(0.1)
            if time() - pirTime > 3:  # 3초 초과
                playBuzzer(melodyList, noteDurations)  # 부저 울림
                pirState = 0
            else:
                if is_Obama:  # 오바마가 인식되면
                    isFace = True  # 얼굴 인증 True
                    lcd.clear()
                    displayText("ACCESS GRANTED", 0, 1)
                    pirState = 0

    return 0


# buzzer
def playBuzzer(melodyList, noteDurations):
    pwm = GPIO.PWM(BUZZER_PIN, 100)

    pwm.start(100)
    pwm.ChangeDutyCycle(50)

    for i in range(len(melodyList)):
        pwm.ChangeFrequency(scale[melodyList[i]])
        sleep(noteDurations[i])
    pwm.stop()


# thread 2
def smart_home():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(LEDs, GPIO.OUT, initial=GPIO.LOW)
    GPIO_EX.setup(PIR_PIN, GPIO_EX.IN)
    GPIO.setup(BUZZER_PIN, GPIO.OUT)
    GPIO.setup(FAN_PIN1, GPIO.OUT, initial=False)
    GPIO.setup(FAN_PIN2, GPIO.OUT, initial=False)

    pw = [1, 2, 3, 4]
    pw_test = [0, 0, 0, 0]

    count = 0

    initKeypad()
    initMcp3208()
    initTextlcd()
    print("smartHome activate")

    global isOpen, isFace, auto_on

    stTime = time()
    prtTime = time()
    autoTime = time()

    while True:
        try:
            readPir()  # pir 동작 감지(얼굴인식, 부저 포함)
            if isOpen:  # 비밀번호 인증되면 아래 실행
                # 2초 마다 센서 값 받아오기
                if time() - stTime > 2:
                    get_sensor_values()
                    stTime = time()
                # on-off by flags
                if auto_on and (time() - autoTime > 2):
                    led_auto()
                    fan_auto()
                else:
                    fanControl()
                    turn_led()

                buzzerControl()
                #5초 마다 LCD에 프린트하기
                if time() - prtTime > 5:
                    print_LCD()
                    prtTime = time()


            elif isFace:  # 오바마 얼굴 인증되면 아래 실행
                keyData = readKeypad()
                if keyData != -1:
                    pw_test[count] = keyData
                    displayText(str(pw_test[count]), count, 0)
                    count += 1
                if count == 4:
                    lcd.clear()
                    if pw == pw_test:  # 비밀번호 인증되면
                        isOpen = True  # 스마트홈 인증 완료
                        displayText("CORRECT", 0, 1)
                    else:
                        isOpen = False
                        # isObama
                        displayText("FAILED", 0, 1)
                    count = 0


        except KeyboardInterrupt:
            lcd.clear()
            spi.close()
            GPIO.cleanup()
        except RuntimeError as error:
            print(error.args[0])


# =================================================================================================
# Flask Server w/ IFTTT

app = Flask(__name__)


@app.route('/')
def hello():
    return "hello world"


@app.route('/led/<onoff>')
def led_onoff(onoff):
    global led_on, isOpen, auto_on

    if isOpen:
        if auto_on:
            return "Auto mode"
        if onoff == "on":
            led_on = True
        elif onoff == "off":
            led_on = False
        return "ACCESS GRANTED"

    return "ACCESS DENIED"


@app.route('/fan/<onoff>')
def fan_onoff(onoff):
    global fan_on, isOpen, auto_on

    if isOpen:
        if auto_on:
            return "Auto mode"
        if onoff == "on":
            fan_on = True
        elif onoff == "off":
            fan_on = False
        return "ACCESS GRANTED"

    return "ACCESS DENIED"


@app.route('/buzzer/<onoff>')
def buzzeronoff(onoff):
    global buzzer_on, isOpen, auto_on

    if isOpen:
        if auto_on:
            return "Auto mode"
        if onoff == "on":
            buzzer_on = True
        elif onoff == "off":
            buzzer_on = False
        return "ACCESS GRANTED"

    return "ACCESS DENIED"


@app.route('/auto/<onoff>')
def autoonoff(onoff):
    global auto_on, isOpen, led_on, fan_on, buzzer_on, printLCD

    if isOpen:
        if onoff == "on":
            auto_on = True
        elif onoff == "off":
            auto_on = False
            fan_on = False
            buzzer_on = False
            printLCD = False
        return "ACCESS GRANTED"

    return "ACCESS DENIED"

@app.route('/lcd/<onoff>')
def LCD(onoff):
    global printLCD

    if onoff == "on":
        printLCD = True
    elif onoff == "off":
        printLCD = False

    return "ACCESS GRANTED"
# =================================================================================================
# execute code

if __name__ == "__main__":
    # run faceDetact function with thread t1
    global t1
    t1 = threading.Thread(target=face_detect)
    t1.daemon = True
    t1.start()

    # run smarthome function with thread t1
    global t2
    t2 = threading.Thread(target=smart_home)
    t2.daemon = True
    t2.start()

    app.run(host='0.0.0.0', port=5000, debug=False)
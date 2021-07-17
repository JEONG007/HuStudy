'''얼굴 인식을 통한 도어락 이중 잠금
1) Text LCD를 통해 입력 받은 비밀번호 출력 예제에 얼굴 인식 기능 추가
2) 힐러리의 얼굴이 인지된 경우, 비밀번호 일치 여부와 관계 없이 ACCESS DENIED 출
력
3) 오바마의 얼굴이 인지된 경우, 이전에 구현한 예제와 같이 작동
(일치할 경우, CORRECT / 불일치할 경우, FAILED)'''

import numpy as np
import cv2
import pickle

import board
import digitalio
import RPi.GPIO as GPIO
from time import sleep
import adafruit_character_lcd.character_lcd as character_lcd
import threading

detect_state = False
led_status = 0

#lcd
# Raspberry Pi pin setup
lcd_rs = digitalio.DigitalInOut(board.D22)
lcd_en = digitalio.DigitalInOut(board.D24)
lcd_d7 = digitalio.DigitalInOut(board.D21)
lcd_d6 = digitalio.DigitalInOut(board.D26)
lcd_d5 = digitalio.DigitalInOut(board.D20)
lcd_d4 = digitalio.DigitalInOut(board.D19)

# Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows = 2

lcd = character_lcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows)

def initTextlcd():
    lcd.clear()
    lcd.home()
    lcd.cursor_position(0, 0)
    sleep(1.0)

def displayText(text=' ', col=0, row=0):
    lcd.cursor_position(col, row)
    lcd.message = text

def clearTextlcd():
    lcd.clear()
    lcd.message = 'clear LCD\nGoodbye!'
    sleep(2.0)
    lcd.clear()

def controlDevice(detect_state):
    while detect_state:
        if (led_status == 1):
            GPIO.output(4, 1)
            displayText("ACCESS DENIED", 0, 1)
            sleep(3)
            lcd.clear()
        # else:
        #     # GPIO.output(4, 0)
        #     displayText("FAIL", 0, 1)


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(4, GPIO.OUT, initial=GPIO.LOW)

global t
#detect_state = True
t = threading.Thread(target=controlDevice, args=(detect_state,))
t.daemon = True
t.start()

face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml')
eye_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_eye.xml')
smile_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_smile.xml')

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("./recognizers/face-trainner.yml")

labels = {"person_name": 1}
with open("pickles/face-labels.pickle", 'rb') as f:
    og_labels = pickle.load(f)
    labels = {v: k for k, v in og_labels.items()}

cap = cv2.VideoCapture(0)

initTextlcd()

while (True):
    # Capture frame-by-frame
    ret, frame = cap.read()
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

            if name == "obama":
                led_status = 1
            else:
                led_status = 0

        img_item = "7.png"
        cv2.imwrite(img_item, roi_color)

        color = (255, 0, 0)  # BGR 0-255
        stroke = 2
        end_cord_x = x + w
        end_cord_y = y + h
        cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), color, stroke)
    # subitems = smile_cascade.detectMultiScale(roi_gray)
    # for (ex,ey,ew,eh) in subitems:
    #	cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
    # Display the resulting frame
    GPIO.setup(4, GPIO.OUT, initial=GPIO.LOW)
    cv2.imshow('frame', frame)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

# When everything done, release the capture
clearTextlcd()
GPIO.cleanup()
cap.release()
cv2.destroyAllWindows()


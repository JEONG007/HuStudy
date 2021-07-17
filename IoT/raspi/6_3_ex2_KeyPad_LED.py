'''KeyPad 입력 모듈 완성하기
1) 키패드의 3행, 4행의 입력이 나오도록 코드 작성
2) *, #의 입력이 제대로 동작하도록 작성
3) Hint-1: runningStep에 따른 행 선택(selectRow)와 열 입력 감지(readCol)
Hint-2: 문자입력(*, #)은 keyData 변수 저장과 출력에 문자열에 맞게 작성'''

'''KeyPad 입력 숫자에 따른 LED 제어
1) 키패드 각 입력 [1, 2, 3, 4]에 따라 할당된 LED 점등
2) 키패드 1 입력 시, LED_1이 ON
3) LED_i 가 ON인 상태에서 키패드 i 입력 시, OFF
4) [1, 2, 3, 4] 외의 키패드 입력 시, 현재 점등된 모든 LED OFF'''


import RPi.GPIO as GPIO
from time import sleep
import GPIO_EX

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

LED_1 = 4
LED_2 = 5
LED_3 = 14
LED_4 = 15

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
            keypadstate = keypadstate + (i+2)
            sleep(0.5)
    return keypadstate

def readKeypad():
    global g_preData
    keyData = -1

    runningStep = selectRow(1)
    row1Data = readCol()
    selectRow(0)
    sleep(0.001)
    if(row1Data != -1):
        keyData = row1Data

    if runningStep == 1:
        if keyData == -1:
            runningStep = selectRow(2)
            row2Data = readCol()
            selectRow(0)
            sleep(0.001)
            if(row2Data != -1):
                keyData = row2Data + 3
        if keyData == -1:
            runningStep = selectRow(3)
            row3Data = readCol()
            selectRow(0)
            sleep(0.001)
            if(row3Data != -1):
                keyData = row3Data + 6
        if keyData == -1:
            runningStep = selectRow(4)
            row4Data = readCol()
            selectRow(0)
            sleep(0.001)
            if(row4Data != -1):
                keyData = row4Data + 9
            
    sleep(0.1)

    if keyData == -1:
        return -1

    if g_preData == keyData:
        g_preData = -1
        return -1
    g_preData = keyData

    if keyData == 10:
        print("\r\nkeypad Data : %s" % "*")
    elif keyData == 11:
        print("\r\nkeypad Data : %s" % 0)
    elif keyData == 12:
        print("\r\nkeypad Data : %s" % "#")
    else:
        print("\r\nkeypad Data : %s" % keyData)


    return keyData

def main():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    
    GPIO.setup(LED_1, GPIO.OUT, initial=False)
    GPIO.setup(LED_2, GPIO.OUT, initial=False)
    GPIO.setup(LED_3, GPIO.OUT, initial=False)
    GPIO.setup(LED_4, GPIO.OUT, initial=False)
    key1 = 0; key2 = 0; key3 = 0; key4 = 0

    initKeypad()
    print("setup keypad pin")

    try:
        while True:
            keyData = readKeypad()

            if keyData == 1:
                if key1 == 0:
                    GPIO.output(LED_1, GPIO.HIGH)
                    key1 = 1
                else:
                    GPIO.output(LED_1, GPIO.LOW)
                    key1 = 0
            elif keyData == 2:
                if key2 == 0:
                    GPIO.output(LED_2, GPIO.HIGH)
                    key2 = 1
                else:
                    GPIO.output(LED_2, GPIO.LOW)
                    key2 = 0
            elif keyData == 3:
                if key3 == 0:
                    GPIO.output(LED_3, GPIO.HIGH)
                    key3 = 1
                else:
                    GPIO.output(LED_3, GPIO.LOW)
                    key3 = 0
            elif keyData == 4:
                if key4 == 0:
                    GPIO.output(LED_4, GPIO.HIGH)
                    key4 = 1
                else:
                    GPIO.output(LED_4, GPIO.LOW)
                    key4 = 0
            elif keyData != -1:
                GPIO.output(LED_1, GPIO.LOW)
                GPIO.output(LED_2, GPIO.LOW)
                GPIO.output(LED_3, GPIO.LOW)
                GPIO.output(LED_4, GPIO.LOW)
                key1 = 0; key2 = 0; key3 = 0; key4 = 0

    except KeyboardInterrupt:
        GPIO.cleanup()

if __name__ == '__main__':
    main()
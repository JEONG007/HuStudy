'''입력 받은 숫자 출력 및 비밀번호 일치 여부 확인
1) 입력 받은 4자리 숫자를 첫 줄에 출력
2) 두 번째 줄에 입력 받은 숫자가 미리 설정된 비밀번호와 일치하는 지 확인
3) 일치할 경우 CORRECT를, 불일치할 경우 FAIL을 출력'''

import board
import digitalio
import RPi.GPIO as GPIO
from time import sleep
import adafruit_character_lcd.character_lcd as character_lcd
import GPIO_EX

#keypad
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

#led
LED_1 = 4
LED_2 = 5
LED_3 = 14
LED_4 = 15

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

    pw = [1, 2, 3, 4]
    pw_test = [0, 0, 0, 0]

    count = 0

    initKeypad()
    initTextlcd()
    print("setup keypad pin")

    try:
        while True:
            keyData = readKeypad()
            if keyData != -1:
                pw_test[count] = keyData
                displayText(str(pw_test[count]), count, 0)
                count += 1
            if count == 4:
                if pw == pw_test:
                    displayText("CORRECT", 0, 1)
                else:
                    displayText("FAIL", 0, 1)
                count = 0
                sleep(3)
                lcd.clear()
    except RuntimeError as error:
        print(error.args[0])
    except KeyboardInterrupt:
        clearTextlcd()
        GPIO.cleanup()


if __name__ == '__main__':
    main()
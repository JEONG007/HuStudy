'''온도 및 습도 출력
1) DHT11을 통해 구한 온도와 습도 값을 Text LCD에 출력
2) 첫 줄에 Temp. (온도) C
3) 둘 째 줄에 Humidity (습도) % '''

import board
import digitalio
import adafruit_dht
import adafruit_character_lcd.character_lcd as character_lcd
from time import sleep

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

dhtDevice = adafruit_dht.DHT11(board.D17)
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

def main():
    initTextlcd()
    print("start textlcd program ...")
    while True:
        try:
            temperature_c = dhtDevice.temperature
            humidity = dhtDevice.humidity
            print(f"Temp: {temperature_c:.1f} Humidity: {humidity}")
            lcd.clear()
            displayText(str(temperature_c), 0, 0)
            displayText('C', 3, 0)
            displayText(str(humidity), 0, 1)
            displayText('%', 3, 1)
            sleep(3)
        except RuntimeError as error:
            print(error.args[0])
        except KeyboardInterrupt:
            clearTextlcd()

if __name__ == '__main__':
    main()
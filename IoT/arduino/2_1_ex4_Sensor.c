/*센서 및 액츄에이터 통합 – 기본 IoT 시스템 구현
1) 온/습도(DHT22)는 2초마다 측정
2) 토양 습도(SOIL-LINK)는 3초마다 측정
3) FAN / PUMP는 주변 온습도 환경에 따라 자동 동작
  : FAN ON(29도 이상) / FAN OFF (20도 이하) / FAN PWM 65 (사이 범위)
  : PUMP ON (토양 습도 30~60% 사이)
4) 센서 및 액츄에이터 상태 OLED 표시
  : DHT22 및 SOIL-LINK 측정 정보
  : FAN/PUMP/LED 동작 상태
  : LED 자동 ON/OFF 시간 간격*/

#include <U8g2lib.h>
#include "DHT.h"
#include <SoftPWM.h>

SOFTPWM_DEFINE_CHANNEL(A3);
U8G2_SH1106_128X64_NONAME_F_HW_I2C u8g2(U8G2_R0, /* reset=*/ U8X8_PIN_NONE);

#define DHTPIN A1
#define DHTTYPE DHT22
#define SOILHUMI A6
#define LAMP 17
#define PUMP 16


DHT dht(DHTPIN, DHTTYPE);

uint32_t HdtDelay = 2000;
uint32_t Hdt_ST = 0;

uint32_t Soil_Delay = 3000;
uint32_t Soil_ST = 0;

uint32_t TimeCompare;
uint32_t led_ST = 0;

uint32_t TimeSum;
int Hour = 0;
int Minute = 1;


float Temp;
float Humi;
int Soilhumi = 0;

int fan = 0;
String pump = "";

void setup() {
    // put your setup code here, to run once:
    dht.begin();
    u8g2.begin();
    SoftPWM.begin(490);

    
    Serial.begin(9600);
    pinMode(SOILHUMI, INPUT);

    pinMode(LAMP, OUTPUT);
    pinMode(PUMP,OUTPUT);
    TimeSum = (uint32_t)2000;

    Hdt_ST = millis();
    Soil_ST = millis();
    led_ST = millis();
}

void loop() {
  // put your main code here, to run repeatedly:
    if((millis()-Hdt_ST) > HdtDelay) {
        Humi = dht.readHumidity();
        Temp = dht.readTemperature();

        if(isnan(Humi) || isnan(Temp)) {
        Serial.println(F("Failed to read from DHT sensor!"));
        return;
        }
        OLEDdraw();
        Hdt_ST = millis();
    }
    if((millis()-Soil_ST) > Soil_Delay) {
        Soilhumi = map(analogRead(SOILHUMI),0,1023,100,0);

        OLEDdraw();
        Soil_ST = millis();
    }

    TimeCompare = (millis() - led_ST) / TimeSum;
    if(TimeCompare % 2 == 0)
    {
        digitalWrite(LAMP, LOW);
    }
    else if(TimeCompare % 2 == 1)
    {
        digitalWrite(LAMP, HIGH);
    }

    if(Temp >= 29)
    {
        fan = 100;
        SoftPWM.set(100);
    }
    else if(Temp <= 20)
    {
        fan = 0;
        SoftPWM.set(0);
    }
    else
    {
        fan = 65;
        SoftPWM.set(65);
    }

    if(Soilhumi >= 30 && Soilhumi <= 60)
    {
        digitalWrite(PUMP,HIGH);
        pump = "ON";
    }
    else
    {
        digitalWrite(PUMP,LOW);
        pump = "OFF";
    }
}

void OLEDdraw() {
    u8g2.clearBuffer();
  
    u8g2.setFont(u8g2_font_ncenB08_te);
    u8g2.drawStr(15,16, "Temp.");
    u8g2.setCursor(85,15);
    u8g2.print(Temp);
    u8g2.drawStr(114,16,"\xb0");
    u8g2.drawStr(119, 16, "C");

    u8g2.drawStr(15,27,"Humidity");
    u8g2.setCursor(85,27); u8g2.print(Humi);
    u8g2.drawStr(116, 27, "%");

    u8g2.drawStr(15,36, "SoilHumi.");
    u8g2.setCursor(85,35);
    u8g2.print(Soilhumi);

    u8g2.drawStr(15,46, "Fan.");
    u8g2.setCursor(85,45);
    u8g2.print(fan);

    u8g2.drawStr(15,56, "PUMP.");
    u8g2.setCursor(85,55);
    u8g2.print(pump);

    u8g2.drawStr(15,66, "LED.");
    u8g2.setCursor(85,65);
    u8g2.print("2초");

    u8g2.sendBuffer();
}

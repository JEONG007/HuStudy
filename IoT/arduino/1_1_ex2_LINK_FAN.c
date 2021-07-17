/*주변 온도 조건에 따른 DC FAN 제어
1) DHT22의 온도 측정치에 따라 DC FAN ON/OFF
2) 30도 이상 측정 시, DC FAN ON(PWM: 100)
3) 25도 이하 측정 시, DC FAN OFF(PWM: 0)
4) 중간 온도 범위 (25 < temp. < 30)에서 DC FAN PWM 65으로 ON
5) 현재 온도와 DC FAN PWM 제어 상태를 OLED에 표시*/

#include <SoftPWM.h>
#include <U8g2lib.h>

U8G2_SH1106_128X64_NONAME_F_HW_I2C u8g2(U8G2_R0, /* reset=*/ U8X8_PIN_NONE);

#define SOILHUMI A6

SOFTPWM_DEFINE_CHANNEL(A3);

int Solihumi = 0;
int fan = 0;

void setup() {
    // put your setup code here, to run once:
    SoftPWM.begin(490);
    Serial.begin(9600);
    u8g2.begin();
    pinMode(SOILHUMI, INPUT);
}

void loop() {
    // put your main code here, to run repeatedly:
    Solihumi = map(analogRead(SOILHUMI),0,1023,100,0);

    if(Solihumi >= 30)
    {
        fan = 100;
        SoftPWM.set(fan);
    }
    else if(Solihumi <= 25)
    {
        fan = 0;
        SoftPWM.set(fan);
    }
    else
        fan = 65;
        SoftPWM.set(fan);

    OLEDdraw();
    Serial.print("현재 토양 습도 : ");
    Serial.println(Solihumi);
}

void OLEDdraw() {
  u8g2.clearBuffer();
  u8g2.setFont(u8g2_font_ncenB08_te);

  u8g2.drawStr(1,15,"SMART FARM");
  
  u8g2.drawStr(15,36, "SoilHumi.");
  u8g2.setCursor(85,35);
  u8g2.print(Solihumi);

  u8g2.drawStr(15,46, "FAN.");
  u8g2.setCursor(85,45);
  u8g2.print(fan);
  u8g2.drawStr(119, 36, "%");

  u8g2.sendBuffer();
}

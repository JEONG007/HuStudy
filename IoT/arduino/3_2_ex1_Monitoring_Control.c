/*장치 자동 제어
1) 장치 자동 제어를 ON/OFF 토글 스위치로 입력받는다.
2) 앞서 작성했던, 온도에 따른 DC FAN 제어와 토양 습도 조건에 따른 
   DC PUMP 제어를실행/중지시키는 프로젝트를 작성*/

#include "DHT.h"
#include <VitconBrokerComm.h>
#include <SoftPWM.h>
using namespace vitcon;

#define DHTPIN A1
#define DHTTYPE DHT22
#define SOILHUMI A6
#define PUMP 16

SOFTPWM_DEFINE_CHANNEL(A3);
DHT dht(DHTPIN, DHTTYPE);

bool fan_out_status;
bool pump_out_status;

uint32_t HdtDelay = 2000;
uint32_t Hdt_ST = 0;

int Soilhumi = 0;
float Temp;
float Humi;


void fan_out(bool val) {
    fan_out_status = val;
}

void pump_out(bool val) {
    pump_out_status = val;
}

IOTItemBin FanStatus;
IOTItemBin Fan(fan_out);
IOTItemBin PumpStatus;
IOTItemBin Pump(pump_out);

#define ITEM_COUNT 4

IOTItem *items[ITEM_COUNT] = { &FanStatus, &Fan, &PumpStatus, &Pump };

const char device_id[] = "9686d6afa72f624e63215dea77771517";
BrokerComm comm(&Serial, device_id, items, ITEM_COUNT);

void setup() {
    Serial.begin(250000);
    comm.SetInterval(200);
    dht.begin();

    SoftPWM.begin(490);
    pinMode(PUMP, OUTPUT);
    pinMode(SOILHUMI, INPUT);
    Hdt_ST = millis();
}

void loop() {
    
    if((millis()-Hdt_ST) > HdtDelay) {
        Soilhumi = map(analogRead(SOILHUMI),0,1023,100,0);
        Humi = dht.readHumidity();
        Temp = dht.readTemperature();
        Serial.println(Soilhumi);

        if(isnan(Humi) || isnan(Temp)) {
        Serial.println(F("Failed to read from DHT sensor!"));
        return;
        }
        Hdt_ST = millis();
    }
//    Serial.println(Soilhumi);

//    if(fan_out_status == true) SoftPWM.set(100);
//    else SoftPWM.set(0);

    if(fan_out_status == 1)
    {
        if(Temp >= 29)
        {
            SoftPWM.set(100);
        }
        else if(Temp <= 20)
        {
            SoftPWM.set(0);
        }
        else
        {
            SoftPWM.set(65);
        }
    }
    else
    {
        SoftPWM.set(0);
    }

    Serial.println(pump_out_status);
    if(pump_out_status == 1)
    {
        if(Soilhumi <= 20)
        {
            digitalWrite(PUMP,HIGH);
        }
        else if(Soilhumi >= 30)
        {
            digitalWrite(PUMP,LOW);
        }
    }
    else
    {
        digitalWrite(PUMP,LOW);
    }
    // digitalWrite(PUMP, pump_out_status);

    FanStatus.Set(fan_out_status);
    PumpStatus.Set(digitalRead(PUMP));
    comm.Run();
}
/*1) 새 프로젝트를 생성하여 모니터링과 제어가 동시에 가능한 위젯 구성*/

#include "DHT.h"
#include <VitconBrokerComm.h>
#include <SoftPWM.h>
using namespace vitcon;

#define DHTPIN A1
#define DHTTYPE DHT22
#define SOILHUMI A6

DHT dht(DHTPIN, DHTTYPE);

uint32_t DataCaptureDelay = 2000;
uint32_t DataCapture_ST = 0;

#define LAMP 17
#define PUMP 16
SOFTPWM_DEFINE_CHANNEL(A3);

bool fan_out_status;
bool pump_out_status;
bool lamp_out_status;

float Temp;
float Humi;
int fan;
int Soilhumi = 0;

IOTItemFlo dht22_temp;
IOTItemFlo dht22_humi;
IOTItemInt soilhumi;

void fan_out(bool val)
{
    fan_out_status = val;
}

void pump_out(bool val)
{
    pump_out_status = val;
}

void lamp_out(bool val)
{
    lamp_out_status = val;
}

IOTItemBin FanStatus;
IOTItemBin Fan(fan_out);
IOTItemBin PumpStatus;
IOTItemBin Pump(pump_out);
#define ITEM_COUNT 7
IOTItem *items[ITEM_COUNT] = {&PumpStatus, &Pump, &FanStatus, &Fan, &dht22_temp, &dht22_humi, &soilhumi};

const char device_id[] = "10ddcb4f6e09bab8eccbec25c75da4c2";
BrokerComm comm(&Serial, device_id, items, ITEM_COUNT);

// dht22_temp.Set(Temp);
// soil_Humi.Set(soilhumi);

void setup()
{
    // put your setup code here, to run once:
    Serial.begin(250000);
    comm.SetInterval(200);

    dht.begin();
    pinMode(SOILHUMI, INPUT);
    DataCapture_ST = millis();
    SoftPWM.begin(490);
    pinMode(PUMP, OUTPUT);
}

void loop()
{
    // put your main code here, to run repeatedly:

    if ((millis() - DataCapture_ST) > DataCaptureDelay)
    {
        Soilhumi = map(analogRead(SOILHUMI), 0, 1023, 100, 0);
        Humi = dht.readHumidity();
        Temp = dht.readTemperature();

        DataCapture_ST = millis();

        dht22_temp.Set(Temp);
        dht22_humi.Set(Humi);
        soilhumi.Set(Soilhumi);
    }

    if (fan_out_status == true)
    {
        if (Temp >= 30)
        {
            fan = 100;
            SoftPWM.set(fan);
        }
        else if (Temp <= 25)
        {
            fan = 0;
            SoftPWM.set(fan);
        }
        else if (Temp < 30 && Temp > 25)
        {
            fan = 65;
            SoftPWM.set(fan);
        }
    }
    else
    {
        SoftPWM.set(0);
    }

    if (pump_out_status == true)
    {
        if (Soilhumi <= 20)
        {
            digitalWrite(PUMP, HIGH);
        }
        else if (Soilhumi >= 30)
        {
            digitalWrite(PUMP, LOW);
        }
    }
    else
    {
        digitalWrite(PUMP, LOW);
    }

    FanStatus.Set(fan_out_status);
    PumpStatus.Set(digitalRead(PUMP));

    dht22_temp.Set(Temp);
    dht22_humi.Set(Humi);
    soilhumi.Set(Soilhumi);
    comm.Run();
}
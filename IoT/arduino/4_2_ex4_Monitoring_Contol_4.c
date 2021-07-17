/*수동/자동 제어 위젯에 따른 장치 컨트롤 구현*/

#include <VitconBrokerComm.h>
#include <SoftPWM.h>
using namespace vitcon;

#define SOILHUMI A6
#define PUMP 16
#define LAMP 17

SOFTPWM_DEFINE_CHANNEL(A3);

/*변수*/
bool autoset = false;
bool timerset = false;

bool fanset = false;
bool pumpset = false;
bool ledset = false;

int Solihumi = 0;


/*iot 제어*/
void t_auto(bool val)
{
    autoset = val;
}
void timer(bool val)
{
    timerset = val;
}
void fan(bool val)
{
    fanset = val;
}
void pump(bool val)
{
    pumpset = val;
}
void led(bool val)
{
    ledset = val;
}


IOTItemBin AutoStatus; // 1. 수동/자동
IOTItemBin Auto(t_auto);

IOTItemBin TimerStatus; // 2. 타이머 on/off
IOTItemBin Timer(timer);

IOTItemBin FanStatus; // 6. 펜 on/off
IOTItemBin Fan(fan);
IOTItemBin PumpStatus; // 7. 펌프 on/off
IOTItemBin Pump(pump);
IOTItemBin LedStatus; // 8. 조명 on/off
IOTItemBin Led(led);

#define ITEM_COUNT 10
IOTItem *items[ITEM_COUNT] = {&AutoStatus, &Auto, &TimerStatus, &Timer,
    &FanStatus, &Fan, &PumpStatus, &Pump, &LedStatus, &Led};

const char device_id[] = "6db31da9097e20dabfc55a63061b902d";
BrokerComm comm (&Serial, device_id, items, ITEM_COUNT);


void setup() {
    // put your setup code here, to run once:
    Serial.begin(250000);
    comm.SetInterval(200);

    SoftPWM.begin(490);
    pinMode(PUMP,OUTPUT);
    pinMode(LAMP, OUTPUT);
    // pinMode(SOILHUMI, INPUT);
}

void loop() {
    // put your main code here, to run repeatedly:
    // Solihumi = map(analogRead(SOILHUMI),0,1023,100,0);

    if(autoset)
    {
        //모든 장치 자동
        if(fanset) //fan
            SoftPWM.set(100);
        else
            SoftPWM.set(0);

        if(pumpset) //pump
            digitalWrite(PUMP,HIGH);
        else
            digitalWrite(PUMP,LOW);

        if(ledset) //led
            digitalWrite(LAMP,HIGH);
        else
            digitalWrite(LAMP,LOW);
    }
    else
    {
        //모든 장치 수동
        SoftPWM.set(0); //fan
        digitalWrite(PUMP,LOW); //pump
        digitalWrite(LAMP,LOW); //led
    }

}
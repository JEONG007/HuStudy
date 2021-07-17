/*FAN Remote Control
1) FAN ON/OFF 토글 스위치로 입력받는다.
2) 트랙바로 세기를 입력받고 프로그래스 바로 입력된 세기를 출력한다.
3) 타이머 기반 LED 조명 제어와 마찬가지로 시간 조절 기능을 추가한다. 
(LED와 달리 동작을 먼저 수행하고, 정해놓은 시간이 지나면 꺼지는 형태로 제작한다.)
4) 세기는 60 ~ 100으로 제한을 둔다.
*/

#include <SoftPWM.h>
#include <VitconBrokerComm.h>
using namespace vitcon;

SOFTPWM_DEFINE_CHANNEL(A3);

bool fanset = false;
bool timeset = false;
int32_t Track_Power_status = 60;
bool Interval_Sup_status;
bool Interval_Mup_status;

int Minute = 0;
int Second = 1;

uint32_t TimeSum = 0;
uint32_t TimeCompare;
uint32_t TimePushDelay = 0;
uint32_t TimerStartTime = 0;

void fan(bool val)
{
    fanset = val;
}

void timeset_out(bool val)
{
    timeset = val;
}

void Track_Power(int32_t val)
{
    Track_Power_status = val;
}

void Interval_Mup(bool val)
{
    Interval_Mup_status = val;   
}

void Interval_Sup(bool val)
{
    Interval_Sup_status = val;
}

void IntervalReset(bool val)
{
    if (!timeset && val)
    {
        Minute = 0;
        Second = 1;
    }
}

IOTItemBin FanStatus;
IOTItemBin Fan(fan);

IOTItemInt PowerStatus;
IOTItemInt TrackPower(Track_Power);

IOTItemBin StopStatus;
IOTItemBin Stop(timeset_out);

IOTItemBin IntervalMUP(Interval_Mup);
IOTItemBin IntervalSUP(Interval_Sup);
IOTItemBin IntervalRST(IntervalReset);

IOTItemInt label_Minterval;
IOTItemInt label_Sinterval;

#define ITEM_COUNT 11

IOTItem *items[ITEM_COUNT] = {&FanStatus, &Fan, &PowerStatus,
    &TrackPower, &StopStatus, &Stop, &IntervalMUP,
    &IntervalSUP, &IntervalRST, &label_Minterval, &label_Sinterval};

const char device_id[] = "ea49df30051d4b421117cdf8a5bb0b83";
BrokerComm comm (&Serial, device_id, items, ITEM_COUNT);



void setup() {
    Serial.begin(250000);
    comm.SetInterval(200);

    SoftPWM.begin(490);
    SoftPWM.set(0);
}
void loop() {
    // InvervalSet(fanset);
    InvervalSet(timeset);

    if(fanset)
    {
        if(TimeCompare % 2 ==0)
        {
            SoftPWM.set(Track_Power_status);
        }
        else if (TimeCompare % 2 ==1)
        {
            SoftPWM.set(0);
        }
    }
    else
    {
        SoftPWM.set(0);
    }

    FanStatus.Set(fanset);
    StopStatus.Set(timeset);
    PowerStatus.Set(Track_Power_status);
    label_Minterval.Set(Minute);
    label_Sinterval.Set(Second);
    comm.Run();
}

void InvervalSet(bool timeset) {
    if(!timeset) {
        TimeSum =(uint32_t)(Minute * 60 + Second) * 1000;
        TimerStartTime = millis();

        if(millis() > TimePushDelay + 500) {
            Minute += Interval_Mup_status;
            if(Minute >= 60) Minute = 0;
            Second += Interval_Sup_status;
            if(Second >= 60) Second = 0;

            TimePushDelay = millis();
        }
    }
    else if(timeset) {
        TimeCompare = (millis() - TimerStartTime) /TimeSum;
    }
}
#include "DHT.h"
#include <SoftPWM.h>
#include <VitconBrokerComm.h>
using namespace vitcon;

SOFTPWM_DEFINE_CHANNEL(A3);

#define DHTPIN A1
#define DHTTYPE DHT22
#define SOILHUMI A6
#define PUMP 16
#define LAMP 17

DHT dht(DHTPIN, DHTTYPE);

#include <U8g2lib.h>
U8G2_SH1106_128X64_NONAME_F_HW_I2C u8g2(U8G2_R0, /* reset=*/ U8X8_PIN_NONE);

/*변수*/
float Temp;
float Humi;
int Soilhumi = 0;

bool fan_auto_set = false;
bool pump_auto_set = false;
bool led_auto_set = false;

bool fan_set = false;
bool fan_push_status = false;//fan off
int32_t track_fan_time_status = 1;
int32_t track_fan_start_temp = 0;//fan on
int32_t track_fan_start_temp2 = 0;
bool push_fan_power_up = false;
bool push_fan_power_up2 = false;
bool push_fan_power_reset = false;
int fan_power = 60;
int fan_power2 = 60;

bool pump_set = false;
bool pump_push_status = false; //pump off
int32_t track_pump_time_status = 1;
int32_t track_pump_start_humi = 0;//pump on
int32_t track_pump_end_humi = 0;
bool pump_interval_time_set = false;
bool push_pump_interval_time_up = false;
int pump_interval_time = 1;

bool led_set = false;
bool led_push_status = false;
int32_t track_led_time_status = 1;

bool push_hour_up = false;
bool push_minute_up = false;
bool push_second_up = false;
bool push_set_time = false;
bool push_reset_time = false;
bool push_hour_down = false;
bool push_minute_down = false;
bool push_second_down = false;

/*시간 변수*/
uint32_t FanTimeSum = 1; //fan off
uint32_t FanTimeCompare = 1;
uint32_t FanTimerStartTime;
uint32_t FanTimePushDelay = 0;
uint32_t FanPowerPushDelay = 0;//fan on

uint32_t PumpTimeSum = 1; //pump off
uint32_t PumpTimeCompare = 1;
uint32_t PumpTimerStartTime;
uint32_t PumpTimePushDelay = 0;
uint32_t PumpIntervalTimePushDelay = 0; //pump on
uint32_t PumpIntervalTimeSum = 1;
uint32_t PumpIntervalTimeCompare = 1;
uint32_t PumpIntervalTimerStartTime;

uint32_t LedTimeSumAuto = 0;
uint32_t LedTimeCompareAuto = 0;
uint32_t LedTimeSum = 1;
uint32_t LedTimeCompare = 1;
uint32_t LedTimerStartTime;
uint32_t LedTimerStartTimeAuto;
uint32_t LedTimePushDelay = 0;
int LedTimeHour = 0;
int LedTimeMinute = 0;
int LedTimeSecond = 0;

uint32_t DataCaptureDelay = 2000;
uint32_t DataCapture_ST = 0;

/*제어*/
// bool prev_fan_auto_set = false;
bool prev_fan_push_status = false;
bool prev_pump_push_status = false;
bool prev_led_push_status = false;

void Fan_Auto(bool val)
{
    fan_auto_set = val;
}
void Pump_Auto(bool val)
{
    pump_auto_set = val;
}
void Led_Auto(bool val)
{
    led_auto_set = val;
}
void Fan_Push(bool val)
{
    // if(prev_fan_push_status == false && val == true)
    //     fan_push_status = val;
    // prev_fan_push_status = val;
    fan_push_status = val;
}
void Track_Fan_Time(int32_t val)
{
    track_fan_time_status = val;
}
void Pump_Push(bool val)
{
    pump_push_status = val;
}
void Track_Pump_Time(int32_t val)
{
    track_pump_time_status = val;
}
void Led_Push(bool val)
{
    led_push_status = val;
}
void Track_Led_Time(int32_t val)
{
    track_led_time_status = val;
}


void Track_Fan_Start_Temp(int32_t val)
{
    track_fan_start_temp = val;
}
void Track_Fan_Start_Temp2(int32_t val)
{
    track_fan_start_temp2 = val;
}
void Push_Fan_Power_Up(bool val)
{
    push_fan_power_up = val;
}
void Push_Fan_Power_Up2(bool val)
{
    push_fan_power_up2 = val;
}
void Push_Fan_Power_Reset(bool val)
{
    push_fan_power_reset = val;
}
void Track_Pump_Start_Humi(int32_t val)
{
    track_pump_start_humi = val;
}
void Track_Pump_End_Humi(int32_t val)
{
    track_pump_end_humi = val;
}
void Pump_Interval_Time_Set(bool val)
{
    pump_interval_time_set = val;
}
void Push_Pump_Interval_Time_Up(bool val)
{
    push_pump_interval_time_up = val;
}
void Push_Hour_Up(bool val)
{
    push_hour_up = val;
}

void Push_Minute_Up(bool val)
{
    push_minute_up = val;
}

void Push_Second_Up(bool val)
{
    push_second_up = val;
}

void Push_Set_Time(bool val)
{
    push_set_time = val;
}

void Push_Reset_Time(bool val)
{
    push_reset_time = val;
}

void Push_Hour_Down(bool val)
{
    push_hour_down = val;
}

void Push_Minute_Down(bool val)
{
    push_minute_down = val;
}

void Push_Second_Down(bool val)
{
    push_second_down = val;
}

IOTItemFlo dht22_temp; //내부 온도
IOTItemFlo dht22_humi; //내부 습도
IOTItemInt soilhumi; //토양 습도

IOTItemBin FanAutoStatus; // Fan auto on/off
IOTItemBin FanAuto(Fan_Auto);
IOTItemBin PumpAutoStatus; // Pump auto on/off
IOTItemBin PumpAuto(Pump_Auto);
IOTItemBin LedAutoStatus; // LED auto on/off
IOTItemBin LedAuto(Led_Auto);

IOTItemBin FanStatus; //Fan auto off
IOTItemBin FanPush(Fan_Push);
IOTItemInt FanTimeStatus;
IOTItemInt TrackFanTime(Track_Fan_Time);

IOTItemBin PumpStatus; //Pump auto off
IOTItemBin PumpPush(Pump_Push);
IOTItemInt PumpTimeStatus;
IOTItemInt TrackPumpTime(Track_Pump_Time);

IOTItemBin LedStatus; //LED auto off
IOTItemBin LedPush(Led_Push);
IOTItemInt LedTimeStatus;
IOTItemInt TrackLedTime(Track_Led_Time);

IOTItemInt FanStartTempStatus;//Fan auto on
IOTItemInt TrackFanStartTemp(Track_Fan_Start_Temp);
IOTItemInt FanStartTempStatus2;
IOTItemInt TrackFanStartTemp2(Track_Fan_Start_Temp2);
IOTItemFlo LabelFanPower;
IOTItemFlo LabelFanPower2;
IOTItemBin PushFanPowerUp(Push_Fan_Power_Up);
IOTItemBin PushFanPowerUp2(Push_Fan_Power_Up2);
IOTItemBin PushFanPowerReset(Push_Fan_Power_Reset);

IOTItemInt PumpStartHumiStatus;//Pump auto on
IOTItemInt TrackPumpStartHumi(Track_Pump_Start_Humi);
IOTItemInt PumpEndHumiStatus;
IOTItemInt TrackPumpEndtHumi(Track_Pump_End_Humi);
IOTItemBin PushPumpIntervalTimeUp(Push_Pump_Interval_Time_Up);
IOTItemFlo LabelPumpIntervalTime;
IOTItemBin PumpIntervalTimeStatus;
IOTItemBin PumpIntervalTimeSet(Pump_Interval_Time_Set);

IOTItemInt LabelTimeHour; //LED 관련 부분
IOTItemInt LabelMinuteHour;
IOTItemInt LabelSecondHour;
IOTItemBin PushHourUp(Push_Hour_Up);
IOTItemBin PushMinuteUp(Push_Minute_Up);
IOTItemBin PushSecondUp(Push_Second_Up);
IOTItemBin PushSetTime(Push_Set_Time);
IOTItemBin PushResetTime(Push_Reset_Time);
IOTItemBin PushHourDown(Push_Hour_Down);
IOTItemBin PushMinuteDown(Push_Minute_Down);
IOTItemBin PushSecondDown(Push_Second_Down);


#define ITEM_COUNT 49
IOTItem *items[ITEM_COUNT] = {&dht22_temp, &dht22_humi, &soilhumi,
    &FanAutoStatus, &FanAuto, &PumpAutoStatus, &PumpAuto, &LedAutoStatus, &LedAuto,
    &FanStatus, &FanPush, &FanTimeStatus, &TrackFanTime,
    &PumpStatus, &PumpPush, &PumpTimeStatus, &TrackPumpTime,
    &LedStatus, &LedPush, &LedTimeStatus, &TrackLedTime,
    &FanStartTempStatus, &TrackFanStartTemp, &FanStartTempStatus2, &TrackFanStartTemp2, &LabelFanPower, &LabelFanPower2, &PushFanPowerUp, &PushFanPowerUp2, &PushFanPowerReset,
    &PumpStartHumiStatus, &TrackPumpStartHumi, &PumpEndHumiStatus, &TrackPumpEndtHumi, &PushPumpIntervalTimeUp, &LabelPumpIntervalTime, &PumpIntervalTimeStatus, &PumpIntervalTimeSet,
    &LabelTimeHour, &LabelMinuteHour, &LabelSecondHour, &PushHourUp, &PushMinuteUp, &PushSecondUp, &PushSetTime, &PushResetTime, &PushHourDown, &PushMinuteDown, &PushSecondDown
    };


const char device_id[ ] = "5018c0497b239de6848e87d10036f380";
BrokerComm comm(&Serial, device_id, items, ITEM_COUNT);


void setup() {
  // put your setup code here, to run once:
    Serial.begin(250000);
    SoftPWM.begin(490);
    dht.begin();
    comm.SetInterval(200);
    
    pinMode(SOILHUMI,INPUT);
    pinMode(PUMP,OUTPUT);
    pinMode(LAMP, OUTPUT);

    // u8g2.begin();
    LabelFanPower.Set(fan_power);
    LabelFanPower2.Set(fan_power2);
    LabelPumpIntervalTime.Set(pump_interval_time);
}

void loop() {
    // put your main code here, to run repeatedly:
    if((millis()-DataCapture_ST) > DataCaptureDelay)
    {
        Humi = dht.readHumidity();
        Temp = dht.readTemperature();
        Soilhumi = map(analogRead(SOILHUMI),0,1023,100,0);

        dht22_temp.Set(Temp);
        dht22_humi.Set(Humi);
        soilhumi.Set(Soilhumi);

        DataCapture_ST = millis();
    }

    // OLEDdraw();
    

    if(!fan_auto_set)//fan auto off
    {
        if(fan_push_status)
        {
            FanTimeSet();
        }
        FanTimeCompare = (millis() - FanTimerStartTime) /FanTimeSum;
        if(FanTimeCompare >= 1)// || FanTimeCompare == 0
        {
            SoftPWM.set(0);
            FanStatus.Set(false);
        }
        else
        {
            SoftPWM.set(65);
            FanStatus.Set(true);
        }
    }
    else//fan auto on
    {
        FanPowerSet();
        if(Temp >= track_fan_start_temp2)
        {
            SoftPWM.set(fan_power2);
            FanStatus.Set(fan_power2);
        }
        else if(Temp >= track_fan_start_temp)
        {
            SoftPWM.set(fan_power);
            FanStatus.Set(fan_power);
        }
        else
        {
            SoftPWM.set(0);
            FanStatus.Set(false);
        }

        FanStartTempStatus.Set(track_fan_start_temp);
        FanStartTempStatus2.Set(track_fan_start_temp2);
    }
    
    FanAutoStatus.Set(fan_auto_set);
    FanTimeStatus.Set(track_fan_time_status);

    // digitalWrite(PUMP,HIGH);
    if(!pump_auto_set)//pump auto off
    {
        if(pump_push_status)
        {
            PumpTimeSet();
        }
        PumpTimeCompare = (millis() - PumpTimerStartTime) /PumpTimeSum;
        if(PumpTimeCompare >= 1)// || FanTimeCompare == 0
        {
            digitalWrite(PUMP,LOW);
            PumpStatus.Set(false);
        }
        else
        {
            digitalWrite(PUMP,HIGH);
            PumpStatus.Set(true);
        }
    }
    else //pump auto on
    {
        if(Soilhumi >= track_pump_start_humi && Soilhumi <= track_pump_end_humi)
        {
            if(pump_interval_time_set)
            {
                PumpIntervalTimeUp();
                PumpIntervalTimeCompare = (millis() - PumpIntervalTimerStartTime) / PumpIntervalTimeSum;
                // Serial.println(PumpIntervalTimeCompare);
                if(PumpIntervalTimeCompare % 2 == 0)
                {
                    // digitalWrite(LAMP,HIGH);
                    digitalWrite(PUMP, HIGH);
                    PumpStatus.Set(true);
                }
                else if (PumpIntervalTimeCompare % 2 == 1)
                {
                    // digitalWrite(LAMP,LOW);
                    digitalWrite(PUMP, LOW);
                    PumpStatus.Set(false);
                }
            }
            else
            {
                digitalWrite(PUMP,HIGH);
                PumpStatus.Set(true);
            }
        }
        else
        {
            digitalWrite(PUMP,LOW);
            PumpStatus.Set(false);
        }
    }
    
    PumpAutoStatus.Set(pump_auto_set);
    PumpTimeStatus.Set(track_pump_time_status);

    if(!led_auto_set)//led auto off
    {
        if(led_push_status)
        {
            LedTimeSet();
        }
        LedTimeCompare = (millis() - LedTimerStartTime) /LedTimeSum;
        if(LedTimeCompare >= 1)// || FanTimeCompare == 0
        {
            digitalWrite(LAMP,LOW);
            LedStatus.Set(false);
        }
        else
        {
            digitalWrite(LAMP,HIGH);
            LedStatus.Set(true);
        }
    }
    else//led auto on
    {
        LEDTimeAutoSet();
        LedTimeCompareAuto = (millis() - LedTimerStartTimeAuto) /LedTimeSumAuto;
        if(LedTimeSumAuto == 0)
        {
            digitalWrite(LAMP, HIGH);
            LedStatus.Set(true);
        }
        else if(LedTimeCompareAuto % 2 == 0)
        {
            digitalWrite(LAMP, HIGH);
            LedStatus.Set(true);
        }
        else if (LedTimeCompareAuto % 2 == 1)
        {
            digitalWrite(LAMP, LOW);
            LedStatus.Set(false);
        }
    }
    
    LedAutoStatus.Set(led_auto_set);
    LedTimeStatus.Set(track_led_time_status);

    comm.Run();
}

void FanTimeSet() {
    if(millis() > FanTimePushDelay + 500) 
    {
        FanTimeSum =(uint32_t)track_fan_time_status * 1000;
        FanTimerStartTime = millis();
        FanTimePushDelay = millis();
    }
}
void PumpTimeSet() {
    if(millis() > PumpTimePushDelay + 500) 
    {
        PumpTimeSum =(uint32_t)track_pump_time_status * 1000;
        PumpTimerStartTime = millis();
        PumpTimePushDelay = millis();
    }
}
void LedTimeSet() {
    if(millis() > LedTimePushDelay + 500) 
    {
        LedTimeSum =(uint32_t)track_led_time_status * 1000;
        LedTimerStartTime = millis();
        LedTimePushDelay = millis();
    }
}
void FanPowerSet() {
    if(millis() > FanPowerPushDelay + 500) 
    {
        if(fan_power < 100)
            fan_power += push_fan_power_up*10;
        if(fan_power2 < 100)
            fan_power2 += push_fan_power_up2*10;

        if(push_fan_power_reset)
        {
            fan_power = 60;
            fan_power2 = 60;
        }
        FanPowerPushDelay = millis();
    }
    LabelFanPower.Set(fan_power);
    LabelFanPower2.Set(fan_power2);
}
void PumpIntervalTimeUp() {
    if(millis() > PumpIntervalTimePushDelay + 500) 
    {
        if(push_pump_interval_time_up)
        {
            pump_interval_time += 1;
            PumpIntervalTimeSum = (uint32_t)pump_interval_time * 1000;
            PumpIntervalTimerStartTime = millis();
        }
        PumpIntervalTimePushDelay = millis();
    }
    LabelPumpIntervalTime.Set(pump_interval_time);
}
void LEDTimeAutoSet()
{
    if (millis() > LedTimePushDelay + 500)
    {
        if(push_hour_up)
        {
            LedTimeHour += 1;
            if(LedTimeHour > 23) LedTimeHour = 0;
        }
        
        if(push_minute_up)
        {
            LedTimeMinute += 1;
            if(LedTimeMinute > 59) LedTimeMinute = 0;
        }

        if(push_second_up)
        {
            LedTimeSecond += 1;
            if (LedTimeSecond > 59) LedTimeSecond = 0;
        }
        if(push_hour_down)
        {
            if(LedTimeHour > 0) LedTimeHour -= 1;
        }
        
        if(push_minute_down)
        {
            if(LedTimeMinute > 0) LedTimeMinute -= 1;
        }

        if(push_second_down)
        {
            
            if (LedTimeSecond > 0) LedTimeSecond -= 1;
        }

        if (push_set_time)
        { 
            
            LedTimeSumAuto = (uint32_t)(LedTimeHour * 3600 + LedTimeMinute * 60 + LedTimeSecond) * 1000; 
            LedTimerStartTimeAuto = millis();
        }

        if (push_reset_time)
        {
            LedTimeHour = 0;
            LedTimeMinute = 0;
            LedTimeSecond = 0;
            LedTimeSumAuto = (uint32_t)(LedTimeHour * 3600 + LedTimeMinute * 60 + LedTimeSecond) * 1000; 
        }
        LedTimePushDelay = millis();
    }
    LabelTimeHour.Set(LedTimeHour);
    LabelMinuteHour.Set(LedTimeMinute);
    LabelSecondHour.Set(LedTimeSecond);  
}
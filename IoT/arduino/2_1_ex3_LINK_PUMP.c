/*토양 습도 조건에 따른 DC PUMP 제어
1) SOIL-LINK에서 토양 습도 측정
2) 토양 습도가 30 이하일 때 DC PUMP 동작
3) 토양 습도가 60 이상일 때 DC PUMP OFF*/

#define SOILHUMI A6
#define PUMP 16

int Solihumi = 0;

void setup() {
  // put your setup code here, to run once:
    Serial.begin(9600);
    pinMode(PUMP,OUTPUT);
    pinMode(SOILHUMI, INPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
    Solihumi = map(analogRead(SOILHUMI),0,1023,100,0);

    Serial.println(Solihumi);

    if(Solihumi <= 20)
    {
        digitalWrite(PUMP,HIGH);
    }
    else if(Solihumi >= 30)
    {
        digitalWrite(PUMP,LOW);
    }
}
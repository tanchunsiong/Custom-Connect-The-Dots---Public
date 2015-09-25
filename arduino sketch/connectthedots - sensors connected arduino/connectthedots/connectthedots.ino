#include <dht11.h>
#include <EEPROM.h>
#define MYSERIAL Serial
#define dht_dpin A1 //no ; here. Set equal to channel sensor is on
dht11 DHT;

int ledPinRed =6;
int ledPinGreen=8;


const int LightSensorPin = A0;  // Analog input pin that the potentiometer is attached to
float lightsensorValue = 0; 

const int pirPin = 2;    //the digital pin connected to the PIR sensor's output
float motionvalue=0;




char GUID1[37];
char GUID2[37];
char GUID3[37];
char GUID4[37];
char Org[] = "Microsoft Singapore DX Team";
char Disp[] = "Arduino + Raspiberry Pi 2 on Windows";
char Locn[] = "SG MIC";
char Measure1[] = "temperature";
char Units1[] = "C";
char Measure2[] = "humidity";
char Units2[] = "%";
char Measure3[] = "light";
char Units3[] = "lumen";
char Measure4[] = "motion";
char Units4[] = "binary";
char buffer[300];
char dtostrfbuffer[15];

long unitId;



void setup(){
   Serial.begin(9600);

   delay(1000);//Wait rest of 1000ms recommended delay before
   pinMode(ledPinRed, OUTPUT);
   pinMode(ledPinGreen, OUTPUT);
   String guid=generateGuid();
   guid.toCharArray(GUID1, 37);
    guid=generateGuid();
   guid.toCharArray(GUID2, 37);
    guid=generateGuid();
   guid.toCharArray(GUID3, 37);
    guid=generateGuid();
   guid.toCharArray(GUID4, 37);
   
}//end "setup()"

String generateGuid(){
   String firstpart=generate8();
   while (firstpart.length() <8){
       firstpart=generate8();
   }
   
   String secondtemppart=generate8();
   String secondpart=secondtemppart.substring(0,4);
   String thirdpart=secondtemppart.substring(3,7);
   
   String fourthtemppart=generate8();
   String fourthpart=fourthtemppart.substring(0,4);
   
   String fifthtemppart=generate8();
     while (fifthtemppart.length() <8){
       fifthtemppart=generate8();
   }
    String fifthtemppart2=fourthtemppart.substring(3,7);
    String fifthpart=fifthtemppart + fifthtemppart2;
    


return (firstpart+"-"+secondpart+"-"+thirdpart+"-"+fourthpart+"-"+fifthpart);

}

String generate8(){
 long notunitId;


 unitId = (long)EEPROM.read(0) << 24 | (long)EEPROM.read(1) << 16 | (long)EEPROM.read(2) << 8 | (long)EEPROM.read(3);
  notunitId = (long)EEPROM.read(4) << 24 | (long)EEPROM.read(5) << 16 | (long)EEPROM.read(6) << 8 | (long)EEPROM.read(7);


    unitId = notunitId = 4711;
  if (unitId == -notunitId) {
    
    return String(unitId, HEX);
  } else {
    randomSeed(analogRead(7)*analogRead(6)*analogRead(5)+micros());
    unitId = random();
    notunitId = -unitId;
    EEPROM.write(0, unitId >> 24 & 0xFF);
    EEPROM.write(1, unitId >> 16 & 0xFF);
    EEPROM.write(2, unitId >> 8  & 0xFF);
    EEPROM.write(3, unitId     & 0xFF);
    EEPROM.write(4, notunitId >> 24 & 0xFF);
    EEPROM.write(5, notunitId >> 16 & 0xFF);
    EEPROM.write(6, notunitId >> 8  & 0xFF);
    EEPROM.write(7, notunitId     & 0xFF);
    return String(unitId, HEX);
  }
}



float get_light_level()
{

  float lightSensor = analogRead(LightSensorPin);
  lightSensor = 1/lightSensor *1500;
  return(lightSensor);
}

void loop(){
  //This is the "heart" of the program.
   DHT.read(dht_dpin);
   lightsensorValue =get_light_level();  
   motionvalue=digitalRead(pirPin);

  float temperatureC =DHT.temperature;
float humdity=DHT.humidity;

       
  memset(buffer,'\0',sizeof(buffer));
  strcat(buffer,"{");
  strcat(buffer,"\"guid\":\"");
  strcat(buffer,GUID1);
  strcat(buffer,"\",\"organization\":\"");
  strcat(buffer,Org);
  strcat(buffer,"\",\"timecreated\":\"");
  strcat(buffer,"timenow");
  strcat(buffer,"\",\"displayname\":\"");
  strcat(buffer,Disp);
  strcat(buffer,"\",\"location\":\"");
  strcat(buffer,Locn);  
  strcat(buffer,"\",\"measurename\":\"");
  strcat(buffer,Measure1);
  strcat(buffer,"\",\"unitofmeasure\":\"");
  strcat(buffer,Units1);
  strcat(buffer,"\",\"value\":");
  strcat(buffer,dtostrf(temperatureC,5,2,dtostrfbuffer));
  strcat(buffer,"}");
 Serial.println(buffer);
delay(100);
  // print string for humidity, separated by line for ease of reading
  memset(buffer,'\0',sizeof(buffer));
  strcat(buffer,"{");
  strcat(buffer,"\"guid\":\"");
  strcat(buffer,GUID2);
  strcat(buffer,"\",\"organization\":\"");
  strcat(buffer,Org);
  strcat(buffer,"\",\"timecreated\":\"");
  strcat(buffer,"timenow");
  strcat(buffer,"\",\"displayname\":\"");
  strcat(buffer,Disp);
  strcat(buffer,"\",\"location\":\"");
  strcat(buffer,Locn);  
  strcat(buffer,"\",\"measurename\":\"");
  strcat(buffer,Measure2);
  strcat(buffer,"\",\"unitofmeasure\":\"");
  strcat(buffer,Units2);
  strcat(buffer,"\",\"value\":");
  strcat(buffer,dtostrf(humdity,5,2,dtostrfbuffer));
  strcat(buffer,"}");
 Serial.println(buffer);
delay(100);
  // print string for light, separated by line for ease of reading
  memset(buffer,'\0',sizeof(buffer));
  strcat(buffer,"{");
  strcat(buffer,"\"guid\":\"");
  strcat(buffer,GUID3);
  strcat(buffer,"\",\"organization\":\"");
  strcat(buffer,Org);
  strcat(buffer,"\",\"timecreated\":\"");
  strcat(buffer,"timenow");
  strcat(buffer,"\",\"displayname\":\"");
  strcat(buffer,Disp);
  strcat(buffer,"\",\"location\":\"");
  strcat(buffer,Locn);  
  strcat(buffer,"\",\"measurename\":\"");
  strcat(buffer,Measure3);
  strcat(buffer,"\",\"unitofmeasure\":\"");
  strcat(buffer,Units3);
  strcat(buffer,"\",\"value\":");
  strcat(buffer,dtostrf(lightsensorValue,5,3,dtostrfbuffer));
  strcat(buffer,"}");
 Serial.println(buffer);
delay(100);
 // print string for motion, separated by line for ease of reading
  memset(buffer,'\0',sizeof(buffer));
  strcat(buffer,"{");
  strcat(buffer,"\"guid\":\"");
  strcat(buffer,GUID4);
  strcat(buffer,"\",\"organization\":\"");
  strcat(buffer,Org);
  strcat(buffer,"\",\"timecreated\":\"");
  strcat(buffer,"timenow");
  strcat(buffer,"\",\"displayname\":\"");
  strcat(buffer,Disp);
  strcat(buffer,"\",\"location\":\"");
  strcat(buffer,Locn);  
  strcat(buffer,"\",\"measurename\":\"");
  strcat(buffer,Measure4);
  strcat(buffer,"\",\"unitofmeasure\":\"");
  strcat(buffer,Units4);
  strcat(buffer,"\",\"value\":");
  strcat(buffer,dtostrf(motionvalue,3,1,dtostrfbuffer));
  strcat(buffer,"}");
 Serial.println(buffer);
 
 delay(100);

 if(Serial.available() > 0)
    {
       String str = Serial.readStringUntil('\n');
    Serial.println(str);
        if (str == "{command:off}"){
          digitalWrite(ledPinRed, LOW);
          digitalWrite(ledPinGreen, LOW);
        }
        else if (str == "{command:on}"){
          digitalWrite(ledPinRed, HIGH);
          digitalWrite(ledPinGreen, HIGH);
        }

    }

}// end loop()









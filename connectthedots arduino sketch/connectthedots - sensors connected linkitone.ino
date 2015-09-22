#include <dht11.h>
#include <stdlib.h>
#define MYSERIAL Serial
#define dht_dpin 1 //no ; here. Set equal to channel sensor is on
dht11 DHT;


int ledPinRed  =8;
int ledPinGreen =6;


const int LightSensorPin = A0;  // Analog input pin that the potentiometer is attached to
float lightsensorValue = 0;

const int pirPin = 12;    //the digital pin connected to the PIR sensor's output
float motionvalue = 0;


char GUID1[] = "xxxxxxxx-2222-xxxx-xxxx-xxxxxxxxxxxx";
char GUID2[] = "yyyyyyyy-2222-yyyy-yyyy-yyyyyyyyyyyy";
char GUID3[] = "zzzzzzzz-2222-zzzz-zzzz-zzzzzzzzzzzz";
char GUID4[] = "aaaaaaaa-2222-aaaa-aaaa-aaaaaaaaaaaa";
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

void setup() {
  	   /* Begin serial communication. */
	Serial.begin(9600);
       

        delay(500);
        Serial.println("Sensors connected");	
	Serial.println("Setup complete! Looping main program"); 
    pinMode(ledPinRed, OUTPUT);
     pinMode(ledPinGreen, OUTPUT);

}


void loop() {                

	
	if (true) {
            //This is the "heart" of the program.
            DHT.read(dht_dpin);
            lightsensorValue = get_light_level();
            motionvalue = digitalRead(pirPin);
          
            float temperatureC = DHT.temperature;

            memset(buffer, '\0', sizeof(buffer));
            strcat(buffer, "{");
            strcat(buffer, "\"guid\":\"");
            strcat(buffer, GUID1);
            strcat(buffer, "\",\"organization\":\"");
            strcat(buffer, Org);
            strcat(buffer, "\",\"timecreated\":\"");
            strcat(buffer, "timenow");
            strcat(buffer, "\",\"displayname\":\"");
            strcat(buffer, Disp);
            strcat(buffer, "\",\"location\":\"");
            strcat(buffer, Locn);
            strcat(buffer, "\",\"measurename\":\"");
            strcat(buffer, Measure1);
            strcat(buffer, "\",\"unitofmeasure\":\"");
            strcat(buffer, Units1);
            strcat(buffer, "\",\"value\":");
            strcat(buffer, dtostrf(temperatureC, 5, 2, dtostrfbuffer));
            strcat(buffer, "}");
            Serial.println(buffer);
           

			
            delay(500);
            // print string for humidity, separated by line for ease of reading
            memset(buffer, '\0', sizeof(buffer));
            strcat(buffer, "{");
            strcat(buffer, "\"guid\":\"");
            strcat(buffer, GUID2);
            strcat(buffer, "\",\"organization\":\"");
            strcat(buffer, Org);
            strcat(buffer, "\",\"timecreated\":\"");
            strcat(buffer, "timenow");
            strcat(buffer, "\",\"displayname\":\"");
            strcat(buffer, Disp);
            strcat(buffer, "\",\"location\":\"");
            strcat(buffer, Locn);
            strcat(buffer, "\",\"measurename\":\"");
            strcat(buffer, Measure2);
            strcat(buffer, "\",\"unitofmeasure\":\"");
            strcat(buffer, Units2);
            strcat(buffer, "\",\"value\":");
            strcat(buffer, dtostrf(DHT.humidity, 5, 2, dtostrfbuffer));
            strcat(buffer, "}");
            Serial.println(buffer);
           
            delay(500);
            
            // print string for light, separated by line for ease of reading
            memset(buffer, '\0', sizeof(buffer));
            strcat(buffer, "{");
            strcat(buffer, "\"guid\":\"");
            strcat(buffer, GUID3);
            strcat(buffer, "\",\"organization\":\"");
            strcat(buffer, Org);
            strcat(buffer, "\",\"timecreated\":\"");
            strcat(buffer, "timenow");
            strcat(buffer, "\",\"displayname\":\"");
            strcat(buffer, Disp);
            strcat(buffer, "\",\"location\":\"");
            strcat(buffer, Locn);
            strcat(buffer, "\",\"measurename\":\"");
            strcat(buffer, Measure3);
            strcat(buffer, "\",\"unitofmeasure\":\"");
            strcat(buffer, Units3);
            strcat(buffer, "\",\"value\":");
            strcat(buffer, dtostrf(lightsensorValue, 5, 3, dtostrfbuffer));
            strcat(buffer, "}");
            Serial.println(buffer);
            
            delay(500);
            
            // print string for motion, separated by line for ease of reading
            memset(buffer, '\0', sizeof(buffer));
            strcat(buffer, "{");
            strcat(buffer, "\"guid\":\"");
            strcat(buffer, GUID4);
            strcat(buffer, "\",\"organization\":\"");
            strcat(buffer, Org);
            strcat(buffer, "\",\"timecreated\":\"");
            strcat(buffer, "timenow");
            strcat(buffer, "\",\"displayname\":\"");
            strcat(buffer, Disp);
            strcat(buffer, "\",\"location\":\"");
            strcat(buffer, Locn);
            strcat(buffer, "\",\"measurename\":\"");
            strcat(buffer, Measure4);
            strcat(buffer, "\",\"unitofmeasure\":\"");
            strcat(buffer, Units4);
            strcat(buffer, "\",\"value\":");
            strcat(buffer, dtostrf(motionvalue, 3, 1, dtostrfbuffer));
            strcat(buffer, "}");
            Serial.println(buffer);
           
            delay(500);
	
  } else {
		Serial.println("Not publishing...");
	}

 if(Serial.available() > 0)
    {
       String str = Serial.readStringUntil('\n');
    
        if (str == "{command:off}"){
          digitalWrite(ledPinRed, LOW);
          digitalWrite(ledPinGreen, LOW);
        }
        else if (str == "{command:on}"){
          digitalWrite(ledPinRed, HIGH);
          digitalWrite(ledPinGreen, HIGH);
        }

    }


}

char *dtostrf (double val, signed char width, unsigned char prec, char *sout) {
  char fmt[20];
  sprintf(fmt, "%%%d.%df", width, prec);	  sprintf(sout, fmt, val);
  return sout;
}

float get_light_level()
{

  float lightSensor = analogRead(LightSensorPin);
  lightSensor = 1 / lightSensor * 10;
  return (lightSensor);
}

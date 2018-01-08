//
//    FILE: sensors.ino
//  AUTHOR: Bowoo Jang (codingbowoo@gmail.com)
// CREATED: September 4, 2017
// original code from https://github.com/ekyuho/connected_sensor  
// Released to the public domain
//


#include "MyWifi.h"
MyWifi mywifi("(SSID)", "(PASSWORD)"); // replace (SSID) and (PASSWORD) with your own ssid & password

#include "Bowoo.h"
Bowoo bw;

#include <SoftwareSerial.h>
SoftwareSerial dustport(D1, D0, false, 256);  // RX, TX

SoftwareSerial co2port(D6, D4, false, 256);// RX, TX
const uint8_t cmd[9] = {0xFF,0x01,0x86,0x00,0x00,0x00,0x00,0x00,0x79};

#include "DHT.h"

#define DHTPIN D2     // what digital pin the DHT22 is conected to
#define DHTTYPE DHT22   // there are multiple kinds of DHT sensors

// At Oled.ino
//SSD1306  display(0x3c, D3, D5);  //Data, Clock

#include "Dust.h"
Dust dust;

#include "RunningMedian.h"
RunningMedian pm25s = RunningMedian(19);
RunningMedian pm10s = RunningMedian(19);

const int RATIO = 10;
const int INTERVAL = 60000;
unsigned MYMIN = 0;
unsigned MYSEC = 0;

DHT dht(DHTPIN, DHTTYPE);
int ppm;

void setup() {
  Serial.begin(9600);
  Serial.setTimeout(2000);
  dustport.begin(9600);
  co2port.begin(9600);
  oled_setup();

  // Wait for serial to initialize.
  while(!Serial) { }
  Serial.print("\nConnect WiFi AP: ");
  mywifi.connect_ap();
  if (!mywifi.connected) oled_no_wifi();
  bw.setapikey(mywifi.macstring());
                                                                      
  Serial.println("-------------------------------------");
  Serial.println("Receiving Sensor Data: ");
  Serial.println("-------------------------------------");
  Serial.swap();
  Serial.swap();
}

void got_dust(int pm25, int pm10) {
   pm25 /= RATIO;
   pm10 /= RATIO;

   Serial.print(String(MYMIN)+"M "+ String(MYSEC) +"S, [pm25, pm10]=[");
   Serial.println(String(pm25) +", "+ String(pm10)+ "]");
   pm25s.add(pm25);
   pm10s.add(pm10);
   // Serial.println("pm25 size="+ String(pm25s.getSize()) +", count="+ String(pm25s.getCount()) +", median="+ String(pm25s.getMedian()));
   // Serial.println("pm10 size="+ String(pm10s.getSize()) +", count="+ String(pm10s.getCount()) +", median="+ String(pm10s.getMedian()));

   String msg = "";
   if (!mywifi.connected) msg = "NO WIFI";
   void oled_show(int, int, String);   
   oled_show(pm25, pm10, msg);
}

void do_interval(int ppm, float humid, float temp) {
  if (!mywifi.connected) return;
  bw.send(int(pm25s.getMedian()), int(pm10s.getMedian()), ppm, humid, temp);
}


unsigned long mark = 0, sec_mark = 0;
boolean got_interval = false, got_sec = false;
unsigned long missings = 0;

int timeSinceLastRead = 0;
void loop() {
  unsigned long current = millis();
  float h = 0; // variable for humidity
  float t = 0; // variable for temparature
  uint8_t response[9];

    if(timeSinceLastRead > 2000) {
    // Reading temperature or humidity takes about 250 milliseconds!
    // Sensor readings may also be up to 2 seconds 'old' (its a very slow sensor)
    h = dht.readHumidity();
    t = dht.readTemperature();

    // Check if any reads failed and exit early (to try again).
    if (isnan(h) || isnan(t)) {
      Serial.println("Failed to read from DHT sensor");
      timeSinceLastRead = 0;
      return;
    }

    // Compute heat index in Celsius (isFahreheit = false)
    // float hic = dht.computeHeatIndex(t, h, false);
    Serial.print("Humidity: " + String(h) + " %\t");
    Serial.println("Temperature: " + String(t) + " *C");
  
   
    // CO2 sensor work
    co2port.write(cmd,9);
    co2port.readBytes(response, 9);
    int responseHigh = (int) response[2];
    int responseLow = (int) response[3];
    ppm = (256*responseHigh) + responseLow;
    Serial.println("CO2="+ String(ppm) + " hello " + String(responseHigh) + " / " + String(responseLow));



  if (current > mark) {
    mark = current + INTERVAL;
    got_interval = true;
  }
  if (current > sec_mark) {
    sec_mark = current + 1000;
    got_sec = true;
    missings++;
  }
  
  while (dustport.available() > 0) {
    dust.do_char(dustport.read(), got_dust);
    missings = 0;
    yield();
  }
  
  if (got_interval) {
    got_interval = false;
    do_interval(ppm, h, t);
  }
  if (got_sec) {
    got_sec = false;
    MYMIN = (current/1000) / 60;
    MYSEC = (current/1000) % 60;
    
    if (missings > 15) {
      oled_waiting_dust(missings);
      Serial.println(String(MYMIN)+"M "+ String(MYSEC) +"S: No data from dust sensor. check wiring.");
    }
  }
  yield();

  
  
    timeSinceLastRead = 0;
  }
  delay(100);
  timeSinceLastRead += 100;

}

//
//    FILE: wifi.ino
//  AUTHOR: Kyuho Kim (ekyuho@gmail.com)
// CREATED: September 4, 2017
// Released to the public domain
//
#include "MyWifi.h"
#include <ESP8266WiFi.h>

MyWifi::MyWifi(String _ssid, String _password) { 
  _ssid.toCharArray(ssid, 32);
  _password.toCharArray(password, 32);
  connected = false;
}

MyWifi::MyWifi(String _ssid) {
  MyWifi(_ssid, String(""));
}

void scan () {
    int n = WiFi.scanNetworks();
    Serial.println("Networks nearby");
    for (int i = 0; i < n; ++i) {
      Serial.print(i + 1);
      Serial.print(": ");
      Serial.print(WiFi.SSID(i));
      Serial.print(" (");
      Serial.print(WiFi.RSSI(i));
      Serial.print(")");
      Serial.println((WiFi.encryptionType(i) == ENC_TYPE_NONE)?" ":"*");
    }
}

String MyWifi::macstring(void) {
  return(_macstring);
}

void MyWifi::connect_ap() {
  int count = 60;
  Serial.println();
  Serial.print("connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
    void oled_wifi_going(int, char*, char*);
    oled_wifi_going(count, ssid, password);
    if (!count--) {
      Serial.println("\nNO WIFI");
      scan();
      return;
    }
  }
  Serial.print("\nMy IP address: ");
  Serial.println(WiFi.localIP()); 
  Serial.print("My Mac address: ");
  byte mac[6]; 
  WiFi.macAddress(mac);
  char xx[13];
  for (int i=0; i<6; i++) sprintf(&xx[i*2], "%02x", mac[i]);
  xx[12] = 0;
  _macstring = String(xx);
  Serial.println(_macstring);
  
  Serial.println();
  connected = true;
  return;
}

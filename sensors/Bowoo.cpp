//
//    FILE: server.ino
//  AUTHOR: Bowoo Jang (lisabowoo@gmail.com)
// CREATED: December 31st, 2017
//

#include "Bowoo.h"
#include <ESP8266WiFi.h>
#include <WiFiClient.h>
byte server[] = {52, 78, 192, 119 };

Bowoo::Bowoo(void) {
    _host = "http://ec2-52-78-192-119.ap-northeast-2.compute.amazonaws.com";
    _url = "/log?";  
    _httpPort = 8080;
}

void Bowoo::setapikey(String apikey) {
    _apikey = apikey;
}

boolean Bowoo::send(int pm25, int pm10, int ppm, float humid, float temp) {
  WiFiClient client;

  if (!client.connect(server, 8080)) {
    Serial.print("Bw connection failed: ");
    return(false);
  }
  
  // String payload = "format=4&macapikey="+ _apikey +"&type=D&value="+ String(pm25)+","+ String(pm10) +"&seq="+ String(_seq++);  
  String payload = "pm25=" + String(pm25) + "&pm10=" + String(pm10) + "&ppm=" + String(ppm) + "&humi=" + String(humid)+ "&temp=" + String(temp);
  String getheader = "GET "+ String(_url) + payload +" HTTP/1.1";
  client.println(getheader);
  client.println("User-Agent: ESP8266 Bowoo Jang");  
  client.println("Host: " + String(_host));  
  client.println("Connection: close");  
  client.println();

  Serial.println(getheader);
  while (client.connected()) {
    String line = client.readStringUntil('\n');
    Serial.println(line);
  }
  Serial.println("Done Bowoo.");
}


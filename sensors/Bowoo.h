//
//    FILE: server.ino
//  AUTHOR: Bowoo Jang (lisabowoo@gmail.com)
// CREATED: December 31st, 2017
//

#ifndef Bowoo_h
#define Bowoo_h

#include "Arduino.h"

class Bowoo
{
  public:
    Bowoo(void);
    void setapikey(String);
    boolean send(int, int, int, float, float); // pm2.5, pm10, humidity, temparature
 
  private:
    String _apikey;
    String _url;
    char* _host;
    int _httpPort;   
    int _seq = 0;
};
#endif

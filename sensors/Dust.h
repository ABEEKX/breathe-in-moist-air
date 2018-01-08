//
//    FILE: dust.ino
//  AUTHOR: Kyuho Kim (ekyuho@gmail.com)
// CREATED: September 4, 2017
// Released to the public domain
//
#ifndef Dust_h
#define Dust_h

#include "Arduino.h"

class Dust 
{
  public:
    void do_char(char, void (*function)(int, int));
  private:
    int stat = 1;
    int cnt = 0;
    char buf[10];
};
#endif

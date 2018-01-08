//
//    FILE: dust.ino
//  AUTHOR: Kyuho Kim (ekyuho@gmail.com)
// CREATED: September 4, 2017
// Released to the public domain
//
#include "Dust.h"

void Dust::do_char(char c, void (*function)(int, int)) {
    //Serial.print("stat="+ String(stat) +", "+ "cnt="+ String(cnt) +" ");
    //Serial.print(c, HEX);
    //Serial.println(" ");

    if (stat == 1) {
       if (c == 0xAA) stat = 2;
    } else
    if (stat == 2) {
       if (c == 0xC0) stat =3;
       else stat = 1;
    } else
    if (stat == 3) {
       buf[cnt++] = c;
       if (cnt == 7) stat = 4;
    } else
    if (stat == 4) {
       if (c == 0xAB) {
          //check checusum
          stat = 1;
       }
       else {
          Serial.println("Eh? wrong tailer");
       }
       cnt = 0;
       int pm25 = buf[0] + 256*buf[1];
       int pm10 = buf[2] + 256*buf[3];
       function(pm25, pm10);
    }
}

#include <IRremote.h>
     
    IRsend sender;
     
    void setup() {
      
    }
     
    void loop() {
        sender.sendNEC(0x1FE40BF, 32);
        delay(1000);
    }

#include <Servo.h>

int pos = 0;    // variable to store the servo position
int angle = 10;


Servo myservo;  // create servo object to control a servo
// twelve servo objects can be created on most boards

void setup() {
  myservo.attach(9);  // attaches the servo on pin 9 to the servo object
  pinMode(13, OUTPUT); //set pin 13 as output
}

// Brown  GND
// Red    +
// Orange Signal              

void short_move(){
  
    for (pos = angle; pos >= 0; pos -= 1) { // goes from 180 degrees to 0 degrees
      myservo.write(pos);              // tell servo to go to position in variable 'pos'
      delay(1);                       // waits 15ms for the servo to reach the position
      digitalWrite(13, HIGH); //set pin 13 high (+5V)
    }    
    delay(200);
    for (pos = 0; pos <= angle; pos += 1) { // goes from 0 degrees to 180 degrees
      myservo.write(pos);              // tell servo to go to position in variable 'pos'
      delay(1);                       // waits 15ms for the servo to reach the position
      digitalWrite(13, LOW); //set pin 13 high (+5V)
    }
    delay(500);
}

void long_move(){
    for (pos = angle; pos >= 0; pos -= 1) { // goes from 180 degrees to 0 degrees
      myservo.write(pos);              // tell servo to go to position in variable 'pos'
      delay(1);                       // waits 15ms for the servo to reach the position
      digitalWrite(13, HIGH); //set pin 13 high (+5V)
    }
    delay(500);
    for (pos = 0; pos <= angle; pos += 1) { // goes from 0 degrees to 180 degrees
      myservo.write(pos);              // tell servo to go to position in variable 'pos'
      delay(1);                       // waits 15ms for the servo to reach the position
      digitalWrite(13, LOW); //set pin 13 high (+5V)
    }
    delay(500);
}

void s(){
  short_move();
  short_move();
  short_move();
  delay(1000);
  }

void o(){
  long_move();
  long_move();
  long_move();
  delay(1000);
  }

void m(){
  long_move();
  long_move();
  delay(1000);
  }

void a(){
  short_move();
  long_move();
  delay(1000);
  }

void r(){
  short_move();
  long_move();
  short_move();
  delay(1000);
  }
  
void d(){
  long_move();
  short_move();
  short_move();
  delay(1000);
  }
  
void u(){
  short_move();
  short_move();
  long_move();
  delay(1000);
  }

void k(){
  long_move();
  short_move();
  long_move();
  delay(1000);
  }
  
void loop() {
  s();
  delay(2000);
  o();
  delay(2000);
 }

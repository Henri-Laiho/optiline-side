/*
  Button

  Turns on and off a light emitting diode(LED) connected to digital pin 13,
  when pressing a pushbutton attached to pin 2.

  The circuit:
  - LED attached from pin 13 to ground
  - pushbutton attached to pin 2 from +5V
  - 10K resistor attached to pin 2 from ground

  - Note: on most Arduinos there is already an LED on the board
    attached to pin 13.

  created 2005
  by DojoDave <http://www.0j0.org>
  modified 30 Aug 2011
  by Tom Igoe

  This example code is in the public domain.

  http://www.arduino.cc/en/Tutorial/Button
*/

// constants won't change. They're used here to set pin numbers:
const int buttonPinL = 7;     // the number of the pushbutton pin for Left
const int buttonPinR = 8;     // the number of the pushbutton pin for Right
const int ledPin =  13;      // the number of the LED pin

// variables will change:
int buttonStateL = 0;         // variable for reading the pushbutton status
int buttonStateR = 0;         // variable for reading the pushbutton status

void setup() {
  // initialize the LED pin as an output:
  pinMode(ledPin, OUTPUT);
  // initialize the pushbutton pin as an input:
  pinMode(buttonPinL, INPUT);
  pinMode(buttonPinR, INPUT);

  Serial.begin(9600);
}

void loop() {
  // read the state of the pushbutton value:
  buttonStateL = digitalRead(buttonPinL);
  buttonStateR = digitalRead(buttonPinR);

  // check if the pushbutton is pressed. If it is, the buttonState is HIGH:
  if (buttonStateL == HIGH) {
    // turn LED on:
    digitalWrite(ledPin, HIGH);
    Serial.write("L");
    delay(1000);
  } else {
    // turn LED off:
    digitalWrite(ledPin, LOW);
  }

  if (buttonStateR == HIGH) {
    // turn LED on:
    digitalWrite(ledPin, HIGH);
    Serial.write("R");
    delay(1000);
  } else {
    // turn LED off:
    digitalWrite(ledPin, LOW);

  }
}

//MSG *IA2# I - input, O - output
//second letter - row, third etter - col

const int ledPin = 9;      // the pin that the LED is attached to
String msg;

void setup()
{
  // initialize the serial communication:
  Serial.begin(9600);
  // initialize the ledPin as an output:
  pinMode(ledPin, OUTPUT);
}

void loop() {
  // check if data has been sent from the computer:
  // if there's any serial available, read it:
  

    if (Serial.available()) {
      // read the most recent byte (which will be from 0 to 255):
      if (Serial.read() == '*') {
        msg = Serial.readStringUntil('#');
        
        Serial.println("Yes im here");
      }
      Serial.println(msg);
    }
  
}




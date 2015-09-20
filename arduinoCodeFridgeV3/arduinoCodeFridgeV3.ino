// PROTOCOL:
//MSG *IA2O# I - input, O - output
//     ^ device type
//      ^ row
//       ^ column
//        ^ state

#include <Servo.h> 

const int A_1 = 3;
const int A_2 = 4;
const int B_1 = 5;
const int B_2 = 6;
const int C_1 = 7;
const int C_2 = 8;
Servo servo1;

String msg;
char device;
char row;
char col;
char state;

void setup()
{
  // initialize the serial communication:
  Serial.begin(9600);
  // initialize the ledPin as an output:
  pinMode(A1, OUTPUT);
  servo1.attach(11);
}

void loop() {
  // check if data has been sent from the computer:
  // if there's any serial available, read it:


  if (Serial.available()) {
    if (Serial.read() == '*') {
      msg = Serial.readStringUntil('#');
      device = msg[0];
      row = msg[1];
      col = msg[2];
      state = msg[3];
      Serial.println("Action:"+String(device));
      Serial.println("Row:"+String(row));
      Serial.println("Column:"+String(col));
      Serial.println("Action:"+String(state));
      if (device == 'S') {
        if (state == '1') {
        turnLEDOn(row, col);
        Serial.println("Turn on LED");
        }
        if (state == '2') {
        turnLEDOff(row, col);
        Serial.println("Turn off LED");
        }
      }
      
    }
    Serial.println(msg);
  }

}

void turnLEDOff(char row, char col) {
  if (row == 'A') {
    if (col == '1') {
        digitalWrite(A_1, LOW);
    }
    if (col == '2') {
        digitalWrite(A_2, LOW);
    }
  }
  
    if (row == 'B') {
    if (col == '1') {
        digitalWrite(B_1, LOW);
    }
    if (col == '2') {
        digitalWrite(B_2, HIGH);
        delay(3000);
        digitalWrite(B_2, LOW);
    }
  }
  
    if (row == 'C') {
    if (col == '1') {
        digitalWrite(C_1, HIGH);
        delay(3000);
        digitalWrite(C_1, LOW);
    }
    if (col == '2') {
        digitalWrite(C_2, HIGH);
        delay(3000);
        digitalWrite(C_2, LOW);
    }
  }

}

void turnLEDOn(char row, char col) {
  if (row == 'A') {
    if (col == '1') {
        digitalWrite(A_1, HIGH);
        delay(3000);
        digitalWrite(A_1, LOW);
    }
    if (col == '2') {
        digitalWrite(A_2, HIGH);
        delay(3000);
        digitalWrite(A_2, LOW);
    }
  }
  
    if (row == 'B') {
    if (col == '1') {
        digitalWrite(B_1, HIGH);
        delay(3000);
        digitalWrite(B_1, LOW);
    }
    if (col == '2') {
        digitalWrite(B_2, HIGH);
        delay(3000);
        digitalWrite(B_2, LOW);
    }
  }
  
    if (row == 'C') {
    if (col == '1') {
        digitalWrite(C_1, HIGH);
        delay(3000);
        digitalWrite(C_1, LOW);
    }
    if (col == '2') {
        digitalWrite(C_2, HIGH);
        delay(3000);
        digitalWrite(C_2, LOW);
    }
  }

}
  
//void control(char row, char col) {
//  if (servoID  == 
//  servo1.write(105);
//  delay(700);
//  servo1.write(90);
//}
//
//void backServo(char servoID) {
//  
  


// PROTOCOL:
//MSG *LA2O# I - input, O - output
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
Servo A_1_servo; //PIN 11
Servo A_2_servo; //PIN 10

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
  A_1_servo.attach(11);
  A_2_servo.attach(10);
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
      if (device == 'L') {
        if (state == '1') {
          turnLEDOn(row, col);
          Serial.println("Turn on LED");
        }
        if (state == '0') {
          turnLEDOff(row, col);
          Serial.println("Turn off LED");
        }
      }
      if (device == 'S') {
        if (state == '1') {
          dumpServo(row, col);
          Serial.println("Dump servo ");
        }
        if (state == '0') {
          engageServo(row, col);
          Serial.println("Re-Engage servo LED");
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
      digitalWrite(B_2, LOW);
    }
  }

  if (row == 'C') {
    if (col == '1') {
      digitalWrite(C_1, LOW);
    }
    if (col == '2') {
      digitalWrite(C_2, LOW);
    }
  }

}

void turnLEDOn(char row, char col) {
  if (row == 'A') {
    if (col == '1') {
      digitalWrite(A_1, HIGH);
    }
    if (col == '2') {
      digitalWrite(A_2, HIGH);
    }
  }

  if (row == 'B') {
    if (col == '1') {
      digitalWrite(B_1, HIGH);
    }
    if (col == '2') {
      digitalWrite(B_2, HIGH);
    }
  }

  if (row == 'C') {
    if (col == '1') {
      digitalWrite(C_1, HIGH);
    }
    if (col == '2') {
      digitalWrite(C_2, HIGH);
    }
  }

}


void dumpServo(char row, char col) {
  if (row == 'A') {
    if (col == '1') {
      A_1_servo.write(105);
      delay(700);
      A_1_servo.write(90);
    }
  if (col == '2') {
      A_2_servo.write(105);
      delay(700);
      A_2_servo.write(90);
    }
}
}
 
 
 
void engageServo(char row, char col) {
  if (row == 'A') {
    if (col == '1') {
      A_1_servo.write(75);
      delay(700);
      A_1_servo.write(90);
    }
  if (col == '2') {
      A_2_servo.write(75);
      delay(700);
      A_2_servo.write(90);
    }
}
}

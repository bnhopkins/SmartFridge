import serial # must install serial lib: $pip install pyserial
import time
serArduino = serial.Serial('/dev/tty.usbmodem1421', 9600)
# serArduino.write("*LA11#")

# //  PROTOCOL:
# // MSG *LA2O# I - input, O - output
# //      ^ device type
# //       ^ row
# //        ^ column
# //         ^ state


def main():
    dState('L','A','1','1')
    time.sleep(3)
    dState('L','A','1','0')

def dState(device,row,col,state): # Changes device states
    serArduino.write("*"+device+row+col+state+"#")

main()

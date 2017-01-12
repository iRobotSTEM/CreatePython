import serial
import time

# Assuming BRC is connected to RTS, to wake up the robot.
def wakeRobot(ser):
    ser.rts = True
    time.sleep(0.1)
    ser.rts = False
    time.sleep(1) # Wait for robot to wake up, if asleep.

def resetRobotAndWait(ser):
    ser.reset_input_buffer()
    # Send reset op code to robot
    ser.write('\x07')

    # Wait patiently for text to stop scrolling by so that we know the robot
    #  is reset and not plugged into the charger.
    sBuffer = "dummy string"
    while len(sBuffer) is not 0:
        sBuffer = ser.readline()
        print sBuffer.strip()

# Main body of code starts here!

raw_input("Please unplug the charger, if you haven't already, and then press Enter to continue.")

# Open a serial connection to Roomba.
ser = serial.Serial(port='/dev/ttyUSB0', baudrate=115200, timeout = 3.0)

wakeRobot(ser)

print "Resetting robot:"
resetRobotAndWait(ser)

print "Waking robot to set the LEDs and play a song."
wakeRobot(ser)

# Assuming the robot is awake, start safe mode so we can hack.
ser.write('\x80\x83')
time.sleep(.1)

# Write "Cre8" on the LED screen
ser.write('\xa4Cre8')

# Program a five-note start song into Roomba.
ser.write('\x8c\x00\x05C\x10H\x18J\x08L\x10O\x20')

# Play the song we just programmed.
ser.write('\x8d\x00')
time.sleep(1.6) # wait for the song to complete

print "Done for now; leaving the robot in passive mode."
# Leave the Roomba in passive mode; this allows it to keep
#  running Roomba behaviors while we wait for more commands.
ser.write('\x80')

# Close the serial port; we're done for now.
# Note that if RTS is not toggled within five minutes, 
# the robot will fall asleep, again.
ser.close()

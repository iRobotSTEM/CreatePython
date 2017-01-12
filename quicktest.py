import serial
import time

# Open a serial connection to Roomba; doing so should wake robot
ser = serial.Serial(port='/dev/ttyUSB0', baudrate=115200)
time.sleep(1) # Wait for robot to wake up, if asleep.

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

# Leave the Roomba in passive mode; this allows it to keep
#  running Roomba behaviors while we wait for more commands.
ser.write('\x80')

# Close the serial port; we're done for now.
# Note that if RTS is not toggled within five minutes, 
# the robot will fall asleep, again.
ser.close()

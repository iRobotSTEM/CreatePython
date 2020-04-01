#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###########################################################################
# Copyright (c) 2017-2020 iRobot Corporation#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#   Redistributions of source code must retain the above copyright
#   notice, this list of conditions and the following disclaimer.
#
#   Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in
#   the documentation and/or other materials provided with the
#   distribution.
#
#   Neither the name of iRobot Corporation nor the names
#   of its contributors may be used to endorse or promote products
#   derived from this software without specific prior written
#   permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
###########################################################################

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
    ser.write(b'\x07')
    ser.flush()

    # Wait patiently for text to stop scrolling by so that we know the robot
    #  is reset and not plugged into the charger.
    sBuffer = "dummy string"
    while len(sBuffer) is not 0:
        sBuffer = ser.readline()
        print(sBuffer.strip())

# Main body of code starts here!

input("Please unplug the charger, if you haven't already, and then press Enter to continue.")
# Open a serial connection to Roomba.
ser = serial.Serial(port='/dev/ttyUSB0', baudrate=115200, timeout = 3.0)

wakeRobot(ser)

print("Resetting robot:")
resetRobotAndWait(ser)

print("Waking robot to set the LEDs and play a song.")
wakeRobot(ser)

# Assuming the robot is awake, start safe mode so we can hack.
ser.write(b'\x80\x83')
ser.flush()
time.sleep(.1)

# Write "Cre8" on the LED screen
ser.write(b'\xa4Cre8')
ser.flush()

# Program a five-note start song into Roomba.
ser.write(b'\x8c\x00\x05C\x10H\x18J\x08L\x10O\x20')
ser.flush()

# Play the song we just programmed.
ser.write(b'\x8d\x00')
ser.flush()
time.sleep(1.6) # wait for the song to complete

print("Done for now; leaving the robot in passive mode.")
# Leave the Roomba in passive mode; this allows it to keep
#  running Roomba behaviors while we wait for more commands.
ser.write(b'\x80')
ser.flush()

# Close the serial port; we're done for now.
# Note that if RTS is not toggled within five minutes, 
# the robot will fall asleep, again.
ser.close()

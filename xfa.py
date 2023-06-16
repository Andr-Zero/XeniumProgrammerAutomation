#!/usr/bin/python3


# Python wrapper for Xenium programming using Pi-ZeroW PC-Board
# Copyright (C) 2019 Koos du Preez (kdupreez@hotmail.com)
##
# Automation script cobbled together by Andr0, Rev.5
##
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import os
import subprocess
import RPi.GPIO as GPIO
import time
import threading

######### Start of user configuration #########

# Working Directory
programmer_root = "/home/user/xenium-programmer/"

# OpenXenium Flash File Location.
tsopFlash = os.path.join(programmer_root, "xenium-bin/MakeMhz.bin")

#########  End of user configuration #########

# Commands
cmd_jtag =  os.path.join(programmer_root, "xenium-flash/bin/xenium-jtag")
cmd_jflash =  os.path.join(programmer_root, "xenium-flash/bin/xenium-flash")

# CPLD Files
flash_jed = os.path.join(programmer_root, "xenium-bin/xeniumflash.jed")
xenium_jed= os.path.join(programmer_root, "xenium-bin/openxenium.jed")

# LED Pins
led1 = 19
led2 = 6
led3 = 7

# Button Pins
p1 = 13
p2 = 5
p3 = 25
p4 = 24

def led_clear():
    GPIO.output(led1, GPIO.LOW)
    GPIO.output(led2, GPIO.LOW)
    GPIO.output(led3, GPIO.LOW)
    time.sleep(.2)

def led_flash():

    while True:
        if led == "ok":
            led_clear()
            GPIO.output(led1, GPIO.HIGH)
            time.sleep(1)
            
        elif led == "busy_JTAG":
            led_clear()
            GPIO.output(led2, GPIO.HIGH)
            time.sleep(0.1)
        
        elif led == "busy_LPC":
            led_clear()
            GPIO.output(led2, GPIO.HIGH)
            time.sleep(0.5)

        elif led == "error_JTAG":
            led_clear()
            GPIO.output(led3, GPIO.HIGH)
            time.sleep(0.1)
 
        elif led == "error_LPC":
            led_clear()
            GPIO.output(led3, GPIO.HIGH)
            time.sleep(0.5)

        elif led == "idle":
            led_clear()
            # *--
            GPIO.output(led1, GPIO.HIGH)
            GPIO.output(led2, GPIO.LOW)
            GPIO.output(led3, GPIO.LOW)
            time.sleep(0.2)
            if led == "idle":
                # **-
                GPIO.output(led1, GPIO.LOW)
                GPIO.output(led2, GPIO.HIGH)
                GPIO.output(led3, GPIO.LOW)
                time.sleep(0.2)
            
            if led == "idle":
                # -**
                GPIO.output(led1, GPIO.LOW)
                GPIO.output(led2, GPIO.LOW)
                GPIO.output(led3, GPIO.HIGH)
                time.sleep(0.2)

def shutdown(pinIgnored):
    GPIO.cleanup()
    os.system("sudo shutdown -h now")

def bitbusFirmware(pinIgnored):
    # Program CPLD with BitBus Flash Writer code.
    global led
    led = "busy_JTAG"
    print("\n-------------------------------------")
    print("PROGRAMMING XILINX CPLD: BITBUS BRIDGE")
    print("--------------------------------------\n", flush=True)
    sub_proc = subprocess.run([cmd_jtag, flash_jed])
    if sub_proc.returncode == 0:
        tsop(1)
    else:
        led = "error_JTAG"
        print("\nERROR Programming the Xilinx CPLD as bitBus Bridge!")
        print("Please double check for solder bridges and the JTAG connection!\n", flush=True)
        
def tsop(pinIgnored):
    # Program CPLD with BitBus Flash Writer code.
    global led
    led = "busy_LPC"
    print("\n-----------------------------")
    print("PROGRAMMING FLASH : XENIUM OS")
    print("-----------------------------\n", flush=True)
    sub_proc = subprocess.run([cmd_jflash, tsopFlash, "-y"])
    if sub_proc.returncode == 0:
        xeniumFirmware(1)
    else:
        led = "error_LPC"
        print("\nERROR Loading XeniumOS into Flash memory!")
        print("Please double check for solder bridges and the LPC connection!\n", flush=True)
        
def xeniumFirmware(pinIgnored):
    # Program CPLD with OpenXenium Firmware.
    global led
    led = "busy_JTAG"
    print("\n---------------------------------------------")
    print("PROGRAMMING XILINX CPLD: OPEN XENIUM FIRMWARE")
    print("---------------------------------------------\n", flush=True)
    sub_proc = subprocess.run([cmd_jtag, xenium_jed])
    if sub_proc.returncode == 0:
        led = "ok"
        print("\nMORE INPUT! MORE INPUT!!\n", flush=True)
    else:
        led = "error_JTAG"
        print("\nERROR Programming the Xilinx CPLD with Xenium Firmware!")
        print("Please double check the LPC Header connection!\n", flush=True)

#Using Broadcom pin numbering.
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#Setup pins
GPIO.setup(led1, GPIO.OUT)
GPIO.setup(led2, GPIO.OUT)
GPIO.setup(led3, GPIO.OUT)
GPIO.setup(p1, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(p2, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(p3, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(p4, GPIO.IN, pull_up_down = GPIO.PUD_UP)

# Monitor Button Press
GPIO.add_event_detect(p1, GPIO.FALLING, callback = bitbusFirmware, bouncetime = 2000)
GPIO.add_event_detect(p2, GPIO.FALLING, callback = tsop, bouncetime = 2000)
GPIO.add_event_detect(p3, GPIO.FALLING, callback = xeniumFirmware, bouncetime = 2000)
GPIO.add_event_detect(p4, GPIO.FALLING, callback = shutdown, bouncetime = 2000)

#define Vars
led = "idle"

if __name__ == "__main__":
    try:
        print("---------------------------------------------")
        print("   Programmer Automation Started!            ")
        print(" NOTE: BIN File location defined in script.  ")
        print("---------------------------------------------\n", flush=True)
        if os.path.isfile(tsopFlash) and os.access(tsopFlash, os.R_OK):
            print("TSOP File Access.............. OK")
        else:
            print("TSOP file Access.............. ERROR")
        if os.path.isfile(cmd_jtag) and os.access(cmd_jtag, os.R_OK):
            print("Xenium JTAG File Access....... OK")
        else:
            print("Xenium JTAG file Access....... ERROR")            
        if os.path.isfile(cmd_jflash) and os.access(cmd_jflash, os.R_OK):
            print("Xenium Flash File Access...... OK")
        else:
            print("Xenium Flash file Access...... ERROR")            
        if os.path.isfile(flash_jed) and os.access(flash_jed, os.R_OK):
            print("Flash JED File Access......... OK")
        else:
            print("Flash JED file Access......... ERROR")            
        if os.path.isfile(xenium_jed) and os.access(xenium_jed, os.R_OK):
            print("Xenium JED File Access........ OK")
        else:
            print("Xenium JED file Access........ ERROR")            
        status = threading.Thread(target=led_flash)
        status.start()
            
        while True:
            time.sleep(1)
    finally:
        # Cleanup GPIO
        GPIO.cleanup()

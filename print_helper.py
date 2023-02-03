'''
handles all printing
change stuff here like the header, etc.
'''

from Adafruit_Thermal import *
import serial

# check for presence of thermal printer
printer_is_present = False
try:
    printer = Adafruit_Thermal("/dev/serial0", 19200, timeout=5)
    printer_is_present = True
except:
    print("PRINTER NOT FOUND - USING STANDARD OUTPUT")

# printer_is_present = False


def print_message(name, message):
    '''
    prints a message from the web messaging service
    '''
    if printer_is_present:
        if name == "":
            name = "Anonymous"
        # print header
        printer.setSize('L')
        printer.justify('C')
        printer.println("NEW MESSAGE")
        # print who it's from
        printer.setSize('M')
        printer.println("From: "+name+"\n")
        # print the message
        printer.setSize('S')
        printer.justify('L')
        printer.println(message+"\n")
        # print a line at the bottom
        printer.println("-"*32)
        # feed 2 lines so its visible
        printer.feed(2)
    else:
        if name == "":
            name = "Anonymous"
        # print header
        print("NEW MESSAGE")
        # print who it's from
        print("From: "+name+"\n")
        # print the message
        print(message+"\n")
        # print a line at the bottom
        print("-"*32)

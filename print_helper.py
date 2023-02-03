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


def print_big_header():
    '''
    prints "YOUR DAY TODAY" real big at the top of the page
    '''
    if printer_is_present:
        printer.setSize('L')
        printer.justify('C')
        printer.println("YOUR DAY TODAY")
    else:
        print("YOUR DAY TODAY")


def print_date(date):
    dateString = date.strftime("%A, %B %d, %Y")
    if printer_is_present:
        printer.setSize('M')
        printer.justify('C')
        printer.println(dateString)
        printer.feed(1)
    else:
        print(dateString)


def print_events(events):
    '''
    prints an event from the calendar service
    '''
    if printer_is_present:
        printer.setSize('M')
        printer.justify('L')
        printer.println("CALENDAR:")
    else:
        print("CALENDAR:")
    for event in events:
        # get values from event
        title = event["summary"]
        start_time = event["start"].get("dateTime")[11:16]

        # do a little formatting to make it look pretty
        hour = start_time[0:2]
        mins = start_time[3:8]
        if int(hour) > 12:
            new_hour = str(int(hour)-12)
            start_time = new_hour+":"+mins+" PM"
        elif hour[0] == "0":
            start_time = start_time[1:]
            start_time += " AM"
        elif int(hour) < 12:
            start_time += " AM"
        elif int(hour) == 12:
            start_time += " PM"
        if printer_is_present:
            printer.setSize('S')
            printer.justify('L')
            number_of_dashes = 32 - len(title) - len(start_time)
            printer.println(title+"-"*number_of_dashes+start_time)
        else:
            print(title+"-----"+start_time)
    if len(events) == 0:
        if printer_is_present:
            printer.setSize('S')
            printer.justify('L')
            printer.println("NO EVENTS")
        else:
            print("NO EVENTS")


def print_end_sequence():
    if printer_is_present:
        printer.setSize('S')
        printer.justify('L')
        printer.println("-"*32)
        printer.feed(2)
    else:
        print("-"*32)
        print("\n\n")
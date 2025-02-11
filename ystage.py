#!/usr/bin/python
#
## @file
#
# Kunal Pandit 9/19
#
# Illumina HiSeq2500 Y-STAGE
# Uses command set from Parker ViX 250IH & ViX500 IH
#


import serial
import io
import time


# YSTAGE object

class Ystage():
    
    #
    # Make Ystage object
    #
    def __init__(self, com_port, baudrate = 9600):

        # Open Serial Port
        s = serial.Serial(com_port, baudrate, timeout = 1)

        # Text wrapper around serial port                
        self.serial_port = io.TextIOWrapper(io.BufferedRWPair(s,s,),
                                            encoding = 'ascii',
                                            errors = 'ignore')                
        self.min_y = -7000000
        self.max_y = 7500000
        self.prefix = '1'
        self.suffix = '\r\n'
        self.on = False
        self.position = 0
        self.home = 0
        
    #
    # Initialize Ystage
    #
    def initialize(self):

        response = self.command('Z')                                    # Initialize Stage
        print('ystage: ' + response)

        response = self.command('W(EX,0)')                              # Turn off echo
        print('ystage: ' + response)
                        
        response = self.command('GAINS(5,10,7,1.5,0)')                  # Set gains
        print('ystage: ' + response)                             

        response = self.command('MA')                                   # Set to absolute position mode
        print('ystage: ' + response)
                        
        response = self.command('ON')                                   # Turn Motor ON
        print('ystage: ' + response)
        self.on = True
                        
        response = self.command('GH')                                   # Home Stage
        print('ystage: ' + response)
        # Takes forever to home, do other stuff while y stage homes
        #while not self.check_position():
        #    time.sleep(1)
        #self.position = self.read_position()        

    #
    # Send generic command to Ystage and return response
    #
    def command(self, text):
                        
        self.serial_port.write(self.prefix + text + self.suffix)        # Write to serial port
        self.serial_port.flush()                                        # Flush serial port
        return self.serial_port.readline()                              # Return response
        
    # 
    # Move Ystage to a position
    #
    def move(self, position):
        if position <= self.max_y and position >= self.min_y:
            self.command('D' + str(position))                               # Set distance
            self.command('G')                                               # Go
            while not self.check_position():                                # Wait till y stage is in position
                time.sleep(1)
            self.read_position()                                            # Update stage position
            return True                                                     # Return True that stage is in position
        else:
            print("YSTAGE can only between " + str(self.min_y) + ' and ' + str(self.max_y))

    #
    # Check if Ystage is in position, 1 = yes, 0 = no

    def check_position(self):
        return int(self.command('R(IP)')[1:])                          
    #      
    # Return position of Ystage
    #
    def read_position(self):
        self.position = int(self.command('R(PA)')[1:])                  # Read and store position

        return self.position        

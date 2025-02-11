#!/usr/bin/python
#
## @file
#
# Kunal Pandit 9/19
#
# Illumina HiSeq2500 Optics
# Uses commands found on  https://www.hackteria.org/wiki/HiSeq2000_-_Next_Level_Hacking#Control_Software
#

import time

# Optics object

class Optics():
    #
    # Make Zstage object
    #
    def __init__(self, fpga):
    
        self.serial_port = fpga              
        self.ex = [None, None]
        self.em_in = None
        self.suffix = '\n'
        self.ex_dict = [
                        # EX1    
                        {'home' : 0,
                         'OD1p4' : -36,
                         'OD0p6' : -71,
                         'OD0p2' : -107,
                         'open'  : 143,
                         'OD1p6' : 107,
                         'OD2p0' : 71,
                         'OD4p0' : 36},
                        # EX
                        {'home' : 0,
                         'OD0p2': -107,
                         'open' : 143,
                         'OD2p5': 71}
                        ]
        
                   
    #
    # Initialize Optics 
    #
    def initialize(self):

        #Home Excitation Filters
        self.move_ex(1, 'home')
        self.move_ex(2, 'home')

        # Move emission filter into light path
        self.move_em_in(True)                
                    
    #
    # Send generic serial commands to Optics and return response 
    #
    def command(self, text):                        
        self.serial_port.write(text + self.suffix)                      # Write to serial port
        self.serial_port.flush()                                        # Flush serial port
        return self.serial_port.readline()                              # Return response
                        
                        
    #   
    # Move/Home Excitation Filter    
    #
    def move_ex(self, wheel, position):
        if wheel != 1 and wheel != 2:
            print('Choose excitation filter 1 or 2')
        elif position in self.ex_dict[wheel-1].keys():
            self.command('EX' + str(wheel)+ 'HM')                       # Home Filter
            self.ex[wheel-1] = position
            if position != 'home':                   
                position = str(self.ex_dict[wheel-1][position])         # get step position
                self.command('EX' + str(wheel) + 'MV ' + position)      # Move Filter relative to home 
        elif position not in self.ex_dict[wheel-1].keys():
            print(position + ' filter does not exist in excitation ' + str(wheel))

    #
    # Move emission filter in/out of light path
    # TODO: Check position of emission filter
    #
    def move_em_in(self, INorOUT):
        if INorOUT:
            self.command('EM2I')                                        # Move emission filter into path
            self.em_in = True
        else:
            self.command('EM2O')                                        # Move emission filter out of path
            self.em_in = False

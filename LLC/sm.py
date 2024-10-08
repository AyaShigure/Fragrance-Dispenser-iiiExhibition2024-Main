#!/usr/bin/env python3
from uploader_functions.uploader_functions import *

if __name__ == '__main__':
    port = '/dev/ttyACM0'    
    os.system("clear")
    fancy_print()
    RP2040headerString = PrintRP2040Header()

    active_serial_monitor(port, RP2040headerString)
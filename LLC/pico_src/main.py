from includes.LLC_functions import *
from includes.Subsystems import *
from includes.Stepper_pin_def import *
from machine import Pin, PWM, ADC
import time
'''
    1. System basic functionalitis, tests
    2. Full feedforward control, start to end, with only the control discription
    3. 

    99. A Serial communication control mode
'''


###### Stage 1, System initializations ######
'''
    About boot.py, having boot.py makes deleting files on rp2040 really slow somehow.
'''
time.sleep(3) # Prevent the rshell from grabbing the serial port
boot() # Initialize all pins to 0, beep for 6 times.
led = Pin(25, Pin.OUT)
#############################################
#############################################


##### Stage 2, Actual code ######
vertical_top_limit_switch = Pin(2, Pin.IN, Pin.PULL_UP)
vertical_bottom_limit_switch = Pin(1, Pin.IN, Pin.PULL_UP)
horizontal_plate_side_limit_switch = Pin(3, Pin.IN, Pin.PULL_UP)
horizontal_frame_side_limit_switch = Pin(4, Pin.IN, Pin.PULL_UP)


time_counter = 1
while(1):
    if vertical_bottom_limit_switch.value() == 0:
        print('vertical_bottom_limit_switch is on')
    if vertical_top_limit_switch.value() == 0:
        print('vertical_top_limit_switch is on')
    if horizontal_plate_side_limit_switch.value() == 0:
        print('horizontal_plate_side_limit_switch is on')
    if horizontal_frame_side_limit_switch.value() == 0:
        print('horizontal_frame_side_limit_switch is on')


    time.sleep(0.001)
    time_counter += 1
    if time_counter == 1000:
        beep(1)
        time_counter = 1



##### Stage 3, Done ######
beep(5)
while(1):
    led.toggle()
    time.sleep(0.5)
    led.toggle()
    time.sleep(0.5)

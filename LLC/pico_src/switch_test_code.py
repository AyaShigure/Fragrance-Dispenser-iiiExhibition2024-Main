# from includes.LLC_functions import *
# from includes.Subsystems import *
# from includes.Stepper_pin_def import *
from machine import Pin, PWM, ADC
import time




# self.vertical_top_limit_switch = Pin(2, Pin.IN, Pin.PULL_UP)
# self.vertical_bottom_limit_switch = Pin(1, Pin.IN, Pin.PULL_UP)

# ############## ############## ############## Horizontal motor and limit switches
# '''
#     Motor 4 is used as horizontal position control.
# '''
# self.horizontal_pos_motor = tb6600(
#     step_pin=stepper_motors_pins['Motor 4']['step_pin'],
#     direction_pin=stepper_motors_pins['Motor 4']['direction_pin'],
#     enable_pin=stepper_motors_pins['Motor 4']['enable_pin']
#     ) 

# self.horizontal_plate_side_limit_switch = Pin(3, Pin.IN, Pin.PULL_UP)
# self.horizontal_frame_side_limit_switch = Pin(4, Pin.IN, Pin.PULL_UP)
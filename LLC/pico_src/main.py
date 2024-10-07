from includes.LLC_functions import *
from includes.Subsystems import *

from machine import Pin, PWM, ADC
import time
'''
    1. System basic functionalitis, tests
    2. Full feedforward control, start to end, with only the control discription
    3. 

    99. A Serial communication control mode
'''

# About boot.py, having boot.py makes deleting files on rp2040 really slow somehow.
time.sleep(3) # Prevent the rshell from grabbing the serial port
boot()

led = Pin(25, Pin.OUT)


''' Motor Designations
Motor 1: 
    enable_pin = 22
    direction_pin = 23
    step_pin = 24

Motor 2:
    enable_pin = 19
    direction_pin = 20
    step_pin = 21

Motor 3:
    enable_pin = 17
    direction_pin = 16
    step_pin = 15

Motor 4:
    enable_pin = 12
    direction_pin = 11
    step_pin = 10

Motor 5:
    enable_pin = 9
    direction_pin = 8
    step_pin = 7
'''

# Define motor
enable_pin = 22
direction_pin = 23
step_pin = 24
motor1 = tb6600(step_pin, direction_pin, enable_pin)
motor1.enable_motor()

dir = True
for _ in range(6):
    dir = not dir
    time.sleep(0.01)
    motor1.rotate_with_ramp(steps=400, direction=dir, min_delay_us=800, max_delay_us=2000, ramp_steps=100)

    time.sleep(0.01)
    beep(1)
    time.sleep(0.1)

motor1.disable_motor()
beep(5)


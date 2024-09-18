from includes.LLC_functions import *
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
pin_init()
beep()




led = Pin(25, Pin.OUT)

# Define motor
enable_pin = 22
direction_pin = 23
step_pin = 24
motor = tb6600(step_pin, direction_pin, enable_pin)
motor.set_direction(True)

for _ in range(2):
    # motor.disable_motor()
    # motor.enable_motor()
    # motor.rotate_with_ramp(steps=4000, direction=True, min_delay_us=1000, max_delay_us=2000, ramp_steps=1)
    # motor.disable_motor()


    pwm =  PWM(Pin(step_pin))
    pwm.freq(1000)



counter = 0
while(counter < 10):

    if counter % 2 == 0:
        buzzer.value(1)
        time.sleep(0.1)
        buzzer.value(0)
        time.sleep(0.1)
        print('Damn')
        # motor.enable_motor()
        # motor.set_direction(1)
        # for _ in range(200):
        #     motor.pulse(delay_us=2500)
        motor.enable_motor()
        motor.rotate_with_ramp(steps=4000, direction=True, min_delay_us=1000, max_delay_us=5000, ramp_steps=1)
        motor.disable_motor()

    counter += 1

    led.toggle()
    time.sleep(1)

for i in range(5):
    buzzer.value(1)
    time.sleep(0.1)
    buzzer.value(0)
    time.sleep(0.1)

motor.disable_motor()

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

# 初始化每个 tb6600 电机类
motor1 = tb6600(
    step_pin=stepper_motors_pins['Motor 1']['step_pin'],
    direction_pin=stepper_motors_pins['Motor 1']['direction_pin'],
    enable_pin=stepper_motors_pins['Motor 1']['enable_pin']
)

motor2 = tb6600(
    step_pin=stepper_motors_pins['Motor 2']['step_pin'],
    direction_pin=stepper_motors_pins['Motor 2']['direction_pin'],
    enable_pin=stepper_motors_pins['Motor 2']['enable_pin']
)

motor3 = tb6600(
    step_pin=stepper_motors_pins['Motor 3']['step_pin'],
    direction_pin=stepper_motors_pins['Motor 3']['direction_pin'],
    enable_pin=stepper_motors_pins['Motor 3']['enable_pin']
)

motor4 = tb6600(
    step_pin=stepper_motors_pins['Motor 4']['step_pin'],
    direction_pin=stepper_motors_pins['Motor 4']['direction_pin'],
    enable_pin=stepper_motors_pins['Motor 4']['enable_pin']
)

motor5 = tb6600(
    step_pin=stepper_motors_pins['Motor 5']['step_pin'],
    direction_pin=stepper_motors_pins['Motor 5']['direction_pin'],
    enable_pin=stepper_motors_pins['Motor 5']['enable_pin']
)

motors = [motor1, motor2, motor3, motor4, motor5]

for motor in motors:
    motor.enable_motor()
    for _ in range(3):
        dir = not dir
        time.sleep(0.01)
        motor.rotate_with_ramp(steps=200, direction=dir, min_delay_us=1000, max_delay_us=3000, ramp_steps=100)

        time.sleep(0.01)
        beep(1)
        time.sleep(0.1)
    motor.disable_motor()
    beep(3)




beep(5)
while(1):
    led.toggle()
    time.sleep(0.5)
    led.toggle()
    time.sleep(0.5)


# # Define motor
# enable_pin = 22
# direction_pin = 23
# step_pin = 24
# motor1 = tb6600(step_pin, direction_pin, enable_pin)
# motor1.enable_motor()

# dir = True
# for _ in range(6):
#     dir = not dir
#     time.sleep(0.01)
#     motor1.rotate_with_ramp(steps=400, direction=dir, min_delay_us=800, max_delay_us=2000, ramp_steps=100)

#     time.sleep(0.01)
#     beep(1)
#     time.sleep(0.1)

# motor1.disable_motor()
# beep(5)


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


###### Estop configrations
estop_pin = 5
system_self_harm_preventer_pin = Pin(estop_pin, Pin.IN, Pin.PULL_UP) # It prevents self harming behavior
def handle_estop(self):
    while(1):
        beep(2)
        print('Emergency E-Stopped. Reboot to resolve the issue.')
        time.sleep(2)
system_self_harm_preventer_pin.irq(trigger=Pin.IRQ_FALLING, handler=handle_estop)

#############################################
#############################################

##### Stage 2, Control logic ######
Pipette_Manipulator = Pipette_Manipulator()

_ = Pipette_Manipulator.horizontal_move_to_frame_side(set_delay_us=6000)
_ = Pipette_Manipulator.horizontal_move_to_plate_side(set_delay_us=6000)

time.sleep(1)
beep(2)

_ = Pipette_Manipulator.vertical_move_to_bottom(set_delay_us=5000)
_ = Pipette_Manipulator.vertical_move_to_top(set_delay_us=5000)


Pipette_Manipulator.disable_stepper_motors()




#############################################
#############################################

##### Stage 3, Done ######
beep(3)
while(1):
    led.toggle()
    time.sleep(0.5)
    led.toggle()
    time.sleep(0.5)

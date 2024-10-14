from includes.LLC_functions import *
from includes.Subsystems import *
from includes.Stepper_pin_def import *
from includes.Subsystem_motion_sequences import *

from machine import Pin, PWM, ADC
import time
'''
    1. System basic functionalitis, tests
    2. Full feedforward control, start to end, with only the control discription
    3. 

    99. A Serial communication control mode
'''

#############################################
###### Stage 1, System initializations ######
'''
    About boot.py, having boot.py makes deleting files on rp2040 really slow somehow.
'''
time.sleep(3) # Prevent the rshell from grabbing the serial port
boot() # Initialize all pins to 0, beep for 6 times.
# led = Pin(25, Pin.OUT)


###### Estop configrations ###### Some how the switch is so to extremely sensitive
estop_pin = 5
system_self_harm_preventer_pin = Pin(estop_pin, Pin.IN, Pin.PULL_UP) # It prevents self harming behavior
def handle_estop(self):
    if system_self_harm_preventer_pin.value() == 1:
        while(1):
            beep(2)
            print('Emergency E-Stopped. Reboot to resolve the issue.')
            time.sleep(2)

system_self_harm_preventer_pin.irq(trigger=Pin.IRQ_FALLING, handler=handle_estop)

#############################################
##### Stage 2, Control logic ######
# Pipette_Manipulator_Motion_Sequences = Pipette_Manipulator_Motion_Sequences()
# Pipette_Manipulator_Motion_Sequences.go_home()
# Pipette_Manipulator_Motion_Sequences.pick_up_a_pipette()

# Rotatory_Plate_Motion_Sequences = Rotatory_Plate_Motion_Sequences()
# Rotatory_Plate_Motion_Sequences.demo_move()

# adc0 = ADCReader(26, name = 'adc0 gpio 26')
# adc1 = ADCReader(27, name = 'adc1 gpio 27')

# while(1):
#     adc0.print_status()
#     # time.sleep(0.5)
#     adc1.print_status()
#     # beep(1)
#     time.sleep(2)

Rotatry_Plate = Rotatry_Plate()
Rotatry_Plate.plate_motor_A.enable_motor()
Rotatry_Plate.plate_motor_B.enable_motor()
Rotatry_Plate.plate_motor_A.set_direction(True)
Rotatry_Plate.plate_motor_B.set_direction(True)

now = time.time()
while((time.time() - now )< 300):
    position_state = Rotatry_Plate.check_laser_sensing()
    print(f'Laser_sensing state: {position_state}')

    if position_state == 0: # Reached 0 position
        beep(4)
        print('Initial position is reached')
        time.sleep(4)
        # Move out of the laser sensor window
        for _ in range(5):
            Rotatry_Plate.pulse_both_motors(delay_us=30000)
            
    if position_state == 1:
        beep(2)
        print('Reached a test tube position')
        time.sleep(2)


    # Go how many steps
    for _ in range(1):
        Rotatry_Plate.pulse_both_motors(delay_us=30000)

    time.sleep(1)


Rotatry_Plate.plate_motor_A.disable_motor()
Rotatry_Plate.plate_motor_B.disable_motor()


# while(1):
#     Rotatry_Plate.laser_sensor_threshold_debug_print()


#############################################


#############################################
##### Stage 3, Done ######
beep(3)
pin_init()
# Pipette_Manipulator.deninit_endeffector()

while(1):
    # led.toggle()
    # time.sleep(0.5)
    # led.toggle()
    # time.sleep(0.5)
    beep(1)
    time.sleep(1)

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




# Pipette_Manipulator_Motion_Sequences = Pipette_Manipulator_Motion_Sequences()
# Rotatory_Plate_Motion_Sequences = Rotatory_Plate_Motion_Sequences()

# Rotatory_Plate_Motion_Sequences.go_home()
# Pipette_Manipulator_Motion_Sequences.go_home()



# Pipette_Manipulator_Motion_Sequences = Pipette_Manipulator_Motion_Sequences()
# Rotatory_Plate_Motion_Sequences = Rotatory_Plate_Motion_Sequences()

# Rotatory_Plate_Motion_Sequences.go_home()
# Pipette_Manipulator_Motion_Sequences.go_home()



# # for _ in range(2):
# #     for _ in range(24):
# #         Pipette_Manipulator_Motion_Sequences.Pipette_manipulator_execute_once()
# #         beep(1)
# #         Rotatory_Plate_Motion_Sequences.Rotatry_Plate.rotate_untill_next_test_tube(auto_engage_disengage=False)
# #     Rotatory_Plate_Motion_Sequences.go_home()
# #     Pipette_Manipulator_Motion_Sequences.go_home()




# def execute_once(Target_fragrancenumber):
#     Rotatory_Plate_Motion_Sequences.Rotatry_Plate.engage_motor_AB()
#     for _ in range(Target_fragrancenumber):
#         time.sleep(0.5)
#         beep(1)
#         Rotatory_Plate_Motion_Sequences.Rotatry_Plate.rotate_untill_next_test_tube(auto_engage_disengage=False)

#     Pipette_Manipulator_Motion_Sequences.Pipette_manipulator_execute_once()
    

#     Rotatory_Plate_Motion_Sequences.go_home()
#     Pipette_Manipulator_Motion_Sequences.go_home()

# execute_once(0)
# execute_once(2)
# execute_once(4)
# execute_once(24)


# Pipette_Manipulator_Motion_Sequences.go_home()
# Pipette_Manipulator_Motion_Sequences.pick_up_a_pipette()
# Pipette_Manipulator_Motion_Sequences.drop_a_drop()
# Pipette_Manipulator_Motion_Sequences.put_back_the_pipette()
# Pipette_Manipulator_Motion_Sequences.Pipette_manipulator_execute_once()



# # Rotatory plate control sequences test
# Rotatory_Plate_Motion_Sequences.go_to_test_tube_NO_n(20)
# beep(10)
# Rotatory_Plate_Motion_Sequences.go_home()

# # while(1):
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

from includes.LLC_functions import *
from includes.Stepper_pin_def import *
from includes.Subsystems import *

from machine import Pin, PWM, ADC
import time

''' 
    This script defines all the motion sequences for all the sub systems.
'''


###### ###### ###### ###### Pipette Manipulator Motion Sequences
class Pipette_Manipulator_Motion_Sequences:
    def __init__(self) -> None:
        self.Pipette_Manipulator = Pipette_Manipulator()
        self.at_home_question_mark = False

    def go_home(self):
        _ = self.Pipette_Manipulator.horizontal_move_to_plate_side(set_delay_us=6000)
        _ = self.Pipette_Manipulator.vertical_move_to_top(set_delay_us=5000)
        self.at_home_question_mark = True
    
    def pick_up_a_pipette(self):
        if self.at_home_question_mark != True:
            self.go_home()
        self.at_home_question_mark = False

        self.Pipette_Manipulator.horizontal_motor_pulse_steps(direction_str='frame_side', steps=80, set_delay_us=3000)
        _ = self.Pipette_Manipulator.vertical_move_to_bottom(set_delay_us=3000)
        self.Pipette_Manipulator.vertical_motor_pulse_steps(direction_str='up', steps=20, set_delay_us=5000)

        self.Pipette_Manipulator.engage_gripper()
        self.Pipette_Manipulator.engage_pusher()
        self.Pipette_Manipulator.disengage_pusher()
        time.sleep(0.5)
        beep(1)

        _ = self.Pipette_Manipulator.vertical_move_to_top(set_delay_us=3000)

###### ###### ###### ###### Rotatory Plate Motion Sequences
class Rotatory_Plate_Motion_Sequences:
    def __init__(self) -> None:
        self.Rotatry_Plate = Rotatory_Plate()
        self.current_pos = None
    
    def go_home(self):
        self.Rotatry_Plate.engage_motor_AB()
        while(1):
            position_state_ = self.Rotatry_Plate.check_laser_sensing()
            if position_state_ != 0:
                self.Rotatry_Plate.rotate_untill_next_test_tube()
            elif position_state_ == 0:
                break
            
        self.current_pos = 0
        beep(5)
        self.Rotatry_Plate.disengage_motor_AB()

    def go_to_test_tube_NO_n(self, n):
        if self.current_pos == None:
            self.go_home()
        while(self.current_pos != n-1):
            self.Rotatry_Plate.rotate_untill_next_test_tube(auto_engage_disengage=True)
            self.current_pos += 1
        beep(5)




# Rotatry_Plate.plate_motor_A.enable_motor()
# Rotatry_Plate.plate_motor_B.enable_motor()
# Rotatry_Plate.plate_motor_A.set_direction(True)
# Rotatry_Plate.plate_motor_B.set_direction(True)

# now = time.time()
# while((time.time() - now )< 600):

#     position_state = Rotatry_Plate.check_laser_sensing()
#     # print(f'Laser_sensing state: {position_state}')
#     if position_state == 0: # Reached 0 position
#         beep(4)
#         print('Initial position is reached')
#         time.sleep(4)
#         # Move out of the laser sensor window
#         for _ in range(5):
#             Rotatry_Plate.pulse_both_motors(delay_us=30000)
            
#     if position_state == 1:
#         beep(2)
#         print('Reached a test tube position')
#         time.sleep(0.5)
#         # Move out of the laser sensor window
#         for _ in range(5):
#             Rotatry_Plate.pulse_both_motors(delay_us=30000)

#     # Go how many steps
#     for _ in range(1):
#         Rotatry_Plate.pulse_both_motors(delay_us=40000)



# Rotatry_Plate.plate_motor_A.disable_motor()
# Rotatry_Plate.plate_motor_B.disable_motor()









class Receipt_Conveyor_Motion_Sequences:
    def __init__(self) -> None:
        pass

# Pipette_Manipulator = Pipette_Manipulator()

# # _ = Pipette_Manipulator.vertical_move_to_top(set_delay_us=5000)
# # _ = Pipette_Manipulator.horizontal_move_to_frame_side(set_delay_us=6000)
# _ = Pipette_Manipulator.horizontal_move_to_plate_side(set_delay_us=6000)
# # Pipette_Manipulator.gripper_demo()

# time.sleep(1)
# beep(2)

# _ = Pipette_Manipulator.vertical_move_to_bottom(set_delay_us=5000)
# # _ = Pipette_Manipulator.vertical_move_to_top(set_delay_us=5000)

# # Pipette_Manipulator.gripper_demo()

# Pipette_Manipulator.disable_stepper_motors()

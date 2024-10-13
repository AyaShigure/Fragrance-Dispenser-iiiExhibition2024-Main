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

        self.Pipette_Manipulator



Pipette_Manipulator = Pipette_Manipulator()

# _ = Pipette_Manipulator.vertical_move_to_top(set_delay_us=5000)
# _ = Pipette_Manipulator.horizontal_move_to_frame_side(set_delay_us=6000)
_ = Pipette_Manipulator.horizontal_move_to_plate_side(set_delay_us=6000)
# Pipette_Manipulator.gripper_demo()

time.sleep(1)
beep(2)

_ = Pipette_Manipulator.vertical_move_to_bottom(set_delay_us=5000)
# _ = Pipette_Manipulator.vertical_move_to_top(set_delay_us=5000)

# Pipette_Manipulator.gripper_demo()

Pipette_Manipulator.disable_stepper_motors()
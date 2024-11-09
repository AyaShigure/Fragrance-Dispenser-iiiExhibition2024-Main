from includes.LLC_functions import *
from includes.Stepper_pin_def import *
from includes.Subsystems import *

from machine import Pin, PWM, ADC
import time

'''
    Design draft doc based postcard and posters !!!!!!
'''

''' 
    This script defines all the motion sequences for all the sub systems.
'''
def eep():
    print('who wont go crazy doing multiple brain juice demanding projects, accross multiple engineering ')
    time.sleep(1)

###### ###### ###### ###### Pipette Manipulator Motion Sequences
class Pipette_Manipulator_Motion_Sequences:
    def __init__(self) -> None:
        self.Pipette_Manipulator = Pipette_Manipulator()
        self.at_home_question_mark = False

    def go_home(self):
        '''
            The pipette manipulator returns to the up, plate side initial position.
        '''
        _ = self.Pipette_Manipulator.vertical_move_to_top(set_delay_us=1500)
        _ = self.Pipette_Manipulator.horizontal_move_to_plate_side(set_delay_us=1500)
        self.at_home_question_mark = True
    
    def pick_up_a_pipette(self):
        '''
            The pipette manipulator starts from its initial position,
            lower the gripper and pick up a pipette.
        '''
        if self.at_home_question_mark != True:
            self.go_home()
        self.at_home_question_mark = False

        self.Pipette_Manipulator.disengage_gripper()
        self.Pipette_Manipulator.disengage_pusher()

        self.Pipette_Manipulator.horizontal_motor_pulse_steps(direction_str='frame_side', steps=80, set_delay_us=2000)
        _ = self.Pipette_Manipulator.vertical_move_to_bottom(set_delay_us=3000)
        self.Pipette_Manipulator.vertical_motor_pulse_steps(direction_str='up', steps=20, set_delay_us=2000)

        self.Pipette_Manipulator.engage_gripper()
        beep(1)
        self.Pipette_Manipulator.engage_pusher()
        time.sleep(1)
        self.Pipette_Manipulator.disengage_pusher()
        time.sleep(0.1)
        self.Pipette_Manipulator.engage_pusher()
        time.sleep(0.3)
        self.Pipette_Manipulator.disengage_pusher()
        time.sleep(0.1)

        # time.sleep(0.5)
        beep(2)

        _ = self.Pipette_Manipulator.vertical_move_to_top(set_delay_us=1500)
        self.go_home()
        self.at_home_question_mark = True

    def put_back_the_pipette(self):
        '''
            The pipette manipulator starts from its initial position,
            lower the gripper (but not all the way to the bottom),
            release the gripper to let the pipette fall back into the test tube while avoiding hard crashing

        ''' 
        if self.at_home_question_mark != True:
            self.go_home()
        self.at_home_question_mark = False

        self.Pipette_Manipulator.horizontal_motor_pulse_steps(direction_str='frame_side', steps=47, set_delay_us=2000)
        self.Pipette_Manipulator.vertical_motor_pulse_steps(direction_str='down', steps=790, set_delay_us=8000)
        self.Pipette_Manipulator.horizontal_motor_pulse_steps(direction_str='frame_side', steps=40, set_delay_us=2000)

        self.Pipette_Manipulator.disengage_pusher()
        self.Pipette_Manipulator.disengage_gripper()
        # time.sleep(0.5)
        # self.Pipette_Manipulator.engage_gripper()
        # self.Pipette_Manipulator.engage_pusher()
        # time.sleep(0.5)
        beep(1)

        self.Pipette_Manipulator.disengage_servo_motors()
        _ = self.Pipette_Manipulator.vertical_move_to_top(set_delay_us=3000)
        self.go_home()
        self.at_home_question_mark = True

    def drop_a_drop(self):
        '''
            Move to the top position, then to the frme side, lower the manipulator,
            drop a drop, then go home.
        '''
        self.at_home_question_mark = False
        _ = self.Pipette_Manipulator.vertical_move_to_top(set_delay_us=1500)

        _ = self.Pipette_Manipulator.horizontal_move_to_frame_side(set_delay_us=1500)
        self.Pipette_Manipulator.vertical_motor_pulse_steps(direction_str='down', steps=600, set_delay_us=1500)
        self.Pipette_Manipulator.engage_pusher()
        beep(1)
        time.sleep(0.1)

        self.Pipette_Manipulator.disengage_pusher()

        self.go_home()
        self.at_home_question_mark = True

    def Pipette_manipulator_execute_once(self):
        '''
            A full execution cycle start from initial home position, get pipette, drop a drop, put the pipette back, then go home
        '''
        self.go_home()
        self.pick_up_a_pipette()
        self.drop_a_drop()
        self.put_back_the_pipette()




###### ###### ###### ###### Rotatory Plate Motion Sequences
class Rotatory_Plate_Motion_Sequences:
    def __init__(self) -> None:
        self.Rotatry_Plate = Rotatory_Plate() 
        self.current_pos = None
    
    def go_home(self,dir=0):
        self.Rotatry_Plate.engage_motor_AB()
        while(1):
            position_state_ = self.Rotatry_Plate.rotate_untill_home_reaching_home_pos()
            if position_state_ != 0:
                self.Rotatry_Plate.rotate_untill_next_test_tube(auto_engage_disengage=False, go_home_mode=True,direction=dir)
            elif position_state_ == 0:
                break
            
        self.current_pos = 0
        beep(5)
        # self.Rotatry_Plate.disengage_motor_AB()

    def go_to_test_tube_NO_n(self, n):
        if self.current_pos == None:
            self.go_home()
        while(self.current_pos != n-1):
            self.Rotatry_Plate.rotate_untill_next_test_tube(auto_engage_disengage=False)
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

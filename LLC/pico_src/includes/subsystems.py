from includes.LLC_functions import *


class Rotatry_Plate():

    pass


class Pipette_Manipulator_Gripper():
    def __init__(self) -> None:
        self.pipette_gripper = Servo(25,initial_angel=140) # 140 -> Outer most pos, 140 ->
        self.pipette_pusher = Servo(18,initial_angel=80) # 80 -> Outer most pos, 80 -> 110
        self.pipette_gripper_angle_limit = [140, 115] # [Outer most, Inner most]
        self.pipette_pusher_angle_limit = [90, 100] # [Outer most, Inner most]
    
        self.vertical_pos_motor = None # Stepper class
        self.vertical_top_limit_switch = None # Limit switch class
        self.vertical_bottom_limit_switch = None # Limit switch class
        
        self.horizontal_pos_motor = None # Stepper class
        self.horizontal_motor_side_limit_switch = None # Limit switch class
        self.horizontal_frame_side_limit_switch = None # Limit switch class

    # Basical control functions
    def engage_gripper(self):
        self.pipette_gripper.set_angle(self.pipette_gripper_angle_limit[1])
    def disengage_gripper(self):
        self.pipette_gripper.set_angle(self.pipette_gripper_angle_limit[0])
    def engage_pusher(self):
        self.pipette_pusher.set_angle(self.pipette_pusher_angle_limit[1])
    def disengage_pusher(self):
        self.pipette_pusher.set_angle(self.pipette_pusher_angle_limit[0])

    def gripper_demo(self):
        for _ in range(4):
            self.engage_pusher()
            time.sleep(.5)
            self.engage_gripper()
            beep(1)
            time.sleep(.5)

            self.disengage_gripper()
            time.sleep(.5)

            self.disengage_pusher()
            beep(2)
            time.sleep(.5)

            time.sleep(0.1)

class Receipt_Conveyor():

    pass
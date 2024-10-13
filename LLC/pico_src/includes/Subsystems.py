from includes.LLC_functions import *
from includes.Stepper_pin_def import *
# This function sets defines the subsystems within the fragrance dispenser


''' Motor Designations:
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


# # 初始化每个 tb6600 电机类
# motor1 = tb6600(
#     step_pin=stepper_motors_pins['Motor 1']['step_pin'],
#     direction_pin=stepper_motors_pins['Motor 1']['direction_pin'],
#     enable_pin=stepper_motors_pins['Motor 1']['enable_pin']
# )

# motor2 = tb6600(
#     step_pin=stepper_motors_pins['Motor 2']['step_pin'],
#     direction_pin=stepper_motors_pins['Motor 2']['direction_pin'],
#     enable_pin=stepper_motors_pins['Motor 2']['enable_pin']
# )

# motor5 = tb6600(
#     step_pin=stepper_motors_pins['Motor 5']['step_pin'],
#     direction_pin=stepper_motors_pins['Motor 5']['direction_pin'],
#     enable_pin=stepper_motors_pins['Motor 5']['enable_pin']
# )

# motors = [motor1, motor2, motor3, motor4, motor5]

''' 
    Position limit switch pin:
        Vertical top: 2
        Vertical bottom: 1
        Horizontal plate side: 3
        Horizontal frame side: 4
'''
class Pipette_Manipulator():
    def __init__(self) -> None:
        ############## ############## ############## Endeffector/gripper
        self.pipette_gripper = Servo(25,initial_angel=140) # 140 -> Outer most pos, 140 ->
        self.pipette_pusher = Servo(18,initial_angel=80) # 80 -> Outer most pos, 80 -> 110
        self.pipette_gripper_angle_limit = [140, 115] # [Outer most, Inner most]
        self.pipette_pusher_angle_limit = [90, 100] # [Outer most, Inner most]
    
        ############## ############## ############## Vertical motor and limit switches
        '''
            Motor 3 is used as vertical position control.
        '''
        self.vertical_pos_motor = tb6600( 
            step_pin=stepper_motors_pins['Motor 5']['step_pin'],
            direction_pin=stepper_motors_pins['Motor 5']['direction_pin'],
            enable_pin=stepper_motors_pins['Motor 5']['enable_pin']
            ) 
        self.vertical_pos_motor.disable_motor()
        self.vertical_top_limit_switch = Pin(2, Pin.IN, Pin.PULL_UP)
        self.vertical_bottom_limit_switch = Pin(1, Pin.IN, Pin.PULL_UP)
        ############## ############## ############## Horizontal motor and limit switches
        '''
            Motor 4 is used as horizontal position control.
        '''
        self.horizontal_pos_motor = tb6600(
            step_pin=stepper_motors_pins['Motor 3']['step_pin'],
            direction_pin=stepper_motors_pins['Motor 3']['direction_pin'],
            enable_pin=stepper_motors_pins['Motor 3']['enable_pin']
            ) 
        self.horizontal_pos_motor.disable_motor()
        self.horizontal_plate_side_limit_switch = Pin(3, Pin.IN, Pin.PULL_UP)
        self.horizontal_frame_side_limit_switch = Pin(4, Pin.IN, Pin.PULL_UP)

    #### Vertical pos control ####
    def vertical_move_to_top(self, set_delay_us):
        self.vertical_pos_motor.enable_motor()
        self.vertical_pos_motor.set_direction(False)
        while self.vertical_top_limit_switch.value() !=0:
            self.vertical_pos_motor.pulse(delay_us=set_delay_us)
        beep(1)
        self.vertical_pos_motor.disable_motor()
        return 1

    def vertical_move_to_bottom(self, set_delay_us):
        self.vertical_pos_motor.enable_motor()
        self.vertical_pos_motor.set_direction(True)
        while self.vertical_bottom_limit_switch.value() !=0:
            self.vertical_pos_motor.pulse(delay_us=set_delay_us)
        beep(1)
        self.vertical_pos_motor.disable_motor()
        return 1

    def vertical_motor_pluse_steps(self, direction, steps, set_delay_us=5000):
        '''
            Move direction:
                direction = True : move to bottom 
                direction = False : move to top

            WARNING: This function is feed fordward control,
                     Do not use this function to move too far of distance.
        '''
        
        # Check if control is doable, i.e. not gonna crash the limit sensors
        if direction == True: # Trying to move to the bottom
            if self.vertical_bottom_limit_switch.value() == 0: # is going to crash into the bottom switch
                print('The endeffector is already at the bottom.')
                return 
        if direction == False: # Trying to move to the top
            if self.vertical_top_limit_switch.value() == 0: # is going to crash into the top switch
                print('The endeffector is already at the top.')
                return 
            
        # Above check is checked, do the sick move.
        self.vertical_pos_motor.enable_motor()
        self.vertical_pos_motor.set_direction(direction)
        for _ in range(steps):
            self.vertical_pos_motor.pulse(delay_us=set_delay_us)
        beep(1)
        self.vertical_pos_motor.disable_motor()


    #### Horizontal pos control ####
    def horizontal_move_to_plate_side(self, set_delay_us):
        self.horizontal_pos_motor.enable_motor()
        self.horizontal_pos_motor.set_direction(False)
        while self.horizontal_plate_side_limit_switch.value() != 0:
            self.horizontal_pos_motor.pulse(delay_us=set_delay_us)
        beep(1)
        self.horizontal_pos_motor.disable_motor()
        return 1

    def horizontal_move_to_frame_side(self, set_delay_us):
        self.horizontal_pos_motor.enable_motor()
        self.horizontal_pos_motor.set_direction(True)
        while self.horizontal_frame_side_limit_switch.value() != 0:
            self.horizontal_pos_motor.pulse(delay_us=set_delay_us)
        beep(1)
        self.horizontal_pos_motor.disable_motor()
        return 1

    def horizontal_motor_pluse_steps(self, direction, steps, set_delay_us=6000):
        '''
            Move direction:
                direction = True : move to frame side
                direction = False : move to plate side

            WARNING: This function is feed fordward control,
                     Do not use this function to move too far of distance.
        '''
        # Check if control is doable, i.e. not gonna crash the limit sensors
        if direction == True: # Trying to move to the frame side
            if self.horizontal_frame_side_limit_switch.value() == 0: # is going to crash into the bottom switch
                print('The endeffector is already at the bottom.')
                return 
        if direction == False: # Trying to move to the plate side
            if self.horizontal_plate_side_limit_switch.value() == 0: # is going to crash into the top switch
                print('The endeffector is already at the top.')
                return 
            
        # Above check is checked, do the sick move.
        self.vertical_pos_motor.enable_motor()
        self.vertical_pos_motor.set_direction(direction)
        for _ in range(steps):
            self.vertical_pos_motor.pulse(delay_us=set_delay_us)
        beep(1)



    def disable_stepper_motors(self):
        self.vertical_pos_motor.disable_motor()
        self.horizontal_pos_motor.disable_motor()

    #### Endeffector control ####
    # Basical control functions
    def engage_gripper(self):
        self.pipette_gripper.set_angle(self.pipette_gripper_angle_limit[1])
    def disengage_gripper(self):
        self.pipette_gripper.set_angle(self.pipette_gripper_angle_limit[0])
    def engage_pusher(self):
        self.pipette_pusher.set_angle(self.pipette_pusher_angle_limit[1])
    def disengage_pusher(self):
        self.pipette_pusher.set_angle(self.pipette_pusher_angle_limit[0])

    def deninit_endeffector(self):
        self.pipette_gripper.deinit()
        self.pipette_pusher.deinit()

    def gripper_demo(self):
        for _ in range(3):
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

    #### Subsystem combined control
    def pipette_manipulator_go_home(self):
        pass





class Rotatry_Plate():
    def __init__(self) -> None:
        pass





class Receipt_Conveyor():
    def __init__(self) -> None:
        pass
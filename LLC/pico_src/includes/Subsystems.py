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

# motor5 = tb6600(
#     step_pin=stepper_motors_pins['Motor 5']['step_pin'],
#     direction_pin=stepper_motors_pins['Motor 5']['direction_pin'],
#     enable_pin=stepper_motors_pins['Motor 5']['enable_pin']
# )

# motors = [motor1, motor2, motor3, motor4, motor5]

class Rotatory_Plate():
    def __init__(self) -> None:
        # These 2 motor must be pulsed together
        self.plate_motor_A = tb6600(
                step_pin=stepper_motors_pins['Motor 1']['step_pin'],
                direction_pin=stepper_motors_pins['Motor 1']['direction_pin'],
                enable_pin=stepper_motors_pins['Motor 1']['enable_pin']
            )
        self.plate_motor_B = tb6600(
                step_pin=stepper_motors_pins['Motor 2']['step_pin'],
                direction_pin=stepper_motors_pins['Motor 2']['direction_pin'],
                enable_pin=stepper_motors_pins['Motor 2']['enable_pin']
            )
        self.plate_motor_A.disable_motor()
        self.plate_motor_B.disable_motor()

        ########## ########## ########## 
        # Laser positioning sensors initializations
        self.inner_laser_sensor = ADCReader(26, name = 'Inner sensor') 
        self.outer_laser_sensor = ADCReader(27, name = 'Outer sensor') 
        self.laser_sensor_threshold = 2.3 # On Off threshold
        ########## ########## ##########

    ##### Motor control utilities
    def engage_motor_AB(self):
        self.plate_motor_A.enable_motor()
        self.plate_motor_B.enable_motor()
    
    def disengage_motor_AB(self):
        self.plate_motor_A.disable_motor()
        self.plate_motor_B.disable_motor()

    def set_direction_AB(self, direction):
        self.plate_motor_A.set_direction(direction)
        self.plate_motor_B.set_direction(direction)

    def pulse_both_motors(self, delay_us = 10000):
        '''
            Pulse both motor together.
        '''
        self.plate_motor_A.step.on()
        self.plate_motor_B.step.on()
        time.sleep_us(delay_us)
        self.plate_motor_A.step.off()
        self.plate_motor_B.step.off()
        time.sleep_us(delay_us)

    def rotate_both_motors(self, direction, step, set_delay_time):
        '''
            Rotate both motor for designated step along the designated direction.
        '''
        self.engage_motor_AB()
        self.set_direction_AB(direction)
        for _ in range(step):
            self.pulse_both_motors(set_delay_time)
        self.disengage_motor_AB()

    def check_laser_sensing(self):
        '''
            This function will return the sensor state.
            With all the gap between test tube holder covered by masking tape,
            Me could determine the rotatory plate's position.

            return 0: Sensor is over home position test tube.
            return 1: Sensor is over a test tube holder.
            return -1: Sensors are fully blocked, sensor and test tube holder is not aligned.
        '''
        ########### Check outer sensor ###########
        outer_voltage = self.outer_laser_sensor.read_voltage()
        if outer_voltage > self.laser_sensor_threshold:
            outer_sensor_state = True
        else:
            outer_sensor_state = False

        ########### Check inner sensor ###########
        inner_volatge = self.inner_laser_sensor.read_voltage()
        if inner_volatge > self.laser_sensor_threshold:
            inner_sensor_state = True
        else:
            inner_sensor_state = False

        # # Debug print
        # print(f'inner_sensor_state: {inner_sensor_state}, outer_sensor_state: {outer_sensor_state}')
        ########### ########### ########### ###########
        # Current position state
        if inner_sensor_state == True and outer_sensor_state == True:
            ### Reached 0 positon
            return 0
        elif inner_sensor_state == False and outer_sensor_state == True:
            ### Reached a test tube position
            return 1
        elif inner_sensor_state == False and outer_sensor_state == False:
            ### In the middle of transition
            return -1
        else:
            return None
        
    def laser_sensor_threshold_debug_print(self):
        ''' 
            Triggering threshold will change depending on the lighting conditions
            Use this to check if the threshold should be changed.
        '''
        self.inner_laser_sensor.print_status()
        self.outer_laser_sensor.print_status()
        beep(2)
        time.sleep(2)

    def rotate_untill_next_test_tube(self, auto_engage_disengage=False):
        '''
            This function will rotate the plate untill sensor is triggered.
        '''
        if auto_engage_disengage:
            self.engage_motor_AB()

        for _ in range(10):
            self.pulse_both_motors(delay_us=40000)
        while(1):
            position_state = self.check_laser_sensing()
            if position_state == 0 or position_state == 1:
                beep(1)
                if auto_engage_disengage:
                    self.disengage_motor_AB()
                return
            self.pulse_both_motors(delay_us=40000)




class Receipt_Conveyor():

    def __init__(self) -> None:
        self.plate_motor_A = tb6600(
                step_pin=stepper_motors_pins['Motor 4']['step_pin'],
                direction_pin=stepper_motors_pins['Motor 4']['direction_pin'],
                enable_pin=stepper_motors_pins['Motor 4']['enable_pin']
            )
        self.plate_motor_A.disable_motor()

        ########## ########## ########## 
        # Laser positioning sensors initializations
        self.receipt_sensor = ADCReader(28, name = 'receipt sensor') 
        self.receipt_sensor_state = False
        ########## ########## ##########

    def laser_sensing(self):
        pass











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

    # direction_str must be 'up' or 'down'
    def vertical_motor_pulse_steps(self, direction_str, steps, set_delay_us=5000):

        if direction_str == 'up':
            direction = False
        elif direction_str == 'down':
            direction = True
        else:
            print('Invalid direction string, check you direction string !!!!!aaaaa')
            return
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

    # direction_str must be 'plate_side' or 'frame_side'
    def horizontal_motor_pulse_steps(self, direction_str, steps, set_delay_us=6000):
        if direction_str == 'plate_side':
            direction = False
        elif direction_str == 'frame_side':
            direction = True
        else:
            print('Invalid direction string, check you direction string !!!!!aaaaa')
            return
            
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
        self.horizontal_pos_motor.enable_motor()
        self.horizontal_pos_motor.set_direction(direction)
        for _ in range(steps):
            self.horizontal_pos_motor.pulse(delay_us=set_delay_us)
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

    # def deninit_endeffector(self): # This actually will not fork for servos saves 
    #     self.pipette_gripper.deinit()
    #     self.pipette_pusher.deinit()

    def gripper_demo(self):
        for _ in range(3):
            # Engage
            self.engage_pusher()
            time.sleep(.5)
            self.engage_gripper()
            beep(1)
            time.sleep(.5)

            # Disengage
            self.disengage_gripper()
            time.sleep(.5)
            self.disengage_pusher()
            beep(2)
            time.sleep(.5)

from includes.LLC_functions import *
from includes.Subsystems import *
from includes.Stepper_pin_def import *
from includes.Subsystem_motion_sequences import *

Pipette_Manipulator_Motion_Sequences = Pipette_Manipulator_Motion_Sequences()
Rotatory_Plate_Motion_Sequences = Rotatory_Plate_Motion_Sequences()

# Rotatory_Plate_Motion_Sequences.go_home()
# Pipette_Manipulator_Motion_Sequences.go_home()


def execute_once(Target_fragrancenumber):
    Rotatory_Plate_Motion_Sequences.Rotatry_Plate.engage_motor_AB()
    for _ in range(Target_fragrancenumber):
        time.sleep(0.5)
        beep(1)
        Rotatory_Plate_Motion_Sequences.Rotatry_Plate.rotate_untill_next_test_tube(auto_engage_disengage=False)

    Pipette_Manipulator_Motion_Sequences.Pipette_manipulator_execute_once()

    Rotatory_Plate_Motion_Sequences.go_home()
    Pipette_Manipulator_Motion_Sequences.go_home()
    
    
def system_go_home():
    Rotatory_Plate_Motion_Sequences.go_home()
    Pipette_Manipulator_Motion_Sequences.go_home()

    
def system_power_off():
    boot() # Initialize all pins to 0, beep for 6 times.


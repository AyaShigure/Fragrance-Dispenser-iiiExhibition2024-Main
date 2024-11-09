
port = '/dev/ttyACM0'
import os
import time

class Fragrance_Dispenser_The_Machine():
    def __init__(self, port):
        self.include_cmd = 'from\ Fragrance_Dispenser_API_pico\ import\ \* '
        self.command_header = 'rshell repl pyboard '
        self.command_end = '~1+1~'
        
    def system_go_home(self):
        go_home_cmd = '~system_go_home\(\) '
        cmd = self.command_header + self.include_cmd + go_home_cmd + self.command_end
        print(cmd)

        self.send_serial_command(cmd)
        
    def execute_once(self, fragrance_number):
        execute_cmd = '~execute_once\({}\) '.format(fragrance_number)
        cmd = self.command_header + self.include_cmd + execute_cmd + self.command_end
        print(cmd)

        self.send_serial_command(cmd)
    
    # Somehow this effects the servos
    def disable_system(self): 
        disable_system_cmd = '~system_power_off\(\) '
        cmd = self.command_header + self.include_cmd + disable_system_cmd + self.command_end
        print(cmd)
        self.send_serial_command(cmd)        
        
    def send_serial_command(self, cmd):
        os.system(cmd)
        
        
        
    def print_receipt(self, fragrance_number, username_str):
        # Select targtet receipt temp
        
        # Copy that picture(s) to a temp dir
        
        # Put current time and username on to the sheet
        
        # (Resize and )Generate .bmp file to < 570 x 1200
        
        # Call thermo printer object and print
        pass
    
    
if __name__ == '__main__':
    FD = Fragrance_Dispenser_The_Machine(port)
    
    # FD.system_go_home()
    # FD.disable_system()
    # FD.execute_once(4)
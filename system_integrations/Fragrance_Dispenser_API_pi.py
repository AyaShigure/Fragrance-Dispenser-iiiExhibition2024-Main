import os
import time
# from printer_class import *

pico_port = '/dev/ttyACM0'
printer_port = '/dev/usb/lp0' # The port will change depends on how many other device is pluged in


class Fragrance_Dispenser_The_Machine():
    def __init__(self, pico_port, printer_port):
        self.include_cmd = 'from\ Fragrance_Dispenser_API_pico\ import\ \* '
        self.command_header = 'rshell repl pyboard '
        self.command_end = '~1+1~'
        self.pico_port = pico_port
        self.printer_port = printer_port
        # self.printer = thermoPrinter(self.printer_port, './cpp_bin')

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

    def print_receipt(self):
        self.printer_port = self.printer_port
        script_path = os.getcwd()
        imgPath1 = f'{script_path}/media/output/toprint.bmp'
        imgPath2 = f'{script_path}/media/base/comment.bmp'
        self.printer.PrintRasterImage(imgPath1)
        self.printer.FeedAndHalfCut()
        self.printer.PrintRasterImage(imgPath2)
        self.printer.FeedAndFullCut()

if __name__ == '__main__':
    FD = Fragrance_Dispenser_The_Machine(pico_port, printer_port)
    # FD.print_receipt()
    FD.system_go_home()
    # FD.disable_system()
    # FD.execute_once(4)

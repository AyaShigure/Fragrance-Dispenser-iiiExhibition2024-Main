import pigpio
import time
from bcolors import bcolors
from fancy_print import *
import datetime

def PrintRPi4BHeader():
    headerString = '[' + 'Raspberry Pi 4B' + ' | '+ f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}' + '] '
    print_like_GPT(headerString + 'Initiallizing\n', bcolors.color256(fg=229))
    return headerString

def reboot_pico():
    # Reboot pico
    pi = pigpio.pi()

    if not pi.connected:
        print_like_GPT("Failed to connect to pigpio daemon.", bcolors.FAIL)
        exit()

    PICO_RESET_GPIO = 23

    pi.set_mode(PICO_RESET_GPIO, pigpio.OUTPUT)
    pi.write(PICO_RESET_GPIO, 0)
    time.sleep(0.5)
    pi.write(PICO_RESET_GPIO, 1)
    pi.stop()

    print_like_GPT(RPi4BHeaderString + "Pico has been reset via GPIO23.\n", bcolors.OKGREEN)
    time.sleep(0.5)




if __name__ == "__main__":
    RPi4BHeaderString = PrintRPi4BHeader()
    print_like_GPT(RPi4BHeaderString + 'Rebooting the RP2040\n', bcolors.color256(fg=229))
    reboot_pico()
    print_like_GPT(RPi4BHeaderString + "Done............\n", bcolors.color256(fg=229))

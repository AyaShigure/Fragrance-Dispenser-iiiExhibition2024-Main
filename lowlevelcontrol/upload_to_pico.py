import serial
import pigpio
import os
import time
from fancy_print import *
from bcolors import * 

# Utilities
def PrintRP2040Header():
    headerString = '[' + 'RP2040' + ' | '+ f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}' + '] '
    print_like_GPT(headerString + 'Initiallizing\n', bcolors.color256(fg=154))
    return headerString

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

def active_serial_monitor(port, headerString):
    time.sleep(2)
    ser = serial.Serial(port, 115200, timeout=1)

    print_like_GPT(headerString + " Listening to Pico output...\n\n",bcolors.WARNING)

    try:
        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').strip()
                print_like_GPT(headerString + f"{line}\n",  bcolors.color256(fg=154))
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        ser.close()

# To add: 
# 1. Delete all files on pico
# 2. Sync the file trees from local to pico

# Operation mode:
# Preset test system mode ( Move everything )
# Emergency stop


if __name__ == "__main__":
    os.system("clear")
    activate_serial_monitor = False
    port = '/dev/ttyACM0'

    RPi4BHeaderString = PrintRPi4BHeader()

    # Upload via rshell
    print_like_GPT(RPi4BHeaderString + 'Clearing the existing file tree.\n', bcolors.color256(fg=229))
    os.system(f"rshell -p {port} rm -r /pyboard/*")

    print_like_GPT(RPi4BHeaderString + 'Uploading the new file tree.\n', bcolors.color256(fg=229))
    os.system(f"rshell -p {port} rsync ./pico_src/ /pyboard/")
    # os.system(f"rshell -p {port} cp ./pico_src/main.py /pyboard/")
    print_like_GPT(RPi4BHeaderString + 'Rebooting the RP2040\n', bcolors.color256(fg=229))
    reboot_pico()
    print_like_GPT(RPi4BHeaderString + "Done............\n", bcolors.color256(fg=229))


    if activate_serial_monitor:
        os.system("clear")
        ascii_art = pyfiglet.figlet_format("Fragrance Dispenser", font="big")

        print_like_GPT(ascii_art)
        print()
        print_like_GPT('[Created by Kiki & Mo & Aya at The University of Tokyo]', bcolors.OKCYAN)
        print()

        RP2040headerString = PrintRP2040Header()
        active_serial_monitor(port, RP2040headerString)



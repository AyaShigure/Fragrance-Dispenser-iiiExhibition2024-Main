from .bcolors import *
import datetime
import time
import pyfiglet
import serial
import pigpio
import os
import sys


'''
    IMPORTANT:
        This function set is for RPi 4B to upload code under /pico_src to RP2040.
        Do not upload this file to RP2040.

'''
def fancy_print():
    ascii_art = pyfiglet.figlet_format("Fragrance Dispenser", font="big")
    print_like_GPT(ascii_art)
    print()
    print_like_GPT('[Created by Kiki & Mo & Aya at The University of Tokyo]', bcolors.OKCYAN)
    print()

# Utilities
def PrintRP2040Header():
    headerString = '[' + 'RP2040' + ' | '+ f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}' + '] '
    print_like_GPT(headerString + 'Initiallizing\n', bcolors.color256(fg=154))
    return headerString

def PrintRPi4BHeader():
    headerString = '[' + 'Raspberry Pi 4B' + ' | '+ f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}' + '] '
    print_like_GPT(headerString + 'Initiallizing\n', bcolors.color256(fg=229))
    return headerString


def reboot_pico(RPi4BHeaderString):
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


def print_like_GPT(text, color=bcolors.ENDC):
    for i,char in enumerate(text):
        print(f"{color}{char}\u2588{bcolors.ENDC}", end="", flush=True)
        time.sleep(0.003)

        if i < len(text) - 1:
            print('\b \b', end='', flush=True)
    time.sleep(0.5) 

    print('\b \b', end='', flush=True) 


def active_serial_monitor(port, headerString):
    time.sleep(2)
    ser = serial.Serial(port, 115200, timeout=1)

    print_like_GPT(headerString + "Ready...\n\n",bcolors.WARNING)

    try:
        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').strip()
                print_like_GPT(headerString + f"{line}\n",  bcolors.color256(fg=154))
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        ser.close()
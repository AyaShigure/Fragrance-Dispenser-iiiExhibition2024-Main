#!/usr/bin/env python3
from uploader_functions import *


if __name__ == "__main__":
    RPi4BHeaderString = PrintRPi4BHeader()
    print_like_GPT(RPi4BHeaderString + 'Rebooting the RP2040\n', bcolors.color256(fg=229))
    reboot_pico(RPi4BHeaderString)
    print_like_GPT(RPi4BHeaderString + "Done............\n", bcolors.color256(fg=229))


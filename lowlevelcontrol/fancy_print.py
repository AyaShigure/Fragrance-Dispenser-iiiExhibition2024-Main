import pyfiglet
import time
from bcolors import bcolors


def print_like_GPT(text, color=bcolors.ENDC):
    for i,char in enumerate(text):
        print(f"{color}{char}\u2588{bcolors.ENDC}", end="", flush=True)
        time.sleep(0.005)

        if i < len(text) - 1:
            print('\b \b', end='', flush=True)
    time.sleep(0.5) 

    print('\b \b', end='', flush=True) 

if __name__ == "__main__":
    ascii_art = pyfiglet.figlet_format("Fragrance Dispenser", font="big")
    print_like_GPT(ascii_art)
    print()
    print_like_GPT('[Created by Kiki & Mo & Aya at The University of Tokyo]', bcolors.OKCYAN)
    print()

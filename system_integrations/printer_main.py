#!/usr/bin/env python3
from printer_class import *


if __name__ == '__main__':
    # Text to print
#    port = '/dev/usb/lp0'
    port = '/dev/usb/lp0' # The port will change depends on how many other device is pluged in
    cpp_bin_path = './cpp_bin'

    string_to_print_pt1 = '''There is no end though there is a start in space. ---Infinity.
宇宙に始まりはあるが、終わりはない。　---無限\n'''

    string_to_print_pt2 = '''It has own power, it ruins, and it goes though there is a start also in the star. ---Finite.
星にもまた始まりはあるが、自らの力をもって滅び逝く。　---有限\n'''

    string_to_print_pt3 = '''Only the person who was wisdom can read the most foolish one from the history.
英知を持つ者こそ、最も愚かであること。歴史からも読み取れる。\n'''

    string_to_print_pt4 = '''The fish that lives in the sea doesn't know the world in the land. It also ruins and goes if they have wisdom.
海に生ける魚は、陸の世界を知らない。彼らが英知を持てば、それもまた滅び逝く。\n'''

    string_to_print_pt5 = '''It is funnier that man exceeds the speed of light than fish start living in the land.
人間が光の速さを超えるのは、魚たちが陸で生活を始めるよりも滑稽。\n'''

    string_to_print_pt6 = ''' It can be said that this is an final ultimatum from the god to the people who can fight.
これは抗える者たちに対する、神からの最後通告とも言えよう。'''
    
    # Image to print
    script_path = '/home/ubuntu/fragrance_dispenser/system_integrations'
    # imgPath = f'{script_path}/media/logo.bmp'
    # imgPath = f'{script_path}/media/test_5.bmp'
    imgPath1 = f'{script_path}/media/output/toprint.bmp'
    imgPath2 = f'{script_path}/media/tk02.bmp'

    print(imgPath1)
    print(imgPath2)

    # Printer object
    printer = thermoPrinter(port, cpp_bin_path)

    # Execute prints
    # printer.FeedLines(3)
    # printer.FeedAndHalfCut()
    # printer.FeedLines(1)


    # printer.PrintTextUTF8('================================================')
    # printer.FeedLines(1)
    # printer.PrintTextUTF8(string_to_print_pt1)
    # printer.PrintTextUTF8(string_to_print_pt2)
    # printer.PrintTextUTF8(string_to_print_pt3)
    # printer.PrintTextUTF8(string_to_print_pt4)
    # printer.PrintTextUTF8(string_to_print_pt5)
    # printer.PrintTextUTF8(string_to_print_pt6)
    # printer.FeedLines(1)
    # printer.PrintTextUTF8('================================================')
    # printer.FeedLines(1)
    # printer.PrintRasterImage(imgPath)
    # printer.FeedLines(1)
    # printer.PrintTextUTF8('================================================')
    # printer.FeedLines(3)
    printer.PrintRasterImage(imgPath1)
    printer.FeedAndHalfCut()
    printer.PrintRasterImage(imgPath2)
    printer.FeedAndFullCut()

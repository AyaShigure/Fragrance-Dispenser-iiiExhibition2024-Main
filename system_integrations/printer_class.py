import os

class thermoPrinter():
    def __init__(self, port, cpp_bin_path):
        self.port = port
        self.cpp_bin_path = cpp_bin_path
        pass

    def FeedAndFullCut(self):    
        print('Feeding & executing a full cut.')
        os.system(f'sudo box64 {self.cpp_bin_path}/FeedAndFullCut {self.port}')

    def FeedAndHalfCut(self):
        print('Feeding & execut a half cut.')
        os.system(f'sudo box64 {self.cpp_bin_path}/FeedAndHalfCut {self.port}')

    def FeedDot(self, feed_dots_number):
        print(f'Feeding {feed_dots_number} pixels.')
        os.system(f'sudo box64 {self.cpp_bin_path}/FeedDot {self.port} {feed_dots_number}')

    def FeedLines(self, feed_lines_number):
        print(f'Feeding {feed_lines_number} lines.')
        os.system(f'sudo box64 {self.cpp_bin_path}/FeedLines {self.port} {feed_lines_number}')

    def PrintHorizontalLineSpecifyThickness(self, startPoint, endPoint, lineThickness):
        os.system(f'sudo box64 {self.cpp_bin_path}/PrintHorizontalLineSpecifyThickness {self.port} {startPoint} {endPoint} {lineThickness}')

    def PrintSelftest(self):
        os.system(f'sudo box64 {self.cpp_bin_path}/PrintSelftest {self.port}')

    def PrintRasterImage(self, imgPath):
        print('Printing target .bmp file. (Note that the imgPath should be a absolute path)')
        os.system(f'sudo box64 {self.cpp_bin_path}/PrintRasterImage {self.port} \"{imgPath}\"')

    def PrintTextUTF8(self, str):
        print('Printing.')
        os.system(f'sudo box64 {self.cpp_bin_path}/PrintTextUTF8 {self.port} \"{str}\n\"')

class FileReader:
    def __init__(self):
        self.file = open('input.txt', 'r')
        self.line_number = 0
        self.pointer = 0
        self.start = 0
        self.current_line = ""
        self.is_start = True
        self.is_end = False

    def read_line(self):
        self.is_start = False
        c = self.file.readline()
        if c != "":
            self.current_line = c
            self.line_number += 1
            self.start = 0
            self.pointer = 0
        else:
            self.is_end = True

    def read_char(self):  #maybe backward gonna fail after this aproach
        if self.pointer == len(self.current_line):
            self.read_line()
        if self.is_end:
            return 'end'
        x = self.current_line[self.pointer]
        self.pointer += 1
        return x

    def backward(self):
        self.pointer = self.pointer - 1

    def return_token(self):
        z = self.start
        self.start = self.pointer
        return self.current_line[z:self.pointer]
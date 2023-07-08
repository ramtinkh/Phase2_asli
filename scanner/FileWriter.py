class FileWriter:
    def __init__(self):
        self.symbol_table = ["if", "else", "void", "int", "repeat", "break", "until", "return"]
        self.index=100
        self.addresses = {}
        self.tokens = {}
        self.errors = {}
        self.mainAdd = 0
        self.addresses["main"]=[0]
        self.addresses["output"]=[2000]
    def add_symbol(self, name):
        if name not in self.symbol_table:
            if name == "main":
                self.addresses["main"][0]=self.index
            if name == "output":
                return
            else:
                self.addresses[name]=[self.index]
            if name == "main":
                self.mainAdd = self.index
                print("main add", self.mainAdd)
            if(name != "output"):
                self.symbol_table.append(name)
                self.index+=4


    def add_tokens(self, token, type, line_number):
        line_number = str(line_number)
        if self.tokens.get(line_number) is None:
            self.tokens[line_number] = []
        self.tokens[line_number].append([token, type])

    def add_errors(self, token, error_type,  line_number):
        line_number = str(line_number)
        if self.errors.get(line_number) is None:
            self.errors[line_number] = []
        self.errors[line_number].append([token, error_type.error_to_string()])

    def file_writer_tokens(self):
        file1 = open("tokens.txt","w+")
        tokens = ""
        for x in self.tokens.keys():
            tokens+=f"{x}.\t"
            for y in self.tokens[x]:
                tokens += f"({y[1]}, {y[0]}) "
            tokens+='\n'
        # print(tokens)
        file1.write(tokens)
        file1.close()


    def file_writer_symboltable(self):
        file1 = open("symbol_table.txt", "w+")
        symbols = ""
        for i, x in enumerate(self.symbol_table):
            symbols += f"{i+1}.\t{x}\n"
        # print(symbols)
        file1.write(symbols)
        file1.close()

    def file_writer_errors(self):
        file1 = open("lexical_errors.txt", "w+")
        error = ""
        for x in self.errors.keys():
            error+=f"{x}.\t"
            for y in self.errors[x]:
                error += f"({y[0]}, {y[1]}) "
            error += '\n'
        if error == "":
            error = "There is no lexical error."
        # print(error)
        file1.write(error)
        file1.close()


# fw = FileWriter()
# fw.add_tokens( "as" , "id" , 3)
# fw.add_tokens( "df" , "id" , 3)
# fw.add_tokens( "gh" , "id" , 3)
# fw.add_tokens( "dagfhdr" , "id" , 5)
# print(fw.tokens)



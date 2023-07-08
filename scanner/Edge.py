class Edge:

    def __init__(self):
        self.is_include = True
        #self.is_exclude = False
        self.include_edges = []
        self.exclude_edges = []
        self.language_chars=[]
        #self.language_valid_chars()

    def add_to_includes(self, first, last=-1):
        if last == -1:
            last = first
        self.include_edges.append([first, last])

    def add_to_exclude(self, first, last=-1):
        if last == -1:
            last = first
        self.exclude_edges.append([first, last])

    def if_in_include(self , char):
        for x in self.include_edges:
            first = x[0]
            last = x[1]
            if char>=first and char<=last:
                return True
        return False

    def if_in_exclude(self , char):
        if char == 'end':
            return True
        for y in self.exclude_edges:
            first = y[0]
            last = y[1]
            if (first <= char <= last):
                return False
        if self.language_valid_chars(char):
            return True
        return False

    def language_valid_chars(self,char):
        if (char>="0" and char<="9"):
            return True
        if (char>="a" and char<="z"):
            return True
        if(char>="A" and char<="Z"):
            return True
        if (char==";" or char=="," or char=="[" or char=="]" or char=="(" or char==")" or char=="{" or char=="}" or
                char=="+" or char=="-" or char=="*" or char=="<" or char==" " or char=="\n" or char=="\r"
                or char=="\t" or char=="\f" or char=="\v" or char=='end' or char=='='):
                return True
        return False

    def is_have(self, char):
        if self.is_include:
            return self.if_in_include(char)
        else:
            return self.if_in_exclude(char)
# fr=Edge()
# #print(fr.language_valid_chars("$"))
# print(fr.language_valid_chars('end'))





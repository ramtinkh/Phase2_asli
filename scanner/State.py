class State:
    def __init__(self, id=0):
        self.next_states = []
        self.id = id
        self.is_final_state = False
        self.is_error_state = False
        self.is_backward_state = False
        self.is_error_type = False
        self.string = ""
        self.keywords = ["if", "else", "void", "int", "repeat", "break", "until", "return"]


    def add_next_state(self,state,edge):
        self.next_states.append([state, edge])

    def find_next_state(self,char):
        for x in self.next_states:
            new = x[0]
            if x[1].is_have(char):
                if char == 'eof':
                    pass
                elif x[0] == 203 or x[0] == 0:
                    self.string = f"{char}"
                else :
                    self.string += char
                new.string = self.string
                # print("inja     ", new.string)
                return new

    def is_keyword(self, token1):
        if token1 in self.keywords:
            return True
        return False

    def final_state_to_string(self, token=None):
        if self.id == 2:
            if token is not None:
                if self.is_keyword(token):
                    return "KEYWORD"
            return "ID"
        if self.id == 4:
            return "NUM"
        if self.id == 5 or self.id == 6 or self.id == 7 or self.id == 9:
            return "SYMBOL"

    def __str__(self):
        return str(self.id)


            #todo: check if char is in edge

    def error_to_string(self):
        if self.id == 101:
           return "Invalid input"
        if self.id == 102:
           return "Invalid number"
        if self.id == 103:
           return "Unmatched comment"
        if self.id == 104:
           return "Unclosed comment"
        #todo
        ...
from scanner.FileReader import FileReader
from scanner.FileWriter import FileWriter
from scanner.State import State
from scanner.Dfa import Dfa
from scanner.Edge import Edge


class Scanner:
    def __init__(self):
        self.file_reader = FileReader()
        self.file_writer = FileWriter()
        self.dfa = Dfa()
        self.state = self.dfa.first_state
        self.x = self.file_reader.read_char()
        self.counter_comment = 0
        self.backup_comment = ""
        self.comment_start_line = -1
        self.last_char = self.x

    def run(self):
        while True:
            next_state = self.state.find_next_state(self.x)
            #print(next_state)
            if next_state is None and self.state.is_error_state is False:
                if self.state.id == 202 or self.state.id == 204:
                    next_state = self.state
                else:
                    next_state = self.dfa.states[-1]
                    next_state.is_backward_state = False
                    if self.file_reader.pointer - self.file_reader.start == 2 and self.last_char == '/':
                        next_state.is_backward_state = True
            self.state = next_state
           # print(self.x, end='  ')
           #  print(self.state)
            if self.state.is_final_state:
                if self.state.id == 203:
                    self.counter_comment = 0
                    self.backup_comment = ""
                # if state.id == 2:
                if self.state.is_backward_state and self.x != 'end':
                    self.file_reader.backward()
                token1 = self.file_reader.return_token()
                # print("hellooo", token1)
                if self.state.id == 2:
                    self.file_writer.add_symbol(token1)
                if self.state.id != 206 and self.state.id != 203:
                    # print("_____ ",self.state.id, self.file_reader.line_number, token1,end='\n')
                    self.file_writer.add_tokens(token1, self.state.final_state_to_string(token1), self.file_reader.line_number)
                    return [token1, self.state.final_state_to_string(token1), self.file_reader.line_number]
                self.state = self.dfa.first_state
            if self.state.is_error_type:
                if self.state.is_backward_state and self.x != 'end':
                    self.file_reader.backward()
                token_error = self.file_reader.return_token()
                if token_error != ' ' and token_error != '\n' and token_error != '':
                    # print('error', file_reader.line_number, token_error,end='\n')
                    self.file_writer.add_errors(token_error, self.state, self.file_reader.line_number)
                self.state = self.dfa.first_state
            # print(self.x)
            if self.x == 'end':
                if self.file_reader.line_number == 8:
                    return ['$', 'SYMBOL', self.file_reader.line_number + 1]
                else:
                    return ['$', 'SYMBOL', self.file_reader.line_number]
            self.last_char = self.x
            self.x = self.file_reader.read_char()
            if self.state.id == 204 or self.state.id == 205:

                if self.state.id == 204 and self.counter_comment == 0:
                    self.comment_start_line = self.file_reader.line_number
                if self.x == 'end':
                    # print('error', backup_comment, comment_start_line)
                    state_104 = State(104)
                    token2 = '/*' + self.backup_comment
                    if self.counter_comment == 5:
                        token2 += '...'
                    self.file_writer.add_errors(token2, state_104, self.comment_start_line)
                if self.counter_comment < 5:
                    self.backup_comment += self.x
                    self.counter_comment += 1

# for self.x in self.file_writer.tokens.keys():
#     print(self.x)
#     print(self.file_writer.tokens[self.x])
# self.file_writer.self.file_writer_errors()
# self.file_writer.self.file_writer_symboltable()
# self.file_writer.self.file_writer_tokens()
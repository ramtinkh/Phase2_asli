class Node:
    def __init__(self, is_final=False, action=''):
        self.next = []
        self.is_final = is_final
        self.action=action

    def add_next(self, node, edge):
        self.next.append([node, edge])

    def find_next(self, look_ahead):
        next_line = look_ahead[2]
        if look_ahead[1] == 'NUM' or look_ahead[1] == 'ID':
            char = look_ahead[1]
        else:
            char = look_ahead[0]
        for next1 in self.next:
            edge_tmp = next1[1]
            if edge_tmp.contain(char):
                return next1

        return self.find_error(char, next_line)

    def find_error(self, char, next_line):
        for next1 in self.next:
            edge_tmp = next1[1]
            if not next1[1].is_terminal:
                if edge_tmp.is_in_follow(char):
                    return [f'#{next_line} : syntax error, missing {edge_tmp.id}', 1]
                return [f'#{next_line} : syntax error, illegal {char}', 2]
            else:
                return [f'#{next_line} : syntax error, missing {edge_tmp.id}', 3]



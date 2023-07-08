class Edge:
    def __init__(self, id, grammar1, is_terminal=False):
        self.id = id
        if not is_terminal:
            self.first = grammar1.firsts[id]
            self.follow = grammar1.follows[id]
        self.is_terminal = is_terminal

    def is_in_follow(self, char):
        if not self.is_terminal:
            if char in self.follow:
                return True
        return False

    def contain(self, char):
        #check token type
        if not self.is_terminal:
            if char in self.first:
                return True
            if 'ε' in self.first:
                if char in self.follow:
                    return True
        else:
            if char == self.id:
                return True # id e edge??
            if self.id == 'ε':
                #print('hi')
                return True

        return False

# grammar=Grammar()
# # a=grammar.follows['Statement']
# # print(a)
# edge = Edge('Statement')

import json

from parsr.Edge import Edge
from parsr.Diagram import Diagram
from parsr.Node import Node

class Grammar:
    def __init__(self, scanner, code_generator):
        self.firsts = {}
        self.follows = {}

        self.make_error = ""
        self.end_error = False

        self.diagrams = []
        self.edges = {}
        self.is_error = False
        self.terminals = ['ID', ';', '[', 'NUM', ']', '(', ')', 'int', 'void', ',', '{', '}', 'break', 'if', 'else',
                          'repeat', 'until', 'return', '=', '<', '==', '+', '-', '*', 'ε', '$']

        self.code_generator = code_generator
        self.scanner = scanner
        self.lookahead = self.scanner.run()

        self.non_terminals = self.non_terminal_maker()
        self.make_firsts()
        self.make_follows()
        self.edges_creator()
        self.create_diagrams()
        self.diagrams[0].run_diagram()

    def add_error(self, error):
        if not self.end_error:
            self.make_error += error
            self.make_error += '\n'
        if len(error.split()) > 5 and error.split()[5] == "EOF":
            self.end_error = True

    def make_error_file(self):
        with open("syntax_errors.txt", "w", encoding="utf-8") as file:
            if self.make_error == "":
                self.make_error = "There is no syntax error."
            file.write(self.make_error)

    def non_terminal_maker(self):
        grammars_file = open("parsr/grammars.json")
        grammar_nums = json.load(grammars_file)
        grammars_file.close()
        non_terminals = []
        for key in grammar_nums.keys():
            non_terminals.append(key)
        return non_terminals

    def read_lookahead(self):
        self.scanner.run()

    def make_firsts(self):
        first_file = open("parsr/firsts.json")
        firsts = json.load(first_file)
        first_file.close()
        for key in firsts.keys():
            self.firsts[key] = firsts[key]

    def make_follows(self):
        follow_file = open("parsr/follows.json")
        follows = json.load(follow_file)
        follow_file.close()
        for key in follows.keys():
            self.follows[key] = follows[key]

    def edges_creator(self):
        for name_1 in self.terminals:
            self.edges[name_1] = Edge(name_1, self, is_terminal=True)

        for name_1 in self.non_terminals:
            # print(name_1)
            self.edges[name_1] = Edge(name_1, self, is_terminal=False)

    def create_diagrams(self):
        file = open("parsr/grammar.txt", "r", encoding="utf-8")
        for i in range(44):
            line = file.readline()
            names = line.split()
            node0 = Node()
            node_final = Node(True)
            current_node = node0
            # E' -> + T E' | ebsilon
            for j in range(2, len(names)):

                # if names[j+1][0]=='#'

                if names[j][0] == '#':  # new
                    # current_node.action=names[j][1:]
                    # if j >= len(names)-1:
                    #     new_node = node_final
                    # elif names[j+1] == "|":
                    #     new_node = node_final
                    # else:
                    #     new_node = Node()
                    # current_node.add_next(new_node,self.edges['ε'])
                    # current_node=new_node
                    node1 = Node()
                    node1.action = names[j][1:]
                    index = j
                    while index < len(names) - 1 and names[index][0] == "#":
                        index += 1
                    if index == len(names) - 1 or names[index] == "|":
                        current_node.add_next(node1, self.edges['ε'])
                    else:
                        current_node.add_next(node1, self.edges[names[index]])
                    current_node = node1

                    if j >= len(names) - 1:
                        new_node = node_final
                    elif names[j + 1] == "|":
                        new_node = node_final
                    else:
                        new_node = Node()
                    current_node.add_next(new_node, self.edges['ε'])
                    current_node = new_node

                elif names[j] != "|":
                    if names[j] == 'EPSILON':
                        names[j] = 'ε'
                    new_edge = self.edges[names[j]]
                    if j >= len(names) - 1:
                        new_node = node_final
                    elif names[j + 1] == "|":
                        new_node = node_final
                    else:
                        new_node = Node()
                    current_node.add_next(new_node, new_edge)
                    current_node = new_node
                else:
                    current_node = node0
            Diagram(names[0], node0, self)

# grammar=Grammar()
# a=grammar.firsts['Declaration-list']
# print(a)
import copy
import anytree


class Diagram:
    def __init__(self, id1, node, grammar):
        self.id = id1
        self.first_node = node
        self.current_node = None
        self.current_edge = None
        self.grammar = grammar
        self.grammar.diagrams.append(self)

        self.any_tree_parent = None
        self.any_tree_node = None

    def find_state(self):
        if self.grammar.lookahead[0] == '':
            self.grammar.lookahead = self.grammar.scanner.run()
        # print(self.current_node.find_next(self.grammar.lookahead))
        error1 = 'missing A1 on line'
        error2 = 'illegal a found on line'
        error3 = 'missing b on line'
        # print(self.current_node.find_next(self.grammar.lookahead), 200)
        # print(self.grammar.lookahead, 888)
        next_state = self.current_node.find_next(self.grammar.lookahead)
        if type(next_state[0]) is str:
            # print(self.grammar.lookahead[0] != '')
            # print(next_state[0])
            self.grammar.add_error(next_state[0])
            if next_state[1] == 1:
                self.grammar.is_error=True
                a = self.current_node.next[0]
            elif next_state[1] == 2:
                self.grammar.is_error = True
                self.grammar.lookahead = self.grammar.scanner.run()
                # if self.grammar.lookahead[0] == '':
                #     self.grammar.lookahead = self.grammar.scanner.run()
                if not self.grammar.lookahead[0] == "$":
                    a = self.find_state()
                else:
                    return None
            elif next_state[1] == 3:
                # print(self.id)
                self.grammar.is_error = True
                # print(next_state)
                a = self.current_node.next[0]
        else:
            a = self.current_node.find_next(self.grammar.lookahead)
        # print("a injas",a)
        return a

    def match(self, edge):
        look_ahead = self.grammar.lookahead
        if look_ahead[1] == 'NUM' or look_ahead[1] == 'ID':
            char = look_ahead[1]
        else:
            char = look_ahead[0]
        if edge.id == char:
            if not self.grammar.end_error:
                if look_ahead[0] != '$':
                    anytree.Node(f"({look_ahead[1]}, {look_ahead[0]})", parent=self.any_tree_node)
                else:
                    anytree.Node(f"$", parent=self.any_tree_node)
            # print(char+'\n')
            # print( edge.id, char, self.grammar.lookahead)
            if self.current_node.action == "":
                self.grammar.lookahead = self.grammar.scanner.run()

        else:
            # print('error', edge.id, char, self.grammar.lookahead)
            pass

    def run_diagram(self, parent=None):
        if self.grammar.end_error:
            return
        if parent is None:
            self.any_tree_node = anytree.Node(self.id)
        else:
            self.any_tree_parent = parent
            self.any_tree_node = anytree.Node(self.id, parent=parent)

        self.current_node = self.first_node
        while not self.current_node.is_final:
            a = self.find_state()

            if a is None:
                self.grammar.add_error(f'#{self.grammar.lookahead[2]} : syntax error, Unexpected EOF')
                return
            # print(a, self.grammar.lookahead)
            #print(5555)
            self.current_node = a[0]
            self.current_edge = a[1]
            # print(a[1].id)
            #print(a[1].id, self.grammar.lookahead)
            # print(7, a[1].id, a[0].is_final)
            # print(7, a[1].id, a[0].is_final)
            if self.current_node.action != '':  # new
                print(self.current_node.action)
                self.grammar.code_generator.find_action(self.current_node.action, self.grammar.lookahead)
            if a[1].id == 'ε':
                anytree.Node("epsilon", self.any_tree_node)
            elif a[1].id[0] == '#':
                print("salam")
                continue
            elif a[1].is_terminal:
                self.match(a[1])
            else:
                look_ahead = self.grammar.lookahead
                if look_ahead[1] == 'NUM' or look_ahead[1] == 'ID':
                    char = look_ahead[1]
                else:
                    char = look_ahead[0]
                if self.current_edge.contain(char):
                    for dia in self.grammar.diagrams:
                        if dia.id == a[1].id:
                            # print(11, dia.id)
                            # print(char)
                            dia1 = copy.copy(dia)
                            # print(88, self.current_edge.id, self.current_node.action)
                            if self.current_node.action == "":
                                dia1.run_diagram(self.any_tree_node)
                            # print(12, self.id)
        result = ""
        with open("parse_tree.txt", "+w", encoding="utf-8") as file:
            if self.any_tree_parent is None:
                for pre, fill, node in anytree.RenderTree(self.any_tree_node):
                    result += "%s%s" % (pre, node.name)
                    if node.name != "$":
                        result += '\n'
            file.write(result)

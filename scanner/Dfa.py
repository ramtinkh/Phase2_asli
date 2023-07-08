from scanner.State import State
from scanner.Edge import Edge
class Dfa:
    def __init__(self):
        self.first_state = State(0)
        self.states = [self.first_state]
        self.build_dfa()
        state_101 = State(101)
        state_101.is_error_type = True
        # state_101.is_backward_state
        self.states.append(state_101)

    def build_dfa(self):
        #KEYWORD
        state_1=State(1)
        self.states.append(state_1)
        edge01=Edge()
        edge01.add_to_includes("a","z")
        edge01.add_to_includes("A","Z")
        self.first_state.add_next_state(state_1,edge01)
        edge11= Edge()
        edge11.add_to_includes("a","z")
        edge11.add_to_includes("A","Z")
        edge11.add_to_includes("0","9")
        state_1.add_next_state(state_1,edge11)
        state_2 = State(2)
        self.states.append(state_2)
        state_2.is_final_state = True
        state_2.is_backward_state = True
        edge12 = Edge()
        edge12.is_include=False
        edge12.add_to_exclude("0","9")
        edge12.add_to_exclude("a","z")
        edge12.add_to_exclude("A","Z")
        state_1.add_next_state(state_2,edge12)
        #NUMBER
        state_3=State(3)
        self.states.append(state_3)
        edge03 = Edge()
        edge03.add_to_includes("0","9")
        self.first_state.add_next_state(state_3,edge03)
        state_3.add_next_state(state_3,edge03)
        state_4=State(4)
        self.states.append(state_4)
        state_4.is_final_state = True
        state_4.is_backward_state = True
        edge34 = Edge()
        edge34.is_include = False
        edge34.add_to_exclude("0", "9")
        edge34.add_to_exclude("a", "z")
        edge34.add_to_exclude("A", "Z")
        state_3.add_next_state(state_4, edge34)
        #invalid number error
        state_102 = State(102)
        state_102.is_error_type = True
        self.states.append(state_102)
        edge_invalid_number = Edge()
        edge_invalid_number.add_to_includes("a","z")
        edge_invalid_number.add_to_includes("A","Z")
        state_3.add_next_state(state_102,edge_invalid_number)
        #Symbol
        state_5 = State(5)
        self.states.append(state_5)
        state_5.is_final_state = True
        edge05 = Edge()
        edge05.add_to_includes(";")
        edge05.add_to_includes(",")
        edge05.add_to_includes("[")
        edge05.add_to_includes("]")
        edge05.add_to_includes("(")
        edge05.add_to_includes(")")
        edge05.add_to_includes("{")
        edge05.add_to_includes("}")
        edge05.add_to_includes("+")
        edge05.add_to_includes("-")
        edge05.add_to_includes("<")
        self.first_state.add_next_state(state_5, edge05)
        state_6 = State(6)
        self.states.append(state_6)
        edge06 = Edge()
        edge06.add_to_includes("=")
        self.first_state.add_next_state(state_6,edge06)
        state_7 = State(7)
        self.states.append(state_7)
        state_7.is_final_state = True
        edge67 = Edge()
        edge67.add_to_includes("=")
        state_6.add_next_state(state_7, edge67)
        state_8 = State(8)
        self.states.append(state_8)
        edge08 = Edge()
        edge08.add_to_includes("*")
        self.first_state.add_next_state(state_8, edge08)
        state_9 = State(9)
        self.states.append(state_9)
        state_9.is_backward_state = True
        state_9.is_final_state = True
        edge69 = Edge()
        edge69.is_include = False
        edge69.add_to_exclude("=")
        state_6.add_next_state(state_9, edge69)
        edge89 = Edge()
        edge89.is_include = False
        edge89.add_to_exclude("/")
        state_8.add_next_state(state_9, edge89)


        # unmatched comment error
        edge_unmatched_comment = Edge()
        edge_unmatched_comment.add_to_includes("/")
        state_103 = State(103)
        state_103.is_error_type = True
        self.states.append(state_103)
        state_8.add_next_state(state_103,edge_unmatched_comment)
        #white space
        state_206 = State(206)
        self.states.append(state_206)
        state_206.is_final_state = True
        edge0206 = Edge()
        edge0206.add_to_includes(" ")
        edge0206.add_to_includes("\n")
        edge0206.add_to_includes("\r")
        edge0206.add_to_includes("\t")
        edge0206.add_to_includes("\v")
        edge0206.add_to_includes("\f")
        self.first_state.add_next_state(state_206, edge0206)
        #comment
        state_201 = State(201)
        self.states.append(state_201)
        edge0201 = Edge()
        edge0201.add_to_includes("/")
        self.first_state.add_next_state(state_201,edge0201)
        state_202 = State(202)
        self.states.append(state_202)
        edge202202 = Edge()
        edge202202.is_include = False
        edge202202.add_to_exclude("\n")
        state_202.add_next_state(state_202,edge202202)
        state_202.is_final_state = True
        state_203 = State(203)
        self.states.append(state_203)
        state_203.is_final_state = True
        edge202203 = Edge()
        edge202203.add_to_includes("\n")
        state_202.add_next_state(state_203,edge202203)
        state_204 = State(204)
        self.states.append(state_204)
        edge201204 = Edge()
        edge201204.add_to_includes("*")
        state_201.add_next_state(state_204,edge201204)
        edge204204 = Edge()
        edge204204.is_include = False
        edge204204.add_to_exclude("*")
        state_204.add_next_state(state_204,edge204204)
        state_205 = State(205)
        self.states.append(state_205)
        state_204.add_next_state(state_205,edge201204)
        state_205.add_next_state(state_205,edge201204)
        edge204205 = Edge()
        edge204205.is_include = False
        edge204205.add_to_exclude("*")
        edge204205.add_to_exclude("/")
        state_205.add_next_state(state_204, edge204205)
        state_205.add_next_state(state_203,edge0201)


# dfa = Dfa()
# dfa.build_dfa()
# for x in dfa.states:
#     print(x)
#     for y in x.next_states:
#         print(y[0], end=' ')
#     print()
# edge = Edge()
# edge.is_include = False
# edge.add_to_includes('2', '5')
# edge.add_to_exclude('a', 'x')
# print(edge.if_in_exclude('z'))











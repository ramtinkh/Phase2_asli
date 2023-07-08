from codeGenerator.Function import Function

class CodeGenerator:

    def __init__(self, addresses, mainAdd):
        self.stack = []
        self.pb = []
        self.dataIn = 100
        self.temperoryIn = 500
        self.addresses = addresses
        self.arrayAddresses = {}
        self.indexArray = 700
        self.function_arr = []
        self.numberfunction = 0
        self.isfunction = False
        self.breakaddresses = []
        self.mainAdd = mainAdd
        self.isInOutput = False
        self.funCall = -1
        self.whattoreturn = []
        self.tmp = 2400
        self.isvoid = False
        self.lastindirect=0
        self.start=0
        self.atsign = False
    def funcIndirectAdd(self):
        x = self.lastindirect
        self.lastindirect += 4
        return x

    def find_action(self, action, lookahead):
        # print("stack is",self.stack)
        # print('#', action)
        # print(222, lookahead)
        if action == "start":
            self.start_code()
        if action == "checkvoid":
            self.checkvoid()
        if action == "define_id":
            self.define_id(lookahead)
        if action == "end":
            self.end()
        if action == "pnum":
            self.pnum(lookahead)
        if action == "define_array":
            self.define_array()
        if action == "save":
            self.save()
        if action == "jpf":
            self.jpf()
        if action == "jpfsave":
            self.jpfsave()
        if action == "jp":
            self.jp()
        if action == "until":
            self.until()
        if action == "pid":
            self.pid(lookahead)
        if action == "assign":
            self.assign()
        if action == "parray":
            self.parray(lookahead)
        if action == "operation":
            self.operation_()
        if action == "output":
            self.output()
        if action == "label":
            self.label()
        if action == "before_dec_func":
            self.before_dec_func()
        if action == "after_dec_func":
            self.after_dec_func()
        if action == "argument":
            self.argument()
        if action == "returns":
            self.returns()
        if action == "parguments":
            self.parguments()
        if action == "pfunction":
            self.pfunction()
        if action == "findfunction":
            self.findfunction()
        if action == "breakhandle":
            self.breakhandle()
        if action == "arrayinfunction":
            self.arrayinfunction()
        # if action == "endfunction":
        #     self.endfunction()

    def breakhandle(self):
        self.breakaddresses.append(len(self.pb))
        self.pb.append(" ")

    def start_code(self):
        self.pb.append(f"(ASSIGN, #4, 0,   )")
        self.start=len(self.pb)
        self.pb.append("start")

    def gettemp(self):
        tmp = self.temperoryIn
        self.temperoryIn += 4
        return tmp

    def checkvoid(self):
        print("vdvwrv")
        self.isvoid = True

    def pnum(self, lookahead):
        if(lookahead[0]=='+'):
            operation="ADD"
            self.stack.append(operation)
        elif (lookahead[0] == '-'):
            operation="SUB"
            self.stack.append(operation)
        elif (lookahead[0] == '*'):
            operation="MULT"
            self.stack.append(operation)
        elif (lookahead[0] == '<'):
            operation="LT"
            self.stack.append(operation)
        elif (lookahead[0] == '=='):
            operation="EQ"
            self.stack.append(operation)
        else:
            self.stack.append(f"#{lookahead[0]}")

    def end(self):
        print("STACK BEFORE END", self.stack)
        self.stack.pop()

    def define_id(self,lookahead): #??
        # print(33,self.addresses, lookahead)
        if lookahead[0]=="main":
            self.pb[self.start]=f"(JP, {len(self.pb)},  ,   )"
        if self.isfunction == False or self.addresses[lookahead[0]][0]==2000:
            self.pb.append(f"(ASSIGN, #0, {self.addresses[lookahead[0]][0]},   )")
            self.stack.append(self.addresses[lookahead[0]][0])
        else:
            self.pb.append(f"(ASSIGN, #0, {self.addresses[lookahead[0]][0] + 800 + 120 * self.numberfunction } ,   )")
            self.stack.append(self.addresses[lookahead[0]][0] + 800 + 120 * self.numberfunction)
            self.function_arr[-1].variablesAndAdds[lookahead[0]] = [self.addresses[lookahead[0]][0] + 800 + 120 * self.numberfunction]

    def pid(self,lookahead):
        if self.isfunction == False or self.addresses[lookahead[0]][0] == 2000:
            self.stack.append(self.addresses[lookahead[0]][0])
        else:
            if lookahead[0] in self.function_arr[-1].variablesAndAdds:
                self.stack.append(self.addresses[lookahead[0]][0] + 800 + 120 * self.numberfunction)
            else:
                self.stack.append(self.addresses[lookahead[0]][0])

    def define_array(self):
        tmpLenArray = self.stack.pop()
        lenArray = int(tmpLenArray[1:])
        array_add = self.stack.pop()
        self.arrayAddresses[array_add] = [self.indexArray]
        for i in range(lenArray):
            self.pb.append(f"(ASSIGN, #0, {self.indexArray},   )")
            self.indexArray += 4

    def arrayinfunction(self):
        self.function_arr[-1].arrayadds.append(self.stack[-1])

    def parray(self, lookahead):
        tmpIndexArray = self.stack.pop()
        lenIndexArray = tmpIndexArray
        array_add = self.stack.pop()
        temp1 = self.gettemp()
        temp2 = self.gettemp()
        print(self.function_arr[-1].inArgs)
        if [array_add, True] in self.function_arr[-1].inArgs and self.function_arr[-1].id != self.addresses["main"][0]:
            self.pb.append(f"(MULT, #4, {lenIndexArray}, {temp1} )")
            self.pb.append(f"(ADD, {array_add}, {temp1}, {temp1} )")
            print(self.atsign)
            if 'x' in self.addresses:
                if self.addresses['x'][0] == 100:
                    self.stack.append(f"{temp1}")
            else:
                self.stack.append(f"@{temp1}")
        else:
            tmpAddress = self.arrayAddresses[array_add][0]
            self.pb.append(f"(MULT, #4, {lenIndexArray}, {temp1} )")
            self.pb.append(f"(ADD, #{tmpAddress}, {temp1}, {temp1} )")
            self.stack.append(f"@{temp1}")


    def jpfsave(self):
        index1 = self.stack.pop()
        self.pb[index1] = f"(JPF, {self.stack.pop()}, {len(self.pb)+1})"
        self.save()

    def save(self):
        self.stack.append(len(self.pb))
        self.pb.append(" ")

    def jp(self):
        index2 = self.stack.pop()
        self.pb[index2] = f"(JP, {len(self.pb)},  ,   )"

    def assign(self):
        var1 = self.stack.pop()
        var2 = self.stack.pop()
        self.pb.append(f"(ASSIGN, {var1}, {var2},   )")
        self.stack.append(var1)

    def until(self):
        top = len(self.stack) - 1

        self.pb.append(f"(JPF, {self.stack[top]}, {self.stack[top - 1]},   )")
        if self.breakaddresses:
            self.pb[self.breakaddresses[-1]] = f"(JP, {len(self.pb)},  ,   )"
            self.breakaddresses.clear()
        self.stack.pop()
        self.stack.pop()

    def operation_(self):
        op1 = self.stack.pop()
        ope = self.stack.pop()
        op2 = self.stack.pop()
        temp = self.gettemp()
        self.pb.append(f"({ope}, {op2}, {op1}, {temp} )")
        self.stack.append(temp)

    def jpf(self):
        index1 = self.stack.pop()
        self.pb[index1] = f"(JPF, {self.stack.pop()}, {len(self.pb)})"

    def output(self):
        x = self.stack[-1]
        self.pb.append(f"(PRINT, {x},  ,   )")

    def label(self):
        self.stack.append(len(self.pb))

    def before_dec_func(self): #todo
        # if self.numberfunction==0:
        #     self.pb.append(f"(ASSIGN, #0, 2400, )")
        #     self.start = len(self.pb)
        #     self.pb.append("start")
        x = len(self.pb)
        y = self.stack.pop()
        if int(y)!= int(self.addresses["main"][0]):
            self.isfunction = True
        indirectadd = self.funcIndirectAdd()
        function = Function(y, self.numberfunction, indirectadd)
        if self.isvoid:
            function.isvoid = True

        function.pbstart = x
        self.function_arr.append(function)
        self.numberfunction += 1


    def after_dec_func(self): #todo
        self.isfunction = False
        if self.function_arr[-1].id!=self.addresses["main"][0]:
            self.pb.append(f"(JP, @{self.function_arr[-1].indirectAdd},  ,   )")
        self.function_arr[-1].whereToReturn = len(self.pb)
        for j in self.function_arr[-1].returnAdds:
            self.pb[j-1] = f"(JP, {len(self.pb)-1},  ,   )"
        self.isvoid = False

    def argument(self): #todo
        temp = []
        for k in range(len(self.pb) - self.function_arr[-1].pbstart):
            x = self.stack.pop()
            if x not in self.function_arr[-1].arrayadds:
                temp.append([x,False])
            else:
                temp.append([x,True])
        for i in range(len(temp)):
            l = temp.pop()
            self.function_arr[-1].inArgs.append(l)

    def findfunction(self):
        func_add = self.stack.pop()
        if func_add == self.addresses["output"][0]:
            self.isInOutput = True
            return
        for i in range(len(self.function_arr)):
            if self.function_arr[i].id == func_add:
                self.funCall = i

    def pfunction(self): #todo
        if self.isInOutput:
            self.isInOutput = False
            return
        self.pb.append(f"(ASSIGN, #{len(self.pb)+2}, {self.function_arr[self.funCall].indirectAdd},   )")
        self.pb.append(f"(JP, {self.function_arr[self.funCall].pbstart+len(self.function_arr[self.funCall].inArgs)},  ,   )")
        self.stack.append(self.tmp)
        x = self.stack.pop()
        tmp = self.gettemp()
        self.pb.append(f"(ASSIGN, {x}, {tmp},   )")
        self.stack.append(tmp)

    def parguments(self): #todo
        if self.isInOutput:
            self.output()
        else:
            len1 = len(self.function_arr[self.funCall].inArgs)
            for i in range(len1):
                x = self.stack.pop()
                if not self.function_arr[self.funCall].inArgs[len1-i-1][1]:
                    self.pb.append(f"(ASSIGN, {x}, {self.function_arr[self.funCall].inArgs[len1-i-1][0]},   )")
                elif x in self.arrayAddresses:
                    print("!!!!!!!!!!")
                    print(self.pb)
                    print(self.arrayAddresses[x][0], "BASSE DIGE")
                    self.pb.append(f"(ASSIGN, #{self.arrayAddresses[x][0]}, {self.function_arr[self.funCall].inArgs[len1-i-1][0]},   )")
                else:
                    self.atsign = True
                    temp=self.gettemp()
                    self.pb.append(f"(ASSIGN, @{x}, {temp} ,   )")
                    self.pb.append(f"(ASSIGN, #{temp}, {self.function_arr[self.funCall].inArgs[len1-i-1][0]},   )")
    def returns(self):
        if not self.isvoid:
            self.pb.append(f"(ASSIGN, {self.stack.pop()}, {self.tmp},   )")
        self.pb.append("a")
        self.function_arr[-1].returnAdds.append(len(self.pb))

class Function:
    def __init__(self, id=None,numFunc=0,indirectAdd=0):
        self.numFunc = numFunc
        self.id = id
        self.funcPb = []
        self.inArgs = []
        self.variablesAndAdds = {}
        # self.breakAdds = []
        self.returnAdds = []
        self.arrayadds = []
        self.whereToReturn = 0
        self.pbstart = 0
        self.isvoid = False
        self.indirectAdd = indirectAdd
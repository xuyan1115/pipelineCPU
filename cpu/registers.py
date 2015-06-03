class Registers(object):

    def __init__(self, numRegisters=32, bits=32):
        self.numRegisters = numRegisters
        self.register = [0 for i in range(numRegisters)]
        self.bits = bits
        
    def initialize(self):
        self.register = [0 for i in range(self.numRegisters)]

    def setRegisters(self, array):
        assert len(array) == self.numRegisters
        self.register = array

    def __getitem__(self, regNum):
        return self.readRegister(regNum)

    def __setitem__(self, regNum, regValue):
        self.writeRegister(regNum, regValue)

    def readRegister(self, regNum):
        return self.register[regNum]

    def writeRegister(self, regNum, regValue):
        #assert regValue >= 0 and regValue < (1 << self.bits)
        self.register[regNum] = regValue

    def returnSize(self):
        return self.numRegisters

    def printRegisters(self):
        for i in range(self.numRegisters):
            print(bin(self.register[i]))

    def getRegisterState(self):
        return self.register

class PipelineReg(object):

    def __init__(self):
        self.initialize()
        
    def initialize(self):
        self.inst = ''
        self.PCPlus1 = 0
        self.instruction = 0xFC000000
        self.opcode = 0
        self.storeD = 0
        self.readData1 = 0
        self.readData2 = 0
        self.immediateValue = 0
        
        ##signals from control unit
        self.regD = 0
        self.signalAluOp = 0
        self.signalADEPEN = 0
        self.signalBDEPEN = 0
        self.signalQDEPEN = 0
        self.signalWz = 0
        self.signalWreg = 0
        self.signalWmem = 0
        self.signalSld = 0
        self.signalShift = 0
        self.signalSext = 0
        self.signalSst = 0
        self.signalisBtaken = 0
        self.signalBtaken = 0
        self.signalisStore = 0

        self.aluResult = 0
        self.zeroResult = 0
        self.memReadData = 0
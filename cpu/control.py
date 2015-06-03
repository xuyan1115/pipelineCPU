class Control(object):
    
    def __init__(self):
        self.WREG = 0
        self.SST = 0
        self.SLD = 0
        self.SHIFT = 0
        self.SEXT = 0
        self.WMEM = 0
        self.ALUOP = 0b0000
        self.WZ = 0
        self.BTAKEN = 0 
        self.isBRANCH = 0

    def signalIn(self, opCode, zeroResult):
        if opCode == 0b000000: #and
            self.WREG = 1
            self.SST = 0
            self.SLD = 0
            self.SHIFT = 0
            self.SEXT = 0
            self.WMEM = 0
            self.ALUOP = 0b0001
            self.WZ = 1
            self.BTAKEN = 0
            self.isSTORE = 0
        elif opCode == 0b000001: #andi
            self.WREG = 1
            self.SST = 0
            self.SLD = 0
            self.SHIFT = 0
            self.SEXT = 0
            self.WMEM = 0
            self.ALUOP = 0b0001
            self.WZ = 1
            self.BTAKEN = 0
            self.isSTORE = 0
        elif opCode == 0b000010: #or
            self.WREG = 1
            self.SST = 0
            self.SLD = 0
            self.SHIFT = 0
            self.SEXT = 0
            self.WMEM = 0
            self.ALUOP = 0b0010
            self.WZ = 1
            self.BTAKEN = 0
            self.isSTORE = 0
        elif opCode == 0b000011: #ori
            self.WREG = 1
            self.SST = 0
            self.SLD = 0
            self.SHIFT = 0
            self.SEXT = 0
            self.WMEM = 0
            self.ALUOP = 0b0010
            self.WZ = 1
            self.BTAKEN = 0
            self.isSTORE = 0
        elif opCode == 0b000100: #add
            self.WREG = 1
            self.SST = 0
            self.SLD = 0
            self.SHIFT = 0
            self.SEXT = 0
            self.WMEM = 0
            self.ALUOP = 0b0011
            self.WZ = 1
            self.BTAKEN = 0
            self.isBTAKEN = 0
            self.isSTORE = 0
        elif opCode == 0b000101: #addi
            self.WREG = 1
            self.SST = 0
            self.SLD = 0
            self.SHIFT = 0
            self.SEXT = 1
            self.WMEM = 0
            self.ALUOP = 0b0011
            self.WZ = 1
            self.BTAKEN = 0
            self.isSTORE = 0
        elif opCode == 0b000110: #sub
            self.WREG = 1
            self.SST = 0
            self.SLD = 0
            self.SHIFT = 0
            self.SEXT = 1
            self.WMEM = 0
            self.ALUOP = 0b0100
            self.WZ = 1
            self.BTAKEN = 0
            self.isSTORE = 0
        elif opCode == 0b000111: #subi
            self.WREG = 1
            self.SST = 0
            self.SLD = 0
            self.SHIFT = 0
            self.SEXT = 1
            self.WMEM = 0
            self.ALUOP = 0b0100
            self.WZ = 1
            self.BTAKEN = 0
            self.isSTORE = 0
        elif opCode == 0b001000: #load
            self.WREG = 1
            self.SST = 0
            self.SLD = 1
            self.SHIFT = 0
            self.SEXT = 1
            self.WMEM = 0
            self.ALUOP = 0b0011 #add
            self.WZ = 0
            self.BTAKEN = 0
            self.isSTORE = 0
        elif opCode == 0b001001: #store
            self.WREG = 0
            self.SST = 1
            self.SLD = 0
            self.SHIFT = 0
            self.SEXT = 1
            self.WMEM = 1
            self.ALUOP = 0b0011
            self.WZ = 0
            self.BTAKEN = 0
            self.isSTORE = 1
        elif opCode == 0b001010: #bne
            self.WREG = 0
            self.SST = 0
            self.SLD = 0
            self.SHIFT = 0
            self.SEXT = 1
            self.WMEM = 0
            self.ALUOP = 0b0000
            self.WZ = 0
            if not zeroResult:
                self.BTAKEN = 1
            else:
                self.BTAKEN = 0
            self.isSTORE = 0

        elif opCode == 0b001011: #beq
            self.WREG = 0
            self.SST = 0
            self.SLD = 0
            self.SHIFT = 0
            self.SEXT = 1
            self.WMEM = 0
            self.ALUOP = 0b0000
            self.WZ = 0
            if zeroResult:
                self.BTAKEN = 1
            else:
                self.BTAKEN = 0
            self.isSTORE = 0

        elif opCode == 0b001100: #branch
            self.WREG = 0
            self.SST = 0
            self.SLD = 0
            self.SHIFT = 0
            self.SEXT = 1
            self.WMEM = 0
            self.ALUOP = 0b0000
            self.WZ = 0
            self.BTAKEN = 1
            self.isSTORE = 0
        elif opCode == 0b001101: #sll
            self.WREG = 1
            self.SST = 0
            self.SLD = 0
            self.SHIFT = 1
            self.SEXT = 0
            self.WMEM = 0
            self.ALUOP = 0b0101
            self.WZ = 1
            self.BTAKEN = 0
            self.isSTORE = 0
        elif opCode == 0b001110: #srl
            self.WREG = 1
            self.SST = 0
            self.SLD = 0
            self.SHIFT = 1
            self.SEXT = 0
            self.WMEM = 0
            self.ALUOP = 0b0110
            self.WZ = 1
            self.BTAKEN = 0
            self.isSTORE = 0
        elif opCode == 0b001111: #sra
            self.WREG = 1
            self.SST = 0
            self.SLD = 0
            self.SHIFT = 1
            self.SEXT = 0
            self.WMEM = 0
            self.ALUOP = 0b0111
            self.WZ = 1
            self.BTAKEN = 0
            self.isSTORE = 0
        else:
            self.WREG = 0
            self.SST = 0
            self.SLD = 0
            self.SHIFT = 0
            self.SEXT = 0
            self.WMEM = 0
            self.ALUOP = 0b0000
            self.WZ = 0
            self.BTAKEN = 0
            self.isSTORE = 0

    def getBtaken(self):
        return self.BTAKEN
    def getSst(self):
        return self.SST
    def getAluOp(self):
        return self.ALUOP
    def getWz(self):
        return self.WZ
    def getWreg(self):
        return self.WREG
    def getShift(self):
        return self.SHIFT
    def getWmem(self):
        return self.WMEM
    def getSld(self):
        return self.SLD
    def getSext(self):
        return self.SEXT
    def getisSTORE(self):
        return self.isSTORE
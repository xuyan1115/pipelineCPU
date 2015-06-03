# -*- coding: utf-8 -*-
from control import Control
from registers import Registers, PipelineReg
from alu import Alu
from memory import Memory
from translator import opcodes, dec2bin
from function import *
import functools


class Pipelinecpu(object):
    '''This class is the pipelinecpu'''

    def __init__(self):
        self.control = Control()
        self.register = Registers(32)
        self.pcreg = PipelineReg()
        self.if_id = PipelineReg()
        self.id_exe = PipelineReg()
        self.exe_mem = PipelineReg()
        self.mem_wb = PipelineReg()
        self.alu = Alu()
        self.memory = Memory()
        self.initializePipeline()

    def getRegisterState(self):
        return self.register.getRegisterState()

    def getInstructionCount(self):
        return self.instructionCount

    def getDataCount(self):
        return self.dataCount

    def getInstruction(self, i):
        return self.memory.readMemory(i)

    def readMemory(self, i):
        return self.memory.readMemory(i)

    def getPC(self):
        return self.pc

    def initializePipeline(self):
        ## Deletes memory and instruction count
        self.signalWPC = 1
        self.signalWIR = 1
        self.regData = 0
        self.pc = 0
        self.signalBtaken = 0
        self.signalSld = 0
        self.signalWreg = 0
        self.signalLOADDEPEN = 1
        self.inst = ''
        self.signalShift = 0
        self.tempinst = ''
        ## Initializes Registers
        self.memory.initialize()
        self.register.initialize()
        self.pcreg.initialize()
        self.if_id.initialize()
        self.id_exe.initialize()
        self.exe_mem.initialize()
        self.mem_wb.initialize()

    ## Forwarding Unit
    def __forwardingUnit(self):
        int2 = functools.partial(int, base=2)
        self.rs1IsReg = (self.opcode != int2(opcodes['bne'])) & (self.opcode != int2(opcodes['beq'])) & (
            			 self.opcode != int2(opcodes['branch']))
        self.rs2IsReg = (self.opcode == int2(opcodes['and'])) | (self.opcode == int2(opcodes['or'])) | (
           				 self.opcode == int2(opcodes['add'])) | \
                        (self.opcode == int2(opcodes['sub'])) | (self.opcode == int2(opcodes['sra'])) | (
                         self.opcode == int2(opcodes['sll'])) | \
                        (self.opcode == int2(opcodes['srl']))

        # ALU A select signal
        ADEPEN1 = ((self.exe_mem.signalWreg == 1) & (self.readReg1 == self.exe_mem.regD) | (self.mem_wb.signalWreg == 1) & \
                      (self.readReg1 == self.mem_wb.regD)) & (self.rs1IsReg)
        ADEPEN2 = ((self.mem_wb.signalWreg == 1) & (self.readReg1 == self.mem_wb.regD)) & (self.rs1IsReg)
        self.signalADEPEN = ADEPEN1 * 2 + ADEPEN2

        #ALU B select signal
        BDEPEN1 = ((self.exe_mem.signalWreg == 1) & (self.readReg2 == self.exe_mem.regD) | (self.mem_wb.signalWreg == 1) & \
                      (self.readReg2 == self.mem_wb.regD)) & (self.rs2IsReg)
        BDEPEN2 = (self.mem_wb.signalWreg == 1) & (self.readReg2 == self.mem_wb.regD) & (self.rs2IsReg) | (
            not self.rs2IsReg)
        self.signalBDEPEN = BDEPEN1 * 2 + BDEPEN2

        #LOADDEPEN
        EXE_A_DEPEN = (self.readReg1 == self.exe_mem.regD) & (self.exe_mem.signalSld == 1) & (self.rs1IsReg)
        EXE_B_DEPEN = (self.readReg2 == self.exe_mem.regD) & (self.exe_mem.signalSld == 1) & (self.rs2IsReg) | \
        			  (self.readReg2 == self.exe_mem.regD) & (self.exe_mem.signalSld == 1) & (self.opcode == int2(opcodes['store']))
        self.signalLOADDEPEN = not (EXE_A_DEPEN | EXE_B_DEPEN)

        #STORE
        self.signalQDEPEN = (self.readReg2 == self.exe_mem.regD) & (self.exe_mem.signalWreg == 1)

    ## Instruction Fetch Stage
    def __cpuStageIF(self, bin_instruction, instruction):
        self.signalBtaken = self.control.getBtaken()
        if self.signalBtaken:
            self.nextPC = twos_to_int(self.if_id.instruction & 0x3FFFFFF, 26)
        else:
            self.nextPC = self.pc + 1

        int2 = functools.partial(int, base=2)
        if self.opcode == 10 or self.opcode == 11:
            self.signalWPC = not(((self.opcode == int2(opcodes['bne'])) | (self.opcode == int2(opcodes['beq']))) & \
                                    self.exe_mem.signalWreg & (not self.exe_mem.signalSld))
            self.signalWPC = int(self.signalWPC)
            self.signalWIR = self.signalWPC
        else:
            if self.signalLOADDEPEN | (self.opcode == 9): #not loaddepen or after load is store
                self.signalWPC = 1
                self.signalWIR = 1
            else:
                self.signalWIR = 0
                self.signalWPC = 0

        '''
        elif self.opcode == 9:
            self.signalWPC = not(self.exe_mem.signalWreg & (self.exe_mem.signalSld |self.exe_mem.regD == self.readReg2))
            self.signalWPC = int(self.signalWPC)
            self.signalWIR = self.signalWPC
        '''

        if self.signalWPC:
            self.pc = self.nextPC
        else:
            self.pc = self.pc

        if self.signalWIR:
            self.if_id.instruction = bin_instruction
            self.if_id.inst = instruction
        else:
            self.if_id.instruction = self.if_id.instruction
            self.if_id.inst = self.if_id.inst

        return self.pc

    ## Instruction Decode Stage
    def __cpuStageID(self):
        #self.id_exe = self.if_id  # Pipeline shift
        
        ## instruction Decode
        self.opcode = (self.if_id.instruction & 0xFC000000) >> 26  # inst[31:26]

        # Sets control based on opcode and zeroResult
        self.control.signalIn(self.opcode, self.exe_mem.zeroResult)

        self.readReg1 = (self.if_id.instruction & 0x001F0000) >> 16  # inst[20:16]

        if self.control.getSst():  # store
            self.readReg2 = (self.if_id.instruction & 0x03E00000) >> 21  #inst[25:21]
        else:
            self.readReg2 = (self.if_id.instruction & 0x0000001F)  # inst[4:0]

        # Forwarding Detect
        self.__forwardingUnit()

        self.id_exe.regD = ((self.if_id.instruction & 0x03E00000) >> 21) # rd

        # Sets ID_EXE registers based on register data
        self.signalShift = self.control.getShift()
        if self.signalShift:
            self.id_exe.readData1 = self.readReg1  # sa for shift instructions
        else:
            self.id_exe.readData1 = self.register.readRegister(self.readReg1)
        self.id_exe.readData2 = self.register.readRegister(self.readReg2)

        # Stores the necessary control bits in ID_EXE registers
        self.id_exe.signalisStore = self.control.getisSTORE()
        self.id_exe.signalBtaken = self.control.getBtaken()
        self.id_exe.signalQDEPEN = int(self.signalQDEPEN)
        self.id_exe.signalADEPEN = self.signalADEPEN
        #print 'ADEPEN', self.id_exe.signalADEPEN
        self.id_exe.signalBDEPEN = self.signalBDEPEN
        #print 'BDEPEN', self.id_exe.signalBDEPEN
        self.id_exe.signalAluOp = self.control.getAluOp()
        #print 'ALUOP', self.id_exe.signalAluOp
        self.id_exe.signalWz = self.control.getWz() & (self.signalLOADDEPEN | (self.opcode == 9)) & (not self.exe_mem.signalBtaken)
        self.id_exe.signalWreg = self.control.getWreg() & (self.signalLOADDEPEN | (self.opcode == 9)) & (not self.exe_mem.signalBtaken)
        self.id_exe.signalWmem = self.control.getWmem() & (self.signalLOADDEPEN | (self.opcode == 9)) & (not self.exe_mem.signalBtaken)
        self.id_exe.signalSld = self.control.getSld()
        self.id_exe.inst = self.if_id.inst

        # Sets ID_EXE registers immediateValue based on control signal sext
        if self.control.getSext():
            self.id_exe.immediateValue = twos_to_int(self.if_id.instruction & 0xFFFF, 16)
        else:
            self.id_exe.immediateValue = self.if_id.instruction & 0xFFFF
        self.istransfer = (self.opcode == 10 or self.opcode == 11 or self.opcode == 12)
        self.iswrite = (self.id_exe.signalWreg or self.id_exe.signalWmem)
        if (not self.istransfer) & self.iswrite:
            self.tempinst = self.id_exe.inst
        elif self.istransfer & (self.exe_mem.inst == 'stall'):
            self.tempinst = self.id_exe.inst
        elif self.id_exe.inst == '':
            self.tempinst = self.id_exe.inst
        elif self.istransfer & (self.opcode == 12):
            self.tempinst = self.id_exe.inst
        else:
            self.tempinst = 'stall'

    ## Instruction Execution Stage
    def __cpuStageEXE(self):
        self.exe_mem.inst = self.tempinst
        self.exe_mem.signalisStore = self.id_exe.signalisStore
        self.exe_mem.signalBtaken = self.id_exe.signalBtaken
        self.exe_mem.signalADEPEN = self.id_exe.signalADEPEN
        self.exe_mem.signalBDEPEN = self.id_exe.signalBDEPEN
        self.exe_mem.signalAluOp = self.id_exe.signalAluOp
        self.exe_mem.readData2 = self.id_exe.readData2
        self.exe_mem.regD = self.id_exe.regD
        self.exe_mem.signalWmem = self.id_exe.signalWmem
        self.exe_mem.signalWreg = self.id_exe.signalWreg
        self.exe_mem.signalSld = self.id_exe.signalSld
        self.exe_mem.signalWz = self.id_exe.signalWz
        # forwarding
        if self.id_exe.signalADEPEN == 0:
            self.aluA = self.id_exe.readData1
        elif self.id_exe.signalADEPEN == 2:
            self.aluA = self.exe_mem.aluResult
        elif self.id_exe.signalADEPEN == 3:
            self.aluA = self.regData
        else:
            print 'Error!'

        if self.id_exe.signalBDEPEN == 0:
            self.aluB = self.id_exe.readData2
        elif self.id_exe.signalBDEPEN == 1:
            self.aluB = self.id_exe.immediateValue
        elif self.id_exe.signalBDEPEN == 2:
            self.aluB = self.mem_wb.aluResult
        elif self.id_exe.signalBDEPEN == 3:
            self.aluB = self.regData
        else:
            print 'Error!'
        '''
        if self.exe_mem.signalQDEPEN == 0:
            self.storeD = self.id_exe.readData2
        elif self.exe_mem.signalQDEPEN == 1:
            self.storeD = self.regData
        else:
            print 'Error!'
        '''
        self.exe_mem.signalQDEPEN = int(self.id_exe.signalQDEPEN)
        #self.exe_mem.storeD = self.storeD
        self.alu.compute(self.id_exe.signalAluOp, self.aluA, self.aluB)
        ## Sets EXE_MEM registers
        self.exe_mem.aluResult = self.alu.getResults()
        if self.id_exe.signalWz:
            self.exe_mem.zeroResult = self.alu.getZero()

    ## Memory Stage
    def __cpuStageMEM(self):
        self.mem_wb.inst = self.exe_mem.inst
        self.mem_wb.regD = self.exe_mem.regD
        self.mem_wb.readData2 = self.exe_mem.readData2
        self.mem_wb.aluResult = self.exe_mem.aluResult
        self.mem_wb.signalSld = self.exe_mem.signalSld
        self.mem_wb.signalWreg = self.exe_mem.signalWreg
        self.mem_wb.signalWmem = self.exe_mem.signalWmem

        if self.exe_mem.signalQDEPEN == 0:
            self.storeD = self.exe_mem.readData2
        elif self.exe_mem.signalQDEPEN == 1:
            self.storeD = self.regData
        else:
            print 'Error!'

        self.mem_wb.signalQDEPEN = self.exe_mem.signalQDEPEN
        ## Read from Memory
        self.mem_wb.memReadData = self.memory.readMemory(self.exe_mem.aluResult)

        ## Write to Memory
        if self.exe_mem.signalWmem:
            self.memory.writeMemory(int_to_twos(self.exe_mem.aluResult), self.storeD)

    ## Write Back Stage
    def __cpuStageWB(self):
        self.inst = self.mem_wb.inst
        self.signalWreg = self.mem_wb.signalWreg
        self.signalSld = self.mem_wb.signalSld
        if self.signalSld:
            self.regData = self.mem_wb.memReadData
        else:
            self.regData = self.mem_wb.aluResult

        if self.signalWreg:
            self.register.writeRegister(self.mem_wb.regD, self.regData)

    def atomicStep(self, bin_instruction, instruction):
        self.__cpuStageWB()
        self.__cpuStageMEM()
        self.__cpuStageEXE()
        self.__cpuStageID()
        return self.__cpuStageIF(bin_instruction, instruction)

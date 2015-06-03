# -*- coding: utf-8 -*-

__author__ = 'Xu Yan'

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from gui.pipelineGUI import Ui_Pipeline_CPU
from cpu.translator import *
from cpu.pipelinecpu import Pipelinecpu

try:
    _fromUtf8 = QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)

class Pipeline(QDialog, Ui_Pipeline_CPU):
    def __init__(self, parent=None):
        super(Pipeline, self).__init__(parent)
        self.setupUi(self)
        self.inst = []
        self.count = 0
        self.instnum = 0
        self.pipeline = Pipelinecpu()
        self.clk = 0
        self.connect(self.StartButton, SIGNAL('clicked()'),
					 self.onStartClicked)
        self.connect(self.NextstepButton, SIGNAL('clicked()'),
					 self.onNextstepClicked)
        self.connect(self.ResetButton, SIGNAL('clicked()'),
					 self.onResetClicked)

    def getTextEdit(self):
        content = self.instructionInput.toPlainText().split('\n')
        m = len(content)
        for i in range(m):
            if content[i] != '':
                self.inst.append(content[i])  #delete "" rows
        self.instnum = len(self.inst)

    def onResetClicked(self):
        self.count = 0
        self.clk = 0
        self.clock.display(self.clk)
        self.StartButton.setEnabled(True)
        self.NextstepButton.setEnabled(False)
        self.pipeline = Pipelinecpu()
        self.IF_instruction.setText('')
        self.inst = []
        self.signalpc.setText(str(self.pipeline.getPC()))
        self.display()
		

    def onStartClicked(self):
        self.initialize(self)
        self.getTextEdit()
        self.StartButton.setEnabled(False)
        self.NextstepButton.setEnabled(True)
        if self.instnum == 0:
            self.IF_instruction.setText('')
            self.bin_inst = 0xFC000000
        else:
            self.bin_inst = translator(str(self.inst[self.count]))
            self.count = self.pipeline.atomicStep(self.bin_inst, self.inst[self.count])
            self.IF_instruction.setText(self.pipeline.if_id.inst)
        self.clk += 1
        #self.count += 1
        self.clock.display(self.clk)
        self.signalpc.setText(str(self.pipeline.getPC()))
        self.display()

    def onNextstepClicked(self):
        #self.count += 1
        if self.count >= self.instnum:
            self.IF_instruction.setText('')
            self.bin_inst = 0xFC000000
            self.pipeline.atomicStep(self.bin_inst, '')
        else:
            self.IF_instruction.setText(self.inst[self.count])
            self.bin_inst = translator(str(self.inst[self.count]))
            self.count = self.pipeline.atomicStep(self.bin_inst, self.inst[self.count])
        self.clk += 1
        self.clock.display(self.clk)
        self.signalpc.setText(str(self.pipeline.getPC() - 1))
        self.display()

    def display(self):
        #IF_stage
        self.signalbtaken.setText(str(self.pipeline.signalBtaken))
        self.signalwpc.setText(str(self.pipeline.signalWPC))
        self.signalwir.setText(str(self.pipeline.signalWIR))
        self.signalir.setText(self.pipeline.if_id.inst)
        #ID_stage
        self.ID_instruction.setText(str(self.pipeline.id_exe.inst))
        self.signalid_d.setText(str(self.pipeline.id_exe.regD))
        self.signalA.setText(str(self.pipeline.id_exe.readData1))
        self.signalB.setText(str(self.pipeline.id_exe.readData2))
        self.signalI.setText(str(self.pipeline.id_exe.immediateValue))
        self.signalSST.setText(str(self.pipeline.control.getSst()))
        self.signalSEXT.setText(str(self.pipeline.control.getSext()))
        self.signalLOADDEPEN.setText(str(int(self.pipeline.signalLOADDEPEN)))
        self.signalADEPEN_id.setText(str(self.pipeline.id_exe.signalADEPEN))
        self.signalBDEPEN_id.setText(str(self.pipeline.id_exe.signalBDEPEN))
        self.signalQDEPEN_id.setText(str(self.pipeline.id_exe.signalQDEPEN))
        self.signalALUOP_id.setText(str(self.pipeline.id_exe.signalAluOp))
        self.signalWZ_id.setText(str(self.pipeline.id_exe.signalWz))
        self.signalwmem_id.setText(str(self.pipeline.id_exe.signalWmem))
        self.signalsld_id.setText(str(self.pipeline.id_exe.signalSld))
        self.signalwreg_id.setText(str(self.pipeline.id_exe.signalWreg))
        self.signalshift.setText(str(self.pipeline.signalShift))
        #EXE_stage
        self.EXE_instruction.setText(str(self.pipeline.exe_mem.inst))
        self.signalexe_d.setText(str(self.pipeline.exe_mem.regD))
        self.signalz.setText(str(self.pipeline.exe_mem.zeroResult))
        self.signalR.setText(str(self.pipeline.exe_mem.aluResult))
        self.signalS.setText(str(self.pipeline.exe_mem.storeD))
        self.signalADEPEN.setText(str(self.pipeline.exe_mem.signalADEPEN))
        self.signalBDEPEN.setText(str(self.pipeline.exe_mem.signalBDEPEN))
        self.signalQDEPEN_exe.setText(str(self.pipeline.exe_mem.signalQDEPEN))
        self.signalALUOP.setText(str(self.pipeline.exe_mem.signalAluOp))
        self.signalWZ.setText(str(self.pipeline.exe_mem.signalWz))
        self.signalwmem_exe.setText(str(self.pipeline.exe_mem.signalWmem))
        self.signalsld_exe.setText(str(self.pipeline.exe_mem.signalSld))
        self.signalwreg_exe.setText(str(self.pipeline.exe_mem.signalWreg))
        #MEM_stage
        self.MEM_instruction.setText(str(self.pipeline.mem_wb.inst))
        self.signalmem_d.setText(str(self.pipeline.mem_wb.regD))
        self.signalQDEPEN.setText(str(self.pipeline.mem_wb.signalQDEPEN))
        self.signalD.setText(str(self.pipeline.mem_wb.memReadData))
        self.signalC.setText(str(self.pipeline.mem_wb.aluResult))
        self.signalwmem.setText(str(self.pipeline.mem_wb.signalWmem))
        self.signalsld_mem.setText(str(self.pipeline.mem_wb.signalSld))
        self.signalwreg_mem.setText(str(self.pipeline.mem_wb.signalWreg))

        if self.pipeline.mem_wb.signalWmem:
            self.address.setText(str(self.pipeline.mem_wb.aluResult))
            self.addr_value.setText(str(self.pipeline.storeD))
        else:
            self.address.setText('')
            self.addr_value.setText('')
        #WB_stage
        self.WB_instruction.setText(str(self.pipeline.inst))
        self.signalSLD.setText(str(self.pipeline.signalSld))
        self.signalWREG.setText(str(self.pipeline.signalWreg))
        #registers
        self.register0.setText(str(self.pipeline.register.readRegister(0)))
        self.register1.setText(str(self.pipeline.register.readRegister(1)))
        self.register2.setText(str(self.pipeline.register.readRegister(2)))
        self.register3.setText(str(self.pipeline.register.readRegister(3)))
        self.register4.setText(str(self.pipeline.register.readRegister(4)))
        self.register5.setText(str(self.pipeline.register.readRegister(5)))
        self.register6.setText(str(self.pipeline.register.readRegister(6)))
        self.register7.setText(str(self.pipeline.register.readRegister(7)))
        self.register8.setText(str(self.pipeline.register.readRegister(8)))
        self.register9.setText(str(self.pipeline.register.readRegister(9)))
        self.register10.setText(str(self.pipeline.register.readRegister(10)))
        self.register11.setText(str(self.pipeline.register.readRegister(11)))
        self.register12.setText(str(self.pipeline.register.readRegister(12)))
        self.register13.setText(str(self.pipeline.register.readRegister(13)))
        self.register14.setText(str(self.pipeline.register.readRegister(14)))
        self.register15.setText(str(self.pipeline.register.readRegister(15)))
        self.register16.setText(str(self.pipeline.register.readRegister(16)))
        self.register17.setText(str(self.pipeline.register.readRegister(17)))
        self.register18.setText(str(self.pipeline.register.readRegister(18)))
        self.register19.setText(str(self.pipeline.register.readRegister(19)))
        self.register20.setText(str(self.pipeline.register.readRegister(20)))
        self.register21.setText(str(self.pipeline.register.readRegister(21)))
        self.register22.setText(str(self.pipeline.register.readRegister(22)))
        self.register23.setText(str(self.pipeline.register.readRegister(23)))
        self.register24.setText(str(self.pipeline.register.readRegister(24)))
        self.register25.setText(str(self.pipeline.register.readRegister(25)))
        self.register26.setText(str(self.pipeline.register.readRegister(26)))
        self.register27.setText(str(self.pipeline.register.readRegister(27)))
        self.register28.setText(str(self.pipeline.register.readRegister(28)))
        self.register29.setText(str(self.pipeline.register.readRegister(29)))
        self.register30.setText(str(self.pipeline.register.readRegister(30)))
        self.register31.setText(str(self.pipeline.register.readRegister(31)))

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    form = Pipeline()
    form.show()
    app.exec_()
'''
subi r1, r2, 1 
addi r3, r6, 0
bne 5
srl r2, 2, r6
addi r4, r1, 5
or r3, r1, r7

load r1 , 100(r3) 
sub r4, r1, r5
store r4, 55(r3)
or r6, r7, r1
'''
# -*- coding: utf-8 -*-	
from translator import *
from pipelinecpu import Pipelinecpu

#print translator('bne 19')
#print translator('load r10, 40(r4)')
inst = 'addi r5, r3, -7'
bin_inst = translator('addi r5, r3, -7')
print type(bin_inst) 

if __name__ == '__main__':
	pipeline = Pipelinecpu()
	pipeline.atomicStep(bin_inst, inst)
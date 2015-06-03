# -*- coding: utf-8 -*-
class Memory(object):
    def __init__(self):
        self.initialize()
        
    # convience functions
    def __getitem__(self, pc):
        return self.readMemory(pc)
    
    def __setitem__(self, pc, data):
        return self.writeMemory(pc, data)

    def writeMemory(self, pc, data):
        if isinstance(data, int):
            #verbose_print("Writing 0x%08x to 0x%08x"%(data, pc))
            if (pc >= 0x00000000 and pc <= 0xffffffff):
            	self.memory[pc] = data
                print 'PC:', pc, 'value:', self.memory[pc]
            else:
            	print 'address is not exist!' 

    def readMemory(self, pc):
        if (pc >= 0x00000000 and pc <= 0xffffffff):
            self.memory.setdefault(pc, 0x00000000)
            return self.memory[pc]
        else:
            print 'address is not exist!' 
            return 0

    def initialize(self):

        self.memory = dict()
        self.memory[100] = -1

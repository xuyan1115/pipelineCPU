# -*- coding: utf-8 -*-
from function import *

class Alu(object):

    def __init__(self):
        pass

    def compute(self, aluOp, A, B):
        if (aluOp == 0b0001): #and
            self.result = A & B
        elif (aluOp == 0b0010): #or
            self.result = A | B
        elif (aluOp == 0b0011): #add
            amount = A + B
            self.result = amount
        elif (aluOp == 0b0100): #sub
            amount = A - B
            self.result = amount
        elif (aluOp == 0b0101): #sll
            self.result = 0xFFFFFFFF & (B << A)
        elif (aluOp == 0b0111): #sra
            self.result = 0xFFFFFFFF & (B >> A)
        elif (aluOp == 0b0110): #srl
            A1 = 0xFFFFFFFF & ( 1 << (32 - A) )
            A2 = 0xFFFFFFFF & ( B >> A )
            self.result = int('0b' + bin(A1 + A2)[3:], 2)
        else:
            self.result = 0

    def getResults(self):
        return self.result

    def getZero(self):
        if(self.result == 0):
            return 1
        else:
            return 0
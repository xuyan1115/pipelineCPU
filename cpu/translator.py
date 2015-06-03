# -*- coding: utf-8 -*-
#self.ID_rs1IsReg = {'and': 0x00, 'andi': 0x01, 'or': 0x02, 'ori': 0x03, 'add': 0x04, \
#             'addi': 0x05, 'sub': 0x06, 'subi': 0x07, 'load': 0x08, 'store': 0x09}
#    self.ID_rs2IsReg =  {'and': 0x00, 'andi': 0x01, 'or': 0x02, 'ori': 0x03}
opcodes = {
			'and': '000000', 'andi': '000001', 'or': '000010', 'ori': '000011',
			'add': '000100', 'addi': '000101', 'sub': '000110', 'subi': '000111',
			'load': '001000', 'store': '001001', 'bne': '001010', 
			'beq': '001011', 'branch': '001100', 'sll': '001101', 
            'srl': '001110', 'sra': '001111'}

def format_instruction( asm_code ):
	asm_code = asm_code.split(None, 1)
	asm_code = [asm_code[0]] + [x.strip() for x in asm_code[1].replace(',', ' ').split()]
	return asm_code

def dec2bin(num, bits=5):  
    if abs(num) != num:  
        num = 2 ** bits + num 
    tmp = ""  
    while True:  
        tmp += str(num % 2)  
        num = num // 2  
        if num == 0:  
            break   
    if len(tmp) != bits:
        tmp += '0' * (bits - len(tmp))
    tmp = list(tmp)  
    tmp.reverse()  
    tmp = "".join(tmp)  
    return tmp  

def translator( asm_code ):
    op = format_instruction( asm_code )
    if len(op) == 2:   
        bincode = opcodes[op[0]] + dec2bin(int(op[1]), 26)
    elif len(op) == 3: 
        temp = op[2].rstrip(')').split('(')
        temp.reverse()
        op = op[0:2] + temp
        bincode = opcodes[op[0]] + dec2bin(int(op[1][1:])) + dec2bin(int(op[2][1:])) + dec2bin(int(op[3]), 16)
    elif len(op) == 4:
        if op[3][0] == 'r':
            op_4 = int(op[3][1:])
        else:
            if (op[3][-1] == 'H') | (op[3][-1] == 'h'):
                op_4 = int(op[3][:-1], 16)
            elif (op[3][-1] == 'O') | (op[3][-1] == 'o'):
                op_4 = int(op[3][:-1], 8)
            elif (op[3][-1] == 'B') | (op[3][-1] == 'b'):
                op_4 = int(op[3][:-1], 2)
            else:
                op_4 = int(op[3])
        if op[2][0] != 'r':   #sra, sll, srl
            op_3 = int(op[2])
        else:
            op_3 = int(op[2][1:])
        bincode = opcodes[op[0]] + dec2bin(int(op[1][1:])) + dec2bin(op_3) + dec2bin(op_4, 16)

    bincode = int(bincode, 2)
    
    return bincode

if __name__ == '__main__':
    print bin(translator('bne 19'))
    print translator('load r10, 40(r4)')
    m = translator('addi r5, r3, -7')
    print m, type(m)
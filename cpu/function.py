# -*- coding: utf-8 -*-
def make_mask(bits=32, bits2=None):
    '''Make a bitmask for the bits between bits and bits2
     if bits2 is omitted, it's assumed to be 0.'''
    if bits2 is None: return (1 << bits) - 1
    bits, bits2 = sorted([bits, bits2])
    return make_mask(bits2) ^ make_mask(bits)

def int_to_twos(x, bits=32):
    '''Assure that x fits in a specified number of bits, taking the
     2's complement if necessary.'''
    return x & make_mask(bits)

def is_negative(x, bits=32):
    '''Returns the negativity of x.'''
    return bool(x & 1 << (bits - 1))

def twos_to_int(x, bits=32):
    '''Returns the int representation of a 2's complement value.'''
    x = int_to_twos(x, bits)
    return -int_to_twos(-x, bits) if is_negative(x, bits) else x

def sign_extend(x, old_sz=16, new_sz=32):
    '''Sign-extend a value from old_sz bits to new_sz bits.
        WARNING: This will truncate if new_sz < old_sz'''
    assert old_sz <= new_sz
    if is_negative(x, old_sz):
        return int_to_twos(x | make_mask(old_sz, new_sz), new_sz)
    else:
        return int_to_twos(x, old_sz)

if __name__ == '__main__':
    print bin(int_to_twos(-1))
    print twos_to_int(0b11111111111111111111111111111111)
    print bin(sign_extend(0xffff))
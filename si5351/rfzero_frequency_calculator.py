# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.

register calculator for Si5351 for frequencies bewteen
"""

import math

def calc_fmd_omd(fout):
    fref = 25000000
    # d=4
    r = 1
    
    # fout = 9000000
    
    # 292968 <= fout <= 150 MHz
    # I'm not sure about the lower limit. Why isn't it 500 kHz
    
    d = 600000000/fout
    if d < 6:
        d = 6
    elif d%2:
        d+=1
        
    if d*fout < 600000000:
        d+=2
        
    # d needs to be rounded up. I think this rounding might be done when 
    # registers are written to in the rfzero code. I'm just using the Adafruit
    # Si5351 package to write to the registers
    d = math.ceil(d)
    
    
    fvco = d * r * fout
    
    # calculate the Feedback Multisynth Divider
    fmd = fvco/fref
    
    # Get the integer part of fmd
    a = int(fmd)
    
    # Find b/c
    b_c = fmd - a
    
    # c is the denominator. Set it to the largest value
    c = 1048575
    b = int(b_c * c)
    
    fmd_param = (a, b, c)
    omd_param = d
    
    return fmd_param, omd_param



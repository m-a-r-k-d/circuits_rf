# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple demo of the SI5351 clock generator.
# This is like the Arduino library example:
#   https://github.com/adafruit/Adafruit_Si5351_Library/blob/master/examples/si5351/si5351.ino
# Which will configure the chip with:
#  - PLL A at 900MHz
#  - PLL B at 616.66667MHz
#  - Clock 0 at 112.5MHz, using PLL A as a source divided by 8
#  - Clock 1 at 13.553115MHz, using PLL B as a source divided by 45.5
#  - Clock 2 at 10.76khz, using PLL B as a source divided by 900 and further
#    divided with an R divider of 64.
import board
import busio

import adafruit_si5351
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

fmd_9MHz, omd_9MHz = calc_fmd_omd(9000000)
fmd_19MHz, omd_19MHz = calc_fmd_omd(19100000)

# Initialize I2C bus.
i2c = busio.I2C(board.GP1, board.GP0)

# Initialize SI5351.
si5351 = adafruit_si5351.SI5351(i2c)
# Alternatively you can specify the I2C address if it has been changed:
# si5351 = adafruit_si5351.SI5351(i2c, address=0x61)

# Now configue the PLLs and clock outputs.
# The PLLs can be configured with a multiplier and division of the on-board
# 25MHz reference crystal.  For example configure PLL A to 900MHz by multiplying
# by 36.  This uses an integer multiplier which is more accurate over time
# but allows less of a range of frequencies compared to a fractional
# multiplier shown next.

# 260215 MJD - Making this a configure_fractional
### si5351.pll_a.configure_integer(36)  # Multiply 25MHz by 36

### For 9 MHz
# si5351.pll_a.configure_fractional(24,503316,1048575)
### For 19 MHz
# si5351.pll_a.configure_fractional(25,83885,1048575)
si5351.pll_a.configure_fractional(fmd_19MHz[0],fmd_19MHz[1],fmd_19MHz[2])

print(f"PLL A frequency: {si5351.pll_a.frequency / 1000000}MHz")

# And next configure PLL B to 616.6667MHz by multiplying 25MHz by 24.667 using
# the fractional multiplier configuration.  Notice you specify the integer
# multiplier and then a numerator and denominator as separate values, i.e.
# numerator 2 and denominator 3 means 2/3 or 0.667.  This fractional
# configuration is susceptible to some jitter over time but can set a larger
# range of frequencies.

# si5351.pll_b.configure_fractional(24,503316,1048575)  # Multiply 25MHz by 24.667 (24 2/3)
si5351.pll_b.configure_fractional(fmd_9MHz[0],fmd_9MHz[1],fmd_9MHz[2])
print(f"PLL B frequency: {si5351.pll_b.frequency / 1000000}MHz")

# Now configure the clock outputs.  Each is driven by a PLL frequency as input
# and then further divides that down to a specific frequency.
# Configure clock 0 output to be driven by PLL A divided by 8, so an output
# of 112.5MHz (900MHz / 8).  Again this uses the most precise integer division
# but can't set as wide a range of values.
si5351.clock_0.configure_integer(si5351.pll_a, omd_19MHz)
print(f"Clock 0: {si5351.clock_0.frequency / 1000000}MHz")

# Next configure clock 1 to be driven by PLL B divided by 45.5 to get
# 13.5531MHz (616.6667MHz / 45.5).  This uses fractional division and again
# notice the numerator and denominator are explicitly specified.  This is less
# precise but allows a large range of frequencies.
si5351.clock_1.configure_integer(si5351.pll_b, omd_9MHz)  # Divide by 45.5 (45 1/2)
print(f"Clock 1: {si5351.clock_1.frequency / 1000000}MHz")

# Finally configure clock 2 to be driven by PLL B divided once by 900 to get
# down to 685.15 khz and then further divided by a special R divider that
# divides 685.15 khz by 64 to get a final output of 10.706khz.

### si5351.clock_2.configure_integer(si5351.pll_b, 900)

# Set the R divider, this can be a value of:
#  - R_DIV_1: divider of 1
#  - R_DIV_2: divider of 2
#  - R_DIV_4: divider of 4
#  - R_DIV_8: divider of 8
#  - R_DIV_16: divider of 16
#  - R_DIV_32: divider of 32
#  - R_DIV_64: divider of 64
#  - R_DIV_128: divider of 128

##si5351.clock_2.r_divider = adafruit_si5351.R_DIV_64
##print(f"Clock 2: {si5351.clock_2.frequency / 1000}khz")

# After configuring PLLs and clocks, enable the outputs.
si5351.outputs_enabled = True
# You can disable them by setting false.

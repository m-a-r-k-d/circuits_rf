void CalcRegisters(const uint32_t fout, uint8_t *regs)
{
    uint32_t fref = 27000000UL;                  // The reference frequency

    // Calc Output Multisynth Divider and R with e = 0 and f = 1 => msx_p2 = 0 and msx_p3 = 1
    uint32_t d = 4;
    uint32_t msx_p1 = 0;                         // If fout > 150 MHz then MSx_P1 = 0 and MSx_DIVBY4 = 0xC0, see datasheet 4.1.3
    int msx_divby4 = 0;
    int rx_div = 0;
    int r = 1;

    if (fout > 150000000UL)
        msx_divby4 = 0x0C;                       // MSx_DIVBY4[1:0] = 0b11, see datasheet 4.1.3
    else if (fout < 292969UL)                    // If fout < 500 kHz then use R divider, see datasheet 4.2.2. In reality this means > 292 968,75 Hz when d = 2048
    {
        int rd = 0;
        while ((r < 128) && (r * fout < 292969UL))
        {
            r <<= 1;
            rd++;
        }
        rx_div = rd << 4;
		
        d = 600000000UL / (r * fout);            // Use lowest VCO frequency but handle d minimum
        if (d % 2)                               // Make d even to reduce spurious and phase noise/jitter, see datasheet 4.1.2.1.
            d++;

        if (d * r * fout < 600000000UL)          // VCO frequency to low check and maintain an even d value
            d += 2;
    }	
    else                                         // 292968 Hz <= fout <= 150 MHz
    {
        d = 600000000UL / fout;                  // Use lowest VCO frequency but handle d minimum
        if (d < 6)
            d = 6;
        else if (d % 2)                          // Make d even to reduce phase noise/jitter, see datasheet 4.1.2.1.
           d++;
			
        if (d * fout < 600000000UL)              // VCO frequency to low check and maintain an even d value
            d += 2;
    }
    msx_p1 = 128 * d - 512;

    uint32_t fvco = (uint32_t) d * r * fout;

    // Calc Feedback Multisynth Divider
    double fmd = (double)fvco / fref;            // The FMD value has been found
    int a = fmd;                                 // a is the integer part of the FMD value

    double b_c = (double)fmd - a;                // Get b/c
    uint32_t c = 1048575UL;
    uint32_t b = (double)b_c * c;
    if (b > 0)
    {
        c = (double)b / b_c + 0.5;               // Improves frequency precision in some cases
        if (c > 1048575UL)
            c = 1048575UL;
    }

    uint32_t msnx_p1 = 128 * a + 128 * b / c - 512;   // See datasheet 3.2
    uint32_t msnx_p2 = 128 * b - c * (128 * b / c);
    uint32_t msnx_p3 = c;

    // Feedback Multisynth Divider register values
    regs[0] = (msnx_p3 >> 8) & 0xFF;
    regs[1] = msnx_p3 & 0xFF;
    regs[2] = (msnx_p1 >> 16) & 0x03;
    regs[3] = (msnx_p1 >> 8) & 0xFF;
    regs[4] = msnx_p1 & 0xFF;
    regs[5] = ((msnx_p3 >> 12) & 0xF0) + ((msnx_p2 >> 16) & 0x0F);
    regs[6] = (msnx_p2 >> 8) & 0xFF;
    regs[7] = msnx_p2 & 0xFF;

    // Output Multisynth Divider and R register values
    regs[8] = 0;                                  // (msx_p3 >> 8) & 0xFF
    regs[9] = 1;                                  // msx_p3 & 0xFF
    regs[10] = rx_div + msx_divby4 + ((msx_p1 >> 16) & 0x03);
    regs[11] = (msx_p1 >> 8) & 0xFF;
    regs[12] = msx_p1 & 0xFF;
    regs[13] = 0;                                 // ((msx_p3 >> 12) & 0xF0) + (msx_p2 >> 16) & 0x0F
    regs[14] = 0;                                 // (msx_p2 >> 8) & 0xFF
    regs[15] = 0;                                 // msx_p2 & 0xFF

    return;
}
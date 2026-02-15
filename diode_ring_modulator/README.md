# Diode ring modulator
I want to try to get a diode ring modulator working.

ordered:  
26 AWG magnet wire  
1N5817 diodes  
1N5711 diodes
FT37-43 toroids for transformers  

I built the circuit after watching Youtube videos.

![Screenshot of LTSpice circuit](pics/LTSpice_circuit.png)

The screenshot is updated from what I had been using originally. The inductance of the transformers was 1 mH, but I wound a transformer and measured the inductance from 1 - 50 MHZ using my NanoVNA, and the windoings are ~35 uH.  

The simulation looks ok:  

![LTSpice output](pics/Vout_1MHz_input_1kHz_modulation.png)  

If you put a DC offset on the Baseband input, you can make it look like just "regular" AM.  


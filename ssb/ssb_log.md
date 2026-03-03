# Log for SSB transmitter
I'd like to build a QRP single sideband transmitter. I've been watching YouTube videos and reading stuff online.

From the ARRL handbook that I have, here's a block diagram:  
![Picture](pics/ssb_transmitter.jpg)

2-16-26  
I have built a ring diode double sideband suppressed carrier mixer, and I bought a couple from Amazon. They behave pretty similarly. I think the biggest difference is the effects of input voltage. I've made a log of info in the diode_ring_modulator directory.

I have an Si5351a from Amazon for the oscillators. I'm using the Adafruit circuit python example code to set the registers in the chip, and I modified the rfzero code for calculating the Feedback and Output Multisynth Dividers  
https://rfzero.net/tutorials/si5351a/

I bought a crstal QER filter (Quasi equiripple) from diyrf.com off of ebay. I built that yesterday. The pass band seems narrow enough especially if measured betwen 3dB points. Lots of ripple in the pass band though! I will need to make an impedance matching circuit for it. The information that I got with the filter says that the input impedance is approxiomately 250 Ohms. I'm not sure how that is measured, though. When I calibrate the nanovna to 8885 kHz to 9005 kHz and look at the smith chart, the max Ohms measured is 130 Ohms with 177 nH inductance. (The lowest is only about 20 Ohms though - that's how much ripple there is.) 
Calculating the reactance for that gives ~130 Ohms. (It would need to be a lot more inductance to see a significant change from just measured R.)

The impedance matching can be done with   
* just a series resistor (I think, because I want to go from 50 Ohms to 130 Ohms)
* an LC network (L pad, https://electronics.stackexchange.com/questions/705995/why-dont-people-always-use-50-ohm-resistors-when-matching-impedances or https://toroids.info/FT37-43.php). According to the calculator at that toroids site, the L stays pretty constant, and then you can tune with the capacitance. Maybe this is a good use of one of those variable caps?
* an impedance matching transformer (https://www.n1fd.org/2024/05/21/crystal-filter/)

I think that last link talks about obtaining the input impedance of the filter by putting a potentiometer in the circuit and finding what value gives the least pass band ripple in your nanovna. I don't know if I have a 1k pot though  

Maybe I have a 1k pot somewhere....

Looking a little more at the inductance from the wire-wound toroid that I want to use for the impedance matching LC network.  

Using the calculator on that toroids web page, 2.3 turns on the FT37-43 toroid should give 1.89 uH. I used the nanovna to measure an inductor that I wound that way and I get 0.694 uH at 9 MHz
This is what my measurement jig looks like for this. (I kept the original two turns on the toroid.)
![Picture](pics/nanovna_2_terminal_jig.jpg)

| turns | Inductance (uH) | difference (uH) |
| :-----: | :------------:| :-----: |
|  2    |   0.694         | |
|  3    |   1.55          | 0.856 |
|  4    |   2.64          | 1.09  |
|  5    |   4.07          | 1.43  |
|  6    |   5.74          | 1.67  |
|  7    |    7.73         | 1.99  |

The winding on the toroid is pretty sparse. I wonder if as the toroid is more uniformaly wound if the increase in inductance per winding will stabilize.

3 windings gets the inductance closest to 1.89 uH.

I soldered in two inductors with 3 turns of wire with 220 pF capacitors.  

I still see 6.5 dB of ripple in the pass band of the filter.

3-3-26
I changed how I made the inducters for the impedance matching circuit for the crystal filter. I've wound nagnet wire on the cardboard cylinder from Loula's poop bags. I wound 20 turns onto the cylinder and then connected it to the NanoVNA measurement jig. I could take a measurement of the inductance at the same time that I moved the wire windings on the tube. When I measured the correct inductance, I hot glued the wire in place. It was a really easy way to make these inductors. It's pretty easy to peel the hot glue off if you make a mistake, too.  
![Picture](pics/xtal_filter_with_impedance_matching.jpg)

I put two capacitors in parallel to get the capacitance that was calculated.

I tried this circuit with two series 500 Ohm pots at input and output. This eliminates pass band ripple but results in -17dB of insertion loss. (The resistance values that I found were 220 - 250 Ohms.) The LC impedance matching reduces that ripple almost as much, but there is only 2dB of insertion loss.

Links for impedance matching that I found useful:
https://www.n1fd.org/2024/05/21/crystal-filter/

https://passive-components.eu/impedance-matching-with-rf-lc-circuits/

https://circuitcellar.com/research-design-hub/basics-of-design/impedance-matching-fundamentals/

I used the calculator at toroids.info to calculate the inductance and capacitance.  
https://toroids.info/

OR

Another LC calculator for impedance matching  
https://www.leleivre.com/rf_lcmatch.html


The bottom circuit in the picture is for Z2 &lt; Z1 (I think)
![Picture](pics/toroids.info.png)

There is a discrepancy between the two calculators:

![Picture](pics/le_leivre_calculator.png)

The "series-L, parallel-C" circuits have different L and C values. ????

I used the values in the toroids.info calculator for the crystal filter.








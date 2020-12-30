#!/usr/bin/env python
"""
Reads & Prints KISS frames from a Serial console.

For use with programs like Dire Wolf.
"""

import aprs
import kiss


def main():
    frame = aprs.Frame()
    frame.source = aprs.Callsign('W2GMD-14')
    frame.destination = aprs.Callsign('PYKISS')
    frame.path = [aprs.Callsign('WIDE1-1')]
    frame.text = '>Hello World!'

    ki = kiss.SerialKISS(port='/dev/ttyu0', speed='9600')
    ki.start()
    ki.write(frame.encode_ax25())


if __name__ == '__main__':
    main()

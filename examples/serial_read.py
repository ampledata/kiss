#!/usr/bin/env python
"""
Reads & Prints KISS frames from a Serial console.

For use with programs like Dire Wolf.
"""


import aprs
import kiss
import logging


def print_frame(frame):
    try:
        # Decode raw APRS frame into dictionary of separate sections
        decoded_frame = aprs.util.decode_frame(frame)

        # Format the APRS frame (in Raw ASCII Text) as a human readable frame
        formatted_aprs = aprs.util.format_aprs_frame(decoded_frame)

        # This is the human readable APRS output:
        print formatted_aprs

    except Exception as ex:
        print ex
        print "Error decoding frame:"
        print "\t%s" % frame


def main():
    ki = kiss.SerialKISS(port='/dev/cu.AP510-DevB', speed='9600')
    ki._logger.setLevel(logging.INFO)
    ki.start()
    ki.read(callback=print_frame)


if __name__ == '__main__':
    main()

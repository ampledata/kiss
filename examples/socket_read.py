#!/usr/bin/env python
"""
Reads & Prints KISS frames from a TCP Socket.

For use with programs like Dire Wolf.

Mac OS X Tests
--------------

Soundflower, VLC & Dire Wolf as an audio-loopback-to-socket-bridge:

    1. Select "Soundflower (2ch)" as Audio Output.
    2. Play 'test_frames.wav' via VLC: `open -a vlc test_frames.wav`
    3. Startup direwolf: `direwolf "Soundflower (2ch)"`
    4. Run this script.


Dire Wolf as a raw-audio-input-to-socket-bridge:

    1. Startup direwolf: `direwolf - < test_frames.wav`
    2. Run this script.


Test output should be as follows:

    WB2OSZ-15>TEST:,The quick brown fox jumps over the lazy dog!  1 of 4
    WB2OSZ-15>TEST:,The quick brown fox jumps over the lazy dog!  2 of 4
    WB2OSZ-15>TEST:,The quick brown fox jumps over the lazy dog!  3 of 4
    WB2OSZ-15>TEST:,The quick brown fox jumps over the lazy dog!  4 of 4

"""


import aprs
import kiss
import logging


def print_frame(frame):
    try:
        # Decode raw APRS frame into dictionary of separate sections
        decoded_frame = aprs.util.decode_frame(frame[1:])

        # Format the APRS frame (in Raw ASCII Text) as a human readable frame
        formatted_aprs = aprs.util.format_aprs_frame(decoded_frame)

        # This is the human readable APRS output:
        print formatted_aprs

    except Exception as ex:
        print ex
        print "Error decoding frame:"
        print "\t%s" % frame


def main():
    ki = kiss.TCPKISS(host='localhost', port=8001)
    ki._logger.setLevel(logging.INFO)
    ki.start()
    ki.read(callback=print_frame)


if __name__ == '__main__':
    main()

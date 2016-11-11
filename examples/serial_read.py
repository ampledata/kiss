#!/usr/bin/env python
"""
Reads & Prints KISS frames from a Serial console.

Mac OS X Tests
--------------

Soundflower, VLC & Dire Wolf as an audio-loopback-to-socket-bridge:

    1. Select "Soundflower (2ch)" as Audio Output.
    2. Play 'test_frames.wav' via VLC: `open -a vlc test_frames.wav`
    3. Startup direwolf: `direwolf -p "Soundflower (2ch)"`
    4. Run this script.


Dire Wolf as a raw-audio-input-to-socket-bridge:

    1. Startup direwolf: `direwolf -p - < test_frames.wav`
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
        print frame
        # Decode raw APRS frame into dictionary of separate sections
        aprs_frame = aprs.APRSFrame(frame)

        # This is the human readable APRS output:
        print aprs_frame

    except Exception as ex:
        print ex
        print "Error decoding frame:"
        print "\t%s" % frame


def main():
    ki = kiss.SerialKISS(port='/dev/cu.Repleo-PL2303-00303114', speed='9600')
    #ki._logger.setLevel(logging.INFO)
    ki.start()
    ki.read(callback=print_frame, readmode=True)


if __name__ == '__main__':
    main()

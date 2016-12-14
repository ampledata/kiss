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


def print_frame(frame):
    print(aprs.Frame(frame))


def main():
    ki = kiss.TCPKISS(host='localhost', port=8001)
    ki.start()
    ki.read(callback=print_frame)


if __name__ == '__main__':
    main()

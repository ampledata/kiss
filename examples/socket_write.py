#!/usr/bin/env python
"""
Reads & Prints KISS frames from a TCP Socket.

For use with programs like Dire Wolf.
"""


import aprs
import kiss
import logging


def main():
    ki = aprs.APRSKISS(host='localhost', tcp_port=6666)
    ki._logger.setLevel(logging.DEBUG)
    ki.start()
    frame = {
        'source': 'W2GMD-14',
        'destination': 'PYKISS',
        'path': 'WIDE1-1',
        'text': '`25mfs>/"3x}'
    }
    ki.write(frame)


if __name__ == '__main__':
    main()

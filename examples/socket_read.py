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


def main2():

    frame = kiss.strip_df_start(x)

    for frame_slice in range(0, frame_len):
        # Is address field length correct?
        # Find the first ODD Byte followed by the next boundary:
        if (frame[frame_slice] & 0x01 and ((frame_slice + 1) % 7) == 0):
            i = int((frame_slice + 1) / 7)

            # Less than 2 callsigns?
            if 1 < i < 11:
                # For frames <= 70 bytes
                if frame_len >= frame_slice + 2:
                    if (frame[frame_slice + 1] & 0x03 == 0x03 and
                            frame[frame_slice + 2] in
                            [0xF0, 0xCF]):

                        text = frame[frame_slice + 3:]
                        print('Text={}'.format(text))

                        dest = aprs.Callsign(frame)
                        dest2 = aprs.Callsign2(frame, True)
                        print('{}'.format(dest))
                        print("{}".format(dest2.callsign))

                        src = aprs.Callsign(frame[7:])
                        src2 = aprs.Callsign2(frame[7:], True)
                        print("{}".format(src))
                        print("{}".format(src2.callsign))
                        path = []
                        for x in range(2, 1):
                            path_call = aprs.Callsign(frame[x * 7:])

                            if path_call:
                                if frame[x * 7 + 6] & 0x80:
                                    path_call.digi = True

                            path.append(path_call)
                        print("{}".format(path))

def test():
    # http://www.tapr.org/pdf/AX25.2.2.pdf
    import binascii
    import struct
    x =                                     b'\x00\xA8\x8A\xA6\xA8@@\xe0\xAE\x84d\x9e\xA6\xb4\xFF\x03\xF0,The quick brown fox jumps over the lazy dog!  0218 of 1000'
    y =         b'\x82\xA0\xA4\xA6@@`\x88\xAA\x9A\x9A\xB2@`\xAE\x92\x88\x8AB@b\xAE\x92\x88\x8AD@c\x03\xF0,The quick brown fox jumps over the lazy dog!  0218 of 1000'
    bs_header = b'\x82\xA0\xA4\xA6@@`\x88\xAA\x9A\x9A\xB2@`\xAE\x92\x88\x8AB@b\xAE\x92\x88\x8AD@c\x03\xF0'
    bs_packet = b'\x82\xA0\xA4\xA6@@`\x88\xAA\x9A\x9A\xB2@`\xAE\x92\x88\x8AB@b\xAE\x92\x88\x8AD@c\x03\xF0:Test\xF5G'
    expected_bytes = b'\x82\xa0\xa4\xa6@@`\x88\xaa\x9a\x9a\xb2@`\xae\x92\x88\x8ab@b\xae\x92\x88\x8ad@c\x03\xf0:Test\x9f/\xfb\x01'

    z = b'\x98\x94\x6E\xA0'

import binascii

def print_frame2(f):
    r = f[1:]
    print("Raw Frame={}".format(r))
    print("Hex Frame={}".format(binascii.hexlify(r)))

    encoded_destination = r[:7]
    print("       Len Dest={}".format(len(encoded_destination)))
    print("   Encoded Dest={}".format(encoded_destination))
    decoded_destination = decode_callsign(encoded_destination)
    print("   Decoded Dest={}".format(decoded_destination))
    reencoded_destination = encode_callsign2(decoded_destination)
    print("     2 Len Dest={}".format(len(reencoded_destination)))

    print("Re-Encoded Dest={}".format(reencoded_destination))
    redecoded_destination = decode_callsign(reencoded_destination)
    print("Re-Decoded Dest={}".format(redecoded_destination))
    print()
    assert(reencoded_destination == encoded_destination)
    assert(redecoded_destination == decoded_destination)

    encoded_source = r[7:14]
    print("       Len Source={}".format(len(encoded_source)))
    print("   Encoded Source={}".format(encoded_source))
    decoded_source = decode_callsign(encoded_source)
    print("   Decoded Source={}".format(decoded_source))
    reencoded_source = encode_callsign2(decoded_source)
    print("Re-Encoded Source={}".format(reencoded_source))
    redecoded_source = decode_callsign(reencoded_source)
    print("Re-Decoded Source={}".format(redecoded_source))
    print()
    assert(reencoded_source == encoded_source)
    assert(redecoded_source == decoded_source)


def encode_callsign1(full_callsign):
    encoded_callsign = b''
    ssid = '0'

    if '-' in full_callsign:
        full_callsign, ssid = full_callsign.split('-')

    full_callsign = "%-6s" % full_callsign

    for char in full_callsign:
        encoded_char = ord(char) << 1
        encoded_callsign += bytes([encoded_char])

    encoded_ssid = (int(ssid) << 1) | 0x60
    encoded_callsign += bytes([encoded_ssid])

    return encoded_callsign


def decode_callsign(encoded_callsign):
    assert(len(encoded_callsign) == 7)
    callsign = ''
    # To determine the encoded SSID:
    # 1. Right-shift (or un-left-shift) the SSID bit [-1].
    # 2. mod15 the bit (max SSID of 15).
    #
    ssid = str((encoded_callsign[-1] >> 1) & 15) # aka 0x0F
    for char in encoded_callsign[:-1]:
        callsign += chr(char >> 1)
    if ssid == '0':
        return callsign.strip()
    else:
        return '-'.join([callsign.strip(), ssid])


def encode_callsign2(callsign):
    callsign = callsign.upper()
    ssid = '0'
    encoded_callsign = b''

    if '-' in callsign:
        callsign, ssid = callsign.split('-')

    if 10 <= int(ssid) <= 15:
        # We have to call ord() on ssid here because we're receiving ssid as
        # a str() not bytes().
        ssid = chr(ord(ssid[1]) + 10)
        # chr(int('15') + 10)

    assert(len(ssid) == 1)
    assert(len(callsign) <= 6)

    callsign = "{callsign:6s}{ssid}".format(callsign=callsign, ssid=ssid)

    for char in callsign:
        encoded_char = ord(char) << 1
        encoded_callsign += bytes([encoded_char])
    return encoded_callsign


def print_frame(frame):
    print(aprs.Frame(frame[1:]))

def main():
    ki = kiss.TCPKISS(host='localhost', port=8001)
    ki.start()
    ki.read(callback=print_frame)




if __name__ == '__main__':
    main()

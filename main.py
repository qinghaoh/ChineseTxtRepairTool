"""
Copyright (c) 2023, Qinhao Hou
All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree.
"""

import argparse
import re


def parse():
    parser = argparse.ArgumentParser(description='Fix corrupted Chinese characters in a file.')
    parser.add_argument('--infile', type=str, required=True,
                        help='path of input file which has corrupted Chinese characters encoded in UTF-16BE')
    parser.add_argument('--outfile', type=str, required=True,
                        help='path of output file which has corrected Chinese characters encoded in GBK')
    return parser.parse_args()


def convert_uft8_to_gbk(utf8_chars: str) -> str:
    utf16_bytes = utf8_chars.encode('utf-16be')
    # print(type(utf16_bytes))
    # trims \x00 bytes
    # e.g. b'\x00\xb8\x00\xfc' -> [b'\xb8', b'\xfc']
    trimmed_uft16_bytes = bytes(b for b in utf16_bytes)[1::2]

    index = 0
    corrected_chars = ''
    while index < len(trimmed_uft16_bytes):
        utf16_byte = b''

        if trimmed_uft16_bytes[index] > 127:
            utf16_byte = trimmed_uft16_bytes[index: index + 2]
            index += 2
        else:
            # preserves ASCII characters
            utf16_byte = trimmed_uft16_bytes[index].to_bytes(1, 'big')
            index += 1

        try:
            corrected_chars += utf16_byte.decode('gbk')
        except UnicodeDecodeError:
            # private use area code point
            corrected_chars += '\ue009'

    return corrected_chars


if __name__ == '__main__':
    args = parse()

    with open(args.infile, mode='r') as infile:
        with open(args.outfile, mode="w", encoding='utf-8') as outfile:
            for line in infile:
                converted_line = ''.join(group if group.isspace() else convert_uft8_to_gbk(group)
                                         for group in re.split(r'(\s+)', line))
                outfile.write(converted_line)

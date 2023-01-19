"""
Copyright (c) 2023, Qinhao Hou
All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree.
"""

import argparse
import locale


def parse():
    parser = argparse.ArgumentParser(description='Fix corrupted Chinese characters in a file.')
    parser.add_argument('--infile', type=str, required=True,
                        help='path of input file which has corrupted Chinese characters encoded in UTF-16BE')
    parser.add_argument('--outfile', type=str, required=True,
                        help='path of output file which has corrected Chinese characters encoded in GBK')
    return parser.parse_args()


def gbk_encode(input_bytes: bytes) -> str:
    index = 0
    gbk_encoded_chars = ''
    while index < len(input_bytes):
        utf16_byte = b''
        if input_bytes[index] > 127:
            utf16_byte = input_bytes[index: index + 2]
            index += 2
        else:
            # preserves ASCII characters
            utf16_byte = input_bytes[index].to_bytes(1, 'big')
            index += 1

        try:
            gbk_encoded_chars += utf16_byte.decode('gbk')
        except UnicodeDecodeError:
            # private use area code point
            gbk_encoded_chars += '\ue009'

    return gbk_encoded_chars


if __name__ == '__main__':
    args = parse()

    input_encoding = locale.getpreferredencoding()

    line_count = 0
    with open(args.infile, mode='rb') as infile:
        with open(args.outfile, mode="w", encoding='utf-8') as outfile:
            for line in infile:
                encoded_line = gbk_encode(line)
                outfile.write(encoded_line)
                line_count += 1

    print("Input file encoding: {}".format(input_encoding))
    print("Number of processed lines: {}".format(line_count))

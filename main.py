"""
Copyright (c) 2023, Qinhao Hou
All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree.
"""

import argparse
import codecs
import locale


def parse():
    parser = argparse.ArgumentParser(description='Fix non-GBK characters in a file.')
    parser.add_argument('--infile', type=str, required=True,
                        help='path of input file which has corrupted simplified Chinese characters')
    parser.add_argument('--outfile', type=str, required=True,
                        help='path of output file which has corrected simplified Chinese characters encoded in GBK')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse()

    input_encoding = locale.getpreferredencoding()

    # The user-defined error handler is based on the assumption that the input bytes
    # can be split into UTF-16 units, i.e. pairs of bytes
    # The error handler 'replace' uses U+FFFD as the official REPLACEMENT CHARACTER
    # so, we use it here as well.
    codecs.register_error('utf16replace', lambda exc: ('\ufffd', exc.end + 1))
    line_count = 0
    with open(args.infile, mode='rb') as infile:
        with open(args.outfile, mode="w", encoding='utf-8') as outfile:
            for line in infile:
                encoded_line = line.decode(encoding='gbk', errors='utf16replace')
                outfile.write(encoded_line)
                line_count += 1

    print("Input file encoding: %s" % input_encoding)
    print("Number of processed lines: %d" % line_count)

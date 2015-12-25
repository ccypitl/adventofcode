#!/usr/bin/env python
import re


def main():
    input_file = 'input.txt'
    with open(input_file, 'r') as f:
        strings = [l.rstrip() for l in f]
    s_sim_re = re.compile(r'(\\(?![xX][0-9a-fA-F]{2}).)')
    s_hex_re = re.compile(r'(\\[xX][0-9a-fA-F]{2})')
    end_sizes = []
    for s in strings:
        s_clipped = s[1:-1]
        line = s_sim_re.sub('S', s_clipped)
        line = s_hex_re.sub('H', line)
        end_size = len(s) - len(line)
        end_sizes.append(end_size)
    print sum(end_sizes)


if __name__ == '__main__':
    main()

#!/usr/bin/env python
import hashlib


def main():
    input_file = 'input.txt'
    with open(input_file, 'r') as f:
        key = f.read()
    i = 0
    while True:
        m = hashlib.md5()
        com = key + str(i)
        m.update(com)
        digest = m.hexdigest()
        if digest[:5].startswith('00000'):
            print digest
            print com
            print i
            break
        i += 1


if __name__ == '__main__':
    main()

#!/usr/bin/env python


def main():
    input_file = 'input.txt'
    with open(input_file, 'r') as f:
        instr = f.read()
    incr = instr.count('(')
    decr = instr.count(')')
    print incr - decr


if __name__ == '__main__':
    main()

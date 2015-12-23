#!/usr/bin/env python
import re


def main():
    # Get input data
    input_file = 'input.txt'
    ins_re = re.compile(r'^(?:turn )*(.+?) ([0-9]+),([0-9]+) through '
                        '([0-9]+),([0-9]+)$')
    with open(input_file, 'r') as f:
        instructions = [ins_re.findall(l.rstrip())[0] for l in f]
    # Set up lights dict
    lights = {}
    for (x, y) in gen_loc(0, 1000, 0, 1000):
        if x not in lights:
            lights[x] = {}
        lights[x][y] = -1

    # Apply instructions
    for ins in instructions:
        com = ins[0]
        x_start, y_start, x_end, y_end = map(int, ins[1:])
        for (x, y) in gen_loc(x_start, x_end, y_start, y_end):
            lights[x][y] = apply_instruction(com, lights[x][y])

    # Count lights that are on
    count = 0
    for x, values in lights.iteritems():
        for y, state in values.iteritems():
            if state == 1:
                count += 1
    print count


def gen_loc(x_start, x_end, y_start, y_end):
    for i in xrange(x_start, x_end+1):
        for j in xrange(y_start, y_end+1):
            yield (i, j)


def apply_instruction(com, cur):
    if com == 'on':
        return 1
    elif com == 'off':
        return -1
    elif com == 'toggle':
        return cur * -1


if __name__ == '__main__':
    main()

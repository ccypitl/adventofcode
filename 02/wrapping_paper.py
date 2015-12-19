#!/usr/bin/env python
import itertools


def main():
    input_file = 'input.txt'
    with open(input_file, 'r') as f:
        dims = [map(int, l.rstrip().split('x')) for l in f]
    total_wrapping = 0
    for dim in dims:
        prods = map(lambda x: 2*x[0]*x[1], itertools.combinations(dim, r=2))
        area = sum(prods)
        smallest_side = min(prods) / 2
        total_wrapping += (area + smallest_side)
    print total_wrapping


if __name__ == '__main__':
    main()

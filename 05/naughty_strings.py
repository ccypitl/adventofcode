#!/usr/bin/env python
import string as stringlib


def main():
    input_file = 'input.txt'
    doubles = [l*2 for l in stringlib.ascii_lowercase]
    with open(input_file, 'r') as f:
        strings = [l.rstrip() for l in f]
    nice_strings = []
    for string in strings:
        # At least three vowels aeiou
        num_vowels = sum([string.count(l) for l in 'aeiou'])
        if num_vowels < 3:
            continue
        # At least one letter than appears twice in a row
        if not any(d in string for d in doubles):
            continue
        # Does not contain one of these strings ab, cd, pq, or xy
        if any(b in string for b in ['ab', 'cd', 'pq', 'xy']):
            continue
        nice_strings.append(string)
    print len(nice_strings)

if __name__ == '__main__':
    main()

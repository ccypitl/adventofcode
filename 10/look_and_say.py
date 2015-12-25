#!/usr/bin/env python


def main():
    input_file = 'input.txt'
    with open(input_file, 'r') as f:
        sequence = f.read().rstrip()
    look_say_str = sequence
    for i in xrange(0, 40):
        print i + 1
        look_say_str = look_and_say(look_say_str)
    print 'length:', len(look_say_str)


def look_and_say(d):
    ### This is very inefficient...
    # Converting to list of characters
    s = list(d)
    # Initialising resulting sequence string
    new_s = ''
    # Getting first letter; setting count
    l = s.pop(0)
    l_count = 1
    # Iterating remaining letters in input sequence
    while s:
        # Grab the next letter
        n = s.pop(0)
        if n == l:
            # If it's the same; add to counter
            l_count += 1
        else:
            # If different, add count to resulting string and reset
            new_s = new_s + str(l_count) + str(l)
            l_count = 1
            l = n
        # Catching a single new digit at the new of a sequence
        if len(s) == 0:
            new_s = new_s + str(l_count) + str(l)
    return new_s


if __name__ == '__main__':
    main()

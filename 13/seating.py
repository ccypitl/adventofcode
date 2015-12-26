#!/usr/bin/env python
import re
import copy


class Seating(object):

    def __init__(self, happiness_strings):
        self.in_str = happiness_strings
        self.happy_map = {}
        self.map_happiness_strings()
        self.guests = self.happy_map.keys()
        self.happiness = []


    def map_happiness_strings(self):
        happy_re = re.compile(r'^(.+?) would (.+?) ([0-9]+).+?to (.+)\.$')
        for s in self.in_str:
            # Get regex match groups
            source, modifier, happy_units, target = happy_re.match(s).groups()
            # If lose modifier, make happy unit negative
            if modifier == 'lose':
                happy_units = int(happy_units) * -1
            elif modifier == 'gain':
                happy_units = int(happy_units)
            # Initialise source dict if it does not exist
            if source not in self.happy_map:
                self.happy_map[source] = {}
            # Assign value to dict
            self.happy_map[source][target] = happy_units


    def start_seating(self):
        # Selecting starting guests
        for guest in self.guests:
            happiness = {}
            seated = []
            # Calling recursive function to find all possible seating
            self.iterate_seating(guest, seated, happiness)


    def iterate_seating(self, current, seated, happiness):
        # Need to copy mutable types during recursion
        seated = copy.copy(seated)
        happiness = copy.deepcopy(happiness)
        # Add seated guest (current) to seated list
        seated.append(current)
        # Determine guests that are unseated
        unseated = [g for g in self.guests if g not in seated]
        # If all guests have been seated, sum total happiness and record
        if not unseated:
            # Need to add last two sitting next to each other (close the loop)
            g1, g2 = [g for g, v in happiness.iteritems() if len(v) < 2]
            happiness[g1][g2] = self.happy_map[g1][g2]
            happiness[g2][g1] = self.happy_map[g2][g1]
            # Sum all happy units
            seat_happiness = [sum(v.values()) for v in happiness.values()]
            table_happiness = sum(seat_happiness)
            # Append happy units to variable
            self.happiness.append(table_happiness)
            return
        # Iterate all unseated guests and make recursive call
        for guest in unseated:
            # Need a new copy of this for the loop to operate independently
            new_happiness = copy.deepcopy(happiness)
            # Get happy units for seated guests (current) and the newly seated
            happy_units = self.happy_map[current][guest]
            # Need to add seating both ways to the dict; check if key exists
            if current not in new_happiness:
                new_happiness[current] = {}
            if guest not in new_happiness:
                new_happiness[guest] = {}
            # Add seatings (both ways)
            new_happiness[current][guest] = self.happy_map[current][guest]
            new_happiness[guest][current] = self.happy_map[guest][current]
            # Call recursively
            self.iterate_seating(guest, seated, new_happiness)


def main():
    input_file = 'input.txt'
    with open(input_file, 'r') as f:
        happiness_strings = [l.rstrip() for l in f]
    # Create Seating instance and apply regex to input strings
    seating = Seating(happiness_strings)
    # Determine all possible seating arrangements and associated happiness
    seating.start_seating()
    # Print maximum happiness
    print max(seating.happiness)


if __name__ == '__main__':
    main()

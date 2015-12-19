#!/usr/bin/env python
# Using a dictionary of co-ordinate tuples to record Santa vistations


# Empty class to hold positions
class Santa(object):

    def __init__(self):
        # Set up santa
        self.x = 0
        self.y = 0
        self.houses = {self.pos: 1}

    def give_instruction(self, char):
        # Decode instruction
        if char == '^':
            self._move(0, 1)
        elif char == 'v':
            self._move(0, -1)
        elif char == '>':
            self._move(1, 0)
        elif char == '<':
            self._move(-1, 0)

    def _move(self, x, y):
        # Move santa, record house visited
        self.x += x
        self.y += y
        if self.pos in self.houses:
            self.houses[self.pos] += 1
        else:
            self.houses[self.pos] = 1

    @property
    def pos(self):
        return (self.x, self.y)


def main():
    # Wake up santa
    santa = Santa()
    # Get instructions
    input_file = 'input.txt'
    with open(input_file, 'r') as f:
        moves = f.read().rstrip()
    # Send santa to houses
    for direction in moves:
        santa.give_instruction(direction)
    # Count houses which recieved at least one present
    print len(santa.houses)


if __name__ == '__main__':
    main()

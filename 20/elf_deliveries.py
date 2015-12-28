#!/usr/bin/env python


class DeliveryControl(object):


    def __init__(self):
        self.count = 0


    def iterate_houses(self):
        while True:
            self.count += 1
            elves = self.factors(self.count)
            yield House(self.count, elves)

    @staticmethod
    def factors(n):
        # Quickly find factors - taken from stackoverflow.com/a/6800214
        return set(reduce(list.__add__,
                            ([i, n//i] for i in range(1, int(n**0.5) + 1)
                                if n % i == 0)))


class House(object):


    def __init__(self, number, elves):
        self.number = number
        self.elves = elves
        self.presents = sum(self.elves) * 10


def main():
    input_file = 'input.txt'
    with open(input_file, 'r') as f:
        present_target = int(f.read().rstrip())
    deliveries = DeliveryControl()
    # Iterate houses until we meet target
    for house in deliveries.iterate_houses():
        if house.presents >= present_target:
            print 'House:', house.number
            print 'Presents:', house.presents
            return


if __name__ == '__main__':
    main()

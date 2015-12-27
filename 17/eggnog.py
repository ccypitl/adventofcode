#!/usr/bin/env python
import itertools


class EggNogFiller(object):


    def __init__(self, eggnog, containers):
        self.eggnog = eggnog
        self.containers = containers
        self.combinations = 0


    def container_combinations(self):
        # Iterate through all possible combination lengths
        for i in xrange(1, len(self.containers)+1):
            # Iterate all possible combinations
            for p in itertools.combinations(self.containers, i):
                # If the combination sums to exactly 150, count combination
                if sum(p) == 150:
                    self.combinations += 1


def main():
    input_file = 'input.txt'
    with open(input_file, 'r') as f:
        containers = [int(l) for l in f]
    # Initialise instance
    eggnog_filler = EggNogFiller(100, containers)
    # Count combinations which hold exactly 150 litres
    eggnog_filler.container_combinations()
    # Print number of combinations
    print eggnog_filler.combinations


if __name__ == '__main__':
    main()

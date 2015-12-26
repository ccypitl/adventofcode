#!/usr/bin/env python
import re
import math


def main():
    input_file = 'input.txt'
    with open(input_file, 'r') as f:
        spec_strings = [l.rstrip() for l in f]
    race_time = 2503
    distances = {}
    for reindeer, specs in process_spec_strings(spec_strings):
        distances[reindeer] = get_distance(specs, race_time)
    print max(distances.values())


def process_spec_strings(ss):
    spec_re = re.compile(r'^(.+?) can.+?([0-9]+).+?([0-9]+).+?([0-9]+).+$')
    for s in ss:
        # Get regex groups
        result = spec_re.match(s).groups()
        # Split into name and specs; cast specs to int
        reindeer = result[0]
        specs = map(int, result[1:])
        yield (reindeer, specs)


def get_distance(specs, race_time):
    # Unpack specs
    fly_speed, fly_time, rest_time = specs
    # Determine full fly/rest cycle time
    cycle_time = fly_time + rest_time
    # Get number of cycles completed
    cycles = math.floor(race_time / float(cycle_time))
    # Get distance for completed cyles
    distance = cycles * (fly_speed * fly_time)
    # Get remaining time (partial cycle)
    remaining = race_time % cycle_time
    # Determine extra fly time in partial cycle
    if remaining > fly_time:
        extra_time = fly_time
    else:
        extra_time = remaining
    # Calculate extra distance in partial cycle
    extra_distance = fly_speed * extra_time
    # Get total distance
    return distance + extra_distance


if __name__ == '__main__':
    main()

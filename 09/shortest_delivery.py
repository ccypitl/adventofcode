#!/usr/bin/env python
import re
import copy


class Travel(object):

    def __init__(self, distances):
        self.distances = distances
        self.locations = self.distances.keys()
        self.route_distances = []


    def start_travel(self):
        # Not entirely sure this is necessary, but this is how it is
        for location in self.locations:
            visited = []
            distance = 0
            self.travel(location, visited, distance)


    def travel(self, current, visited, distance):
        # Copying list here so we don't operate on other route visited lists
        visited = copy.copy(visited)
        # Add travelled city to visited list
        visited.append(current)
        # Get list of univisted cities
        unvisited = [l for l in self.locations if l not in visited]
        # If we've exhausted the list of visited cities, we're done
        if not unvisited:
            # Visited everyone! Add distance to instance variable
            self.route_distances.append(distance)
        # Get a list of all available cities
        connecting = self.distances[current]
        # Exclude available cities that we've already visited
        unvisited_connecting = [l for l in connecting if l not in visited]
        # Iterate each unvisited, available city and travel there
        for location in unvisited_connecting:
            # Getting distance to new city
            travel_distance = self.distances[current][location]
            # Travel! Making distance addition in args to avoid loop additions
            self.travel(location, visited, distance + travel_distance)


def main():
    input_file = 'input.txt'
    input_re = re.compile(r'^(.+?) to (.+?) = ([0-9]+)$')
    distances = {}
    with open(input_file, 'r') as f:
        for line in f:
            # Mapping boths ways; end to start and start to end
            s, e, d = input_re.match(line.rstrip()).groups()
            if s not in distances:
                distances[s] = {}
            if e not in distances:
                distances[e] = {}
            distances[s][e] = int(d)
            distances[e][s] = int(d)
    # Get list of required locations; using class so that a single variable to
    # hold distances is always available
    traveller = Travel(distances)
    traveller.start_travel()
    print min(traveller.route_distances)



if __name__ == '__main__':
    main()

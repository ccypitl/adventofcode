#!/usr/bin/env python
import itertools

# find neighbours once
# then iterate 100 steps


class Grid(object):


    def __init__(self, light_states):
        self.in_states = light_states
        self.grid = {}
        self.lights = []
        self.process_light_states()


    def process_light_states(self):
        for i, row in enumerate(self.in_states):
            # Initialise row dictionary
            self.grid[i] = {}
            # Creating Light class for each element and putting in lights dict
            for j, state in enumerate(row):
                light = Light(state, i, j)
                self.lights.append(light)
                self.grid[i][j] = light
        # Setting in Light class so that they can access easily
        Light.grid = self.grid
        Light.grid_rows = len(self.grid)
        Light.grid_cols = len(self.grid.values()[0])
        # Call function get initialise neighbour on/off states
        self.get_neighbour_states()


    def update_light_states(self):
        # Call function in each Light instance to determine new state
        for light in self.lights:
            light.update_state()
        self.get_neighbour_states()

    def get_neighbour_states(self):
        # Call function in each Light instance to get neighbours
        for light in self.lights:
            light.get_neighbours_state()

    def count_lights_on(self):
        return len([l for l in self.lights if l.state])


    def print_grid(self):
        for row in self.grid.values():
            text = []
            for light in row.values():
                if light.state:
                    text.append('#')
                else:
                    text.append('.')
            print ''.join(text)


class Light(object):

    # Set by Grid class when initialised; hold position for all lights
    grid = None
    grid_rows = None
    grid_cols = None

    def __init__(self, state, row, col):
        # Convert character state to boolean
        if state == '.':
            self.state = False
        elif state == '#':
            self.state = True
        # Set position
        self.row = row
        self.col = col


    def update_state(self):
        if self.state:
            if self.neighbour_states['on'] not in [2, 3]:
                self.state = False
        else:
            if self.neighbour_states['on'] == 3:
                self.state = True


    def get_neighbours_state(self):
        self.neighbour_states = {'on': 0, 'off': 0}
        for x, y in self.neighbour_locations():
            # If light falls outside of grid, set state to 'off'
            if x < 0 or y < 0:
                self.neighbour_states['off'] += 1
                continue
            elif (x + 1) > self.grid_rows or (y + 1) > self.grid_cols:
                self.neighbour_states['off'] += 1
                continue
            # Get neighbouring light state and add to count
            neighbour_state = self.grid[x][y].state
            if neighbour_state:
                self.neighbour_states['on'] += 1
            else:
                self.neighbour_states['off'] += 1


    def neighbour_locations(self):
        x = [self.row-1, self.row+1, self.row]
        y = [self.col-1, self.col+1, self.col]
        for xi, yi in itertools.product(x, y):
            # Don't return this light's position
            if self.row == xi and self.col == yi:
                continue
            yield xi, yi


def main():
    input_file = 'input.txt'
    steps = 100
    with open(input_file, 'r') as f:
        light_states = [l.rstrip() for l in f]
    grid = Grid(light_states)
    for i in xrange(0, 100):
        grid.update_light_states()
    print grid.count_lights_on()


if __name__ == '__main__':
    main()

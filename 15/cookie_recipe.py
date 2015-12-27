#!/usr/bin/env python
import re
import copy


class RecipeChooser(object):


    def __init__(self, ingredient_strings):
        self.in_str = ingredient_strings
        self.ingredients = {}
        self.process_ingredient_strings()
        self.combinations = []
        self.calculate_combinations()
        self.cookie_scores = []


    def process_ingredient_strings(self):
        prop_re = re.compile(r'([a-z]+?) (-*[0-9]+)')
        name_re = re.compile(r'^(.+?):.+$')
        # Create a dict with name as key containing proper -> value dict
        for s in self.in_str:
            name = name_re.match(s).groups()[0]
            prop = prop_re.findall(s)
            self.ingredients[name] = {k: int(v) for k, v in prop}


    def calculate_recipe_scores(self):
        # Group all properties in a dict by key
        prop_keys = self.ingredients.values()[0].keys()
        # Zipping so that all the property values are grouped
        prop_values = zip(*[v.values() for v in self.ingredients.values()])
        # Generating dict; zipping the respective keys and property groups
        # Exclude calories for cookie scoring
        self.prop_dict = {k: v for k, v in zip(prop_keys, prop_values) if k !=
                'calories'}
        # Iterate over all combinations and calculate cookie score for each
        for combination in self.combinations:
            # Get a list of product sums for each property
            product_sums = [s for s in self.property_product(combination)]
            # Multiply all sums together
            cookie_score = reduce(lambda x, y : x*y, product_sums)
            # Add cookie score to variable
            self.cookie_scores.append(cookie_score)


    def property_product(self, combination):
        for k ,v in self.prop_dict.iteritems():
            # Zip the combination count and ingredient prop for multi.
            products = [c*v for c, v in zip(combination, v)]
            # Get sum of a properties product
            product_sum = sum(products)
            # If the product sum is negative, set it to zero
            if product_sum < 0:
                product_sum = 0
            # Yield the product sum
            yield product_sum


    def calculate_combinations(self, end=101, counts=None):
        # New instance of list
        if not counts:
            counts = []
        # If at second last position, calc last pos and return
        if len(counts) == 3:
            # Last position count is the number of choices - used choices
            total = sum(counts)
            counts.append(100-total)
            self.combinations.append(counts)
            return
        # Loop and call recursively
        for i in xrange(0, end):
            # Must copy so that we don't change during looping
            recurse_counts = copy.copy(counts)
            # Append count for position
            recurse_counts.append(i)
            # Make recursive call
            self.calculate_combinations(end-i, recurse_counts)


def main():
    input_file = 'input.txt'
    with open(input_file, 'r') as f:
        ingredient_strings = [l.rstrip() for l in f]
    # Initialise instance and process ingredient strings
    recipes = RecipeChooser(ingredient_strings)
    # Calculate all possible recipes and cookie scores
    recipes.calculate_recipe_scores()
    # Print the highest cookie score
    print max(recipes.cookie_scores)


if __name__ == '__main__':
    main()

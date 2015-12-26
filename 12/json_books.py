#!/usr/bin/env python
import json


class Accountant(object):


    def __init__(self, transactions):
        self.net = 0
        self.transactions = transactions


    def account(self):
        self.iterate(self.transactions)


    def iterate(self, ds):
        # If type is still iterable, iterate it; else if a number or string
        # number, add it to running total
        if hasattr(ds, '__iter__'):
            # If dict combine key + values and then iter; if list just iter
            if isinstance(ds, dict):
                ns = ds.keys() + ds.values()
                for n in ns:
                    self.iterate(n)
            elif isinstance(ds, list):
                for d in ds:
                    self.iterate(d)
        elif isinstance(ds, int):
            self.net += ds
        elif self.str_num(ds):
            self.net += int(ds)


    @staticmethod
    def str_num(t):
        # Check if string represents an integer
        try:
            int(t)
        except ValueError:
            return False
        else:
            return True


def main():
    input_file = 'input.txt'
    with open(input_file, 'r') as f:
        transactions_json = f.read().rstrip()
    # Read in JSON format
    transactions = json.loads(transactions_json)
    # Initialise Accountant class
    accountant = Accountant(transactions)
    # Count numbers
    accountant.account()
    print accountant.net


if __name__ == '__main__':
    main()

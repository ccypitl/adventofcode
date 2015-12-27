#!/usr/bin/env python
import re


class AuntSue(object):

    # Regexes for processing input strings
    aunt_prop_re = re.compile(r' ([^0-9]+?): ([0-9]+)')
    aunt_num_re = re.compile(r'^Sue ([0-9]+).+$')

    def __init__(self, aunt_string):
        self.aunt_string = aunt_string
        self.process_aunt_string()


    def process_aunt_string(self):
        # Get regex matches
        props = self.aunt_prop_re.findall(self.aunt_string)
        aunt_num = self.aunt_num_re.match(self.aunt_string).groups()[0]
        # Created dict from match groups
        self.properties = {k: v for k, v in props}
        # Set aunt number
        self.num = aunt_num


class Reference(object):

    # Regexes for processin input strings
    reference_re = re.compile(r'^(.+?): ([0-9]+)')

    def __init__(self, reference_strings):
        self.reference_strings = reference_strings
        self.process_reference_string()


    def process_reference_string(self):
        # Get regex matches
        props = [self.reference_re.match(s).groups() for s in
                    self.reference_strings]
        # Create dict from match groups
        self.properties =  {k: v for k, v in props}


    def __eq__(self, other):
        # If other contains prop and is equal for all, return True. If has prop
        # and doesn't equal, return False. No penalty for missing keys.
        for k, v in other.properties.iteritems():
            if k in self.properties:
                if not self.properties[k] == v:
                    return False
        return True


def main():
    # Read in the aunt's properties and reference properties
    input_file = 'input.txt'
    reference_file = 'reference.txt'
    with open(input_file, 'r') as f:
        aunt_strings = [l.rstrip() for l in f]
    with open(reference_file, 'r') as f:
        ref_strings = [l.rstrip() for l in f]
    # Create an AuntSue instance for each aunt
    aunts = [AuntSue(s) for s in aunt_strings]
    # Create a reference instance
    reference = Reference(ref_strings)
    # For each aunt see if it 'equals' the reference; print aunt num if so
    for aunt in aunts:
        if reference == aunt:
            print aunt.num


if __name__ == '__main__':
    main()

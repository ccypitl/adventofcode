#!/usr/bin/env python
import re
import copy


class Plant(object):


    def __init__(self, molecule, rule_strings):
        self.one_rep_molecules = set()
        self.molecule = molecule
        self.molecule_chars = list(molecule)
        self.rule_strings = rule_strings
        self.rules = self.process_rule_strings()
        self.rule_lengths = set([len(rs) for rs, rt in self.rules])
        self.kmers = {l: self.generate_kmers(l) for l in self.rule_lengths}


    def process_rule_strings(self):
        '''Create regexes from rule strings'''
        rule_string_re = re.compile(r'^(.+?) => (.+)$')
        return [rule_string_re.match(r).groups() for r in self.rule_strings]


    def generate_kmers(self, kmer_size):
        # Return list of single characters of molecule for kmers of 1
        if kmer_size == 1:
            # Get start/end indices to enable interop with calibrate_plant
            start = range(0, len(self.molecule))
            end = range(1, len(self.molecule)+1)
            chars = list(self.molecule)
            # Zip each list and return
            return zip(chars, start ,end)
        kmers = []
        # Get the last index we'll need
        idx_end = len(self.molecule) - (kmer_size -1)
        # Cycle over molecule
        for i in xrange(0, idx_end):
            # Get each kmer and position and append to list
            start = i
            end = i + kmer_size
            kmers.append((self.molecule[start:end], start, end))
        return kmers


    def calibrate_plant(self):
        '''Find all molecules one replacement away'''
        for source, target in self.rules:
            # Get a copy of the n-kmer list, we'll be deleting entries
            kmers = copy.copy(self.kmers[len(source)])
            # Collect allmatching kmers from kmer list
            matches = [k for k in kmers if k[0] == source]
            # If no kmers, next
            if not matches:
                continue
            # For each match, generate a one-step replacement molecule
            self.make_replacements(matches, target)


    def make_replacements(self, matches, target):
        # Reverse so that mole. chars. del from the end, preserving indexes
        for match in matches[::-1]:
            # Copy list of molecule characters so we can modify it
            molecule_chars = copy.copy(self.molecule_chars)
            # Delete the matched characters
            molecule_chars[match[1]:match[2]] = ''
            # Add the replacement
            molecule_chars.insert(match[1], target)
            # Update set of one-step replacments with new molecule
            self.one_rep_molecules.update([''.join(molecule_chars)])


def main():
    input_file = 'input.txt'
    with open(input_file, 'r') as f:
        # Only keep lines that have text (other than ret. char.)
        lines = [l.rstrip() for l in f if l.rstrip()]
    # Split lines into rules and input molecule
    rule_strings = [l for l in lines if '=>' in l]
    molecule = [l for l in lines if not '=>' in l][0]
    # Initialise cheical plant instance
    plant = Plant(molecule, rule_strings)
    # Calculate all molecules one replacement away
    plant.calibrate_plant()
    print len(plant.one_rep_molecules)


if __name__ == '__main__':
    main()

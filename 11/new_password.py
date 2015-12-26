#!/usr/bin/env python


class Password(object):

    alpha = 'abcdefghijklmnopqrstuvwxyz'

    def __init__(self, password):
        # Map each alpha to the next proceeding alpha and manually add the 'z'
        self.alpha_dict = {self.alpha[i]: self.alpha[i+1] for i in xrange(0,
            len(self.alpha)-1)}
        self.alpha_dict['z'] = 'a'
        # Generate 3mers for the incrementing three straight rule
        self.alpha_3mers = set(self.generate_kmers(self.alpha, 3))
        # Set password input variable
        self.in_pwd = password
        self.cur_pwd = self.in_pwd


    def __iter__(self):
        return self


    def next(self):
        # Increments passwords until one passes the rules
        password = self.increment(self.cur_pwd)
        while not self.check_password(password):
            password = self.increment(password)
        self.cur_pwd = password
        return self.cur_pwd


    def check_password(self, password):
        # Must not contain the letters i, o or l
        if any(l in password for l in ['i', 'o', 'l']):
                return False
        # Must contain a increasing straight of three letters (e.g. abc)
        password_3mers = self.generate_kmers(password, 3)
        if not any(k in self.alpha_3mers for k in password_3mers):
            return False
        # At least two different, non-overlapping pairs of letters
        password_2mers = self.generate_kmers(password, 2)
        if not self.dual_pairs(password_2mers):
            return False
        return True


    @staticmethod
    def dual_pairs(kmers):
        pairs = 0
        while kmers:
            kmer = kmers.pop(0)
            # If single single in 2kmer, count and remove next to avoid overlap
            if len(set(kmer)) == 1:
                pairs += 1
                # Only remove next if one exists...
                if kmers:
                    del kmers[0]
        # Check the number of pairs found
        if pairs < 2 :
            return False
        else:
            return True


    def increment(self, in_string):
        # Convert string to list
        in_list = list(in_string)
        # Get last character to increment
        last_alpha = in_list[-1]
        # If 'z' last character must increment second last also; recursive
        if last_alpha == 'z':
            new_last_alpha = self.alpha_dict[last_alpha]
            first_alphas = in_string[:-1]
            # Catch if we're going to x -> aa
            if first_alphas:
                new_first_alphas = self.increment(first_alphas)
            else:
                new_first_alphas = 'a'
            return new_first_alphas + new_last_alpha
        else:
            in_list[-1] = self.alpha_dict[last_alpha]
        return ''.join(in_list)


    @staticmethod
    def generate_kmers(s, k):
        kmers = []
        idx_end = len(s) - (k -1)
        for i in xrange(0, idx_end):
            start = i
            end = i + k
            kmers.append(s[start:end])
        return kmers


def main():
    input_file = 'input.txt'
    with open(input_file, 'r') as f:
        password_string = f.read().rstrip()
    password = Password(password_string)
    next_password = next(password)
    print next_password


if __name__ == '__main__':
    main()

#!/usr/bin/env python
# Description: Read all the input instructions. Initial processing done by
# using regex to determine instruction type. Once instruction type has been
# determined, an appropriate instruction instance is created. All instruction
# instances are cycled through as a queue and if the requirements are meet
# (parents) then the instruct is executed. If not, then the instruction is
# placed back into the queue for later evaluation (when dependencies have been
# met).


import re
import sys


class Instruction(object):


    def __init__(self, raw_instruction, raw_params):
        # Set some values
        self.ins_str = raw_instruction
        self.raw_params = raw_params
        self.parents = [] # Need this when searching to tist. b/n val and par
        self.value = None
        # Assign paramenters
        self.target = self.raw_params[-1]
        self.input_params = self.raw_params[:-1]
        self.params = {}
        for input_param in self.input_params:
            if self.is_str_int(input_param):
                # Add value to params dictionary
                self.params[input_param] = int(input_param)
            else:
                # Add parent to parents list + make 'value' for later calc
                self.params[input_param] = None
                self.parents.append(input_param)


    @staticmethod
    def is_str_int(in_string):
        # Function to check if a string is a integer
        try:
            int(in_string)
        except ValueError:
            return False
        else:
            return True


    def add_value(self, parent):
        # Add value to params dict
        self.params[parent] = parent.value


    @staticmethod
    def process_instruction(raw_instruction):
        # Process raw instruction string using regex
        ins_res = {NotInstruction: re.compile(r'^NOT (.+?) -> (.+)'),
                AndInstruction: re.compile(r'^(.+?) AND (.+?) -> (.+)'),
                OrInstruction: re.compile(r'^(.+?) OR (.+?) -> (.+)'),
                LShiftInstruction: re.compile(r'^(.+?) LSHIFT (.+) -> (.+)'),
                RShiftInstruction: re.compile(r'^(.+?) RSHIFT (.+) -> (.+)'),
                InputInstruction: re.compile(r'^([0-9a-z]+?) -> (.+)')}
        # Find regex match
        for ins_type, ins_re in ins_res.iteritems():
            re_result = ins_re.match(raw_instruction)
            if re_result:
                return ins_type(raw_instruction, re_result.groups())
        else:
            print 'Couldn\'t assign instruction to type:\n%s' % raw_instruction
            sys.exit(1)


class InputInstruction(Instruction):


    def __init__(self, *args, **kwargs):
        super(InputInstruction, self).__init__(*args, **kwargs)


    @property
    def get_value(self):
        if not self.value:
            p = self.input_params[0]
            self.value = self.params[p]
        return self.value


class NotInstruction(Instruction):


    def __init__(self, *args, **kwargs):
        super(NotInstruction, self).__init__(*args, **kwargs)


    @property
    def get_value(self):
        if not self.value:
            p = self.input_params[0]
            self.value = 65536 + (~ self.params[p])
        return self.value
        return self.value


class LShiftInstruction(Instruction):


    def __init__(self, *args, **kwargs):
        super(LShiftInstruction, self).__init__(*args, **kwargs)


    @property
    def get_value(self):
        if not self.value:
            p1 = self.input_params[0]
            p2 = self.input_params[1]
            self.value = self.params[p1] << self.params[p2]
        return self.value



class RShiftInstruction(Instruction):


    def __init__(self, *args, **kwargs):
        super(RShiftInstruction, self).__init__(*args, **kwargs)


    @property
    def get_value(self):
        if not self.value:
            p1 = self.input_params[0]
            p2 = self.input_params[1]
            self.value = self.params[p1] >> self.params[p2]
        return self.value

class AndInstruction(Instruction):


    def __init__(self, *args, **kwargs):
        super(AndInstruction, self).__init__(*args, **kwargs)


    @property
    def get_value(self):
        if not self.value:
            p1 = self.input_params[0]
            p2 = self.input_params[1]
            self.value = self.params[p1] & self.params[p2]
        return self.value


class OrInstruction(Instruction):


    def __init__(self, *args, **kwargs):
        super(OrInstruction, self).__init__(*args, **kwargs)


    @property
    def get_value(self):
        if not self.value:
            p1 = self.input_params[0]
            p2 = self.input_params[1]
            self.value = self.params[p1] | self.params[p2]
        return self.value


class Wire(object):


    def __init__(self, instruction):
        # Set some values
        self.name = instruction.target
        self.instruction = instruction
        # Calculate value from parents
        self.value = self.instruction.get_value


    def __hash__(self):
        return hash(self.name)


    def __eq__(self, other):
        return self.name == other


def main():
    # Get input
    input_file = 'input.txt'
    with open(input_file, 'r') as f:
        raw_ins = [l.rstrip() for l in f]
    instructions = [Instruction.process_instruction(l) for l in raw_ins]
    # Process instructions
    wires = set()
    while instructions:
        ins = instructions.pop(0)
        # Proces sinstruction if all all parents are computed;This if statement
        # evalues to True for empty parent lists
        if all(p in wires for p in ins.parents):
            # Add parent value missing from instruction
            for parent in [p for p in wires if p in ins.parents]:
                ins.add_value(parent)
            # Add new wire to the wires set
            wires.update([Wire(ins)])
        else:
            # If parents not computed, add back to list to check later
            instructions.append(ins)
    a = [w for w in wires if w == 'a'][0]
    print a.value


if __name__ == '__main__':
    main()

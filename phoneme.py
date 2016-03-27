# encoding: utf-8

import json

class Phoneme:
    def __init__(self, arg=None, ipa_map=None):
        # using a list instead of a set so it is easier for automatic
        # languages translators/transpilers
        self.features = []
        
        # initialize the phoneme
        self.set_phoneme(arg, ipa_map)
        
    def set_phoneme(self, arg=None, ipa_map=None):
        # phonemes can be initializated with iterateable objects (usually
        # lists, such as ['+voice', '+front']) or with strings, both as a
        # list of distinctive features (such as '+voice,+front') or as in
        # IPA representation (such as '/p/', the slashes being obbligatory).
        # Optional spaces when using features are removed; when using
        # IPA representation, 'ipa_map' must be specified.
        if type(arg) is list:
            # set each element in the list, stripping it
            for feature in arg:
                self.set_feature(feature.strip())
        elif isinstance(arg, str) or isinstance(arg, unicode): # for PY2
            # assume that it is an IPA representation if it starts with '/'
            if arg[0] == '/':
                # interrupt if no mapping was given
                if not ipa_map:
                    raise Exception("IPA mapping not informed for initialization.")
                
                # interrupt if phoneme representation not in the mapping
                if arg[1:-1] not in ipa_map:
                    raise Exception("Phoneme /%s/ not in the IPA mapping." % arg[1:-1])
                    
                # recusively call set_phoneme() with the features in the mapping
                self.set_phoneme(ipa_map[arg[1:-1]]['features'])
            else:
                # "tokenize" and clean string
                feature_list = arg.split(',')
                feature_list = [f.strip() for f in feature_list]
                for feature in feature_list:
                    self.set_feature(feature)
        else:
            raise Exception("Initialized with neither a list or a string.")

    # set a binary or articulatory feature, if possible
    def set_feature(self, feature_string):
        op, feature = feature_string[0], feature_string[1:]
            
        if op == '+':
            # adds feature, if possible
            if feature not in self.features:
                self.features.append(feature)
        elif op == '-':
            # removes feature, if possible
            if feature in self.features:
                self.features.remove(feature)
        elif op == '!':
            # inverts the feature
            if feature in self.features:
                self.features.remove(feature)
            else:
                self.features.append(feature)
        else:
            # invalid operator
            raise Exception("Invalid operator '%s' in '%s'." % (op, feature_string))
            
    def __repr__(self):
        return ','.join(['+'+f for f in self.features])

class PhonemeSequence:
    def __init__(self):
        self.sequence = []

    def append(self, element, ipa_map=None):
        # were we passed a Phoneme instance or we have to create one?
        print type(element)
        if isinstance(element, Phoneme):
            ph = element
        else:
            ph = Phoneme(element, ipa_map)

        self.sequence.append(ph)

    def __repr__(self):
        return '|'.join([repr(ph) for ph in self.sequence])

# load default IPA mapping
with file('ipa.json') as handler:
    IPA = json.load(handler)
        
p = Phoneme(['+voice'])
print repr(p) # should have voice
p.set_feature('+voice')
print repr(p) # should have voice
p.set_feature('+strid')
print repr(p) # should have voice and strid
p.set_feature('-voice')
print repr(p) # should have strid
p.set_feature('!voice')
print repr(p) # should have string and voice

p2 = Phoneme('+voice,+strid')
print "{" + repr(p2)
p3 = Phoneme('/p/', IPA)
print "[" + repr(p3)

#import pprint
#pprint.pprint(IPA)

ps = PhonemeSequence()
ps.append(p3)
ps.append('/a/', IPA)
print "<" + repr(ps)

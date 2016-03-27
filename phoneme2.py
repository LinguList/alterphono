# encoding: utf-8

import json

# check bilabial!!!

IPA = {
  u'ʁ' : { 'features' :    set(['voice', 'cons', 'cont', 'obstr']),
           'description' : 'voiced uvular fricative' },
  u'ɤ' : { 'features' :    set(['tense', 'cont', 'voice', 'syll']),
           'description' : 'close-mid back unrounded vowel' },
  u'ʃ' : { 'features' :    set(['cons', 'cont', 'cor', 'sibilant', 'distr', 'obstr']),
           'description' : 'voiceless palatoalveolar fricative' },
  u'ɪ' : { 'features' :    set(['high', 'cont', 'voice', 'syll', 'front']),
           'description' : 'near-close near-front unrounded vowel' },
  u'ʉ' : { 'features' :    set(['cont', 'syll', 'lab', 'high', 'tense', 'voice']),
           'description' : 'close central rounded vowel' },
  u'ʋ' : { 'features' :    set(['ant', 'voice', 'cons', 'cont']),
           'description' : 'labiodental approximant' },
  u'ʊ' : { 'features' :    set(['cont', 'syll', 'back', 'lab', 'high', 'voice']),
           'description' : 'near-close near-back rounded vowel' },
  u'ʍ' : { 'features' :    set(['high', 'cont', 'back']),
           'description' : 'voiceless labiovelar approximant' },
  u'ʌ' : { 'features' :    set(['cont', 'voice', 'syll']),
           'description' : 'open-mid back unrounded vowel' },
  u'ʏ' : { 'features' :    set(['cont', 'syll', 'lab', 'high', 'front', 'voice']),
           'description' : 'near-close near-front rounded vowel' },
  u'ʎ' : { 'features' :    set(['cons', 'cont', 'high', 'cor', 'distr', 'lat', 'voice']),
           'description' : 'palatal lateral approximant' },
  u'ɯ' : { 'features' :    set(['cont', 'syll', 'back', 'high', 'tense', 'voice']),
           'description' : 'close back unrounded vowel' },
  u'bʷ' : { 'features' :    set(['voice', 'cons', 'obstr', 'lab']),
           'description' : 'labialized voiced bilabial stop' },
  u'tʰ' : { 'features' :    set(['ant', 'spread', 'cons', 'obstr', 'cor']),
           'description' : 'aspirated voiceless alveolar stop' },
  u'ç' : { 'features' :    set(['cons', 'cont', 'high', 'cor', 'distr', 'obstr']),
           'description' : 'voiceless palatal fricative' },
  u'ɮ' : { 'features' :    set(['cons', 'cont', 'ant', 'cor', 'lat', 'voice', 'obstr']),
           'description' : 'voiced alveolar lateral fricative' },
  u'ʝ' : { 'features' :    set(['cons', 'cont', 'high', 'cor', 'distr', 'voice', 'obstr']),
           'description' : 'voiced palatal fricative' },
  u'u' : { 'features' :    set(['cont', 'syll', 'back', 'lab', 'high', 'tense', 'voice']),
           'description' : 'close back rounded vowel' },
  u'ʟ' : { 'features' :    set(['cons', 'cont', 'back', 'high', 'lat', 'voice']),
           'description' : 'velar lateral approximant' },
  u'ʣ' : { 'features' :    set(['cons', 'delrel', 'ant', 'cor', 'voice', 'obstr']),
           'description' : 'voiced alveolar affricate' },
  u'ʤ' : { 'features' :    set(['cons', 'delrel', 'cor', 'sibilant', 'distr', 'voice', 'obstr']),
           'description' : 'voiced palatoalveolar affricate' },
  u'ʧ' : { 'features' :    set(['cons', 'delrel', 'cor', 'sibilant', 'distr', 'obstr']),
           'description' : 'voiceless palatoalveolar affricate' },
  u'ð' : { 'features' :    set(['cons', 'cont', 'ant', 'cor', 'distr', 'voice', 'obstr']),
           'description' : 'voiced dental fricative' },
  u'ø' : { 'features' :    set(['cont', 'syll', 'lab', 'tense', 'front', 'voice']),
           'description' : 'close-mid front rounded vowel' },
  u'ɢ' : { 'features' :    set(['voice', 'cons', 'obstr']),
           'description' : 'voiced uvular stop' },
  u'ɾ' : { 'features' :    set(['cons', 'cont', 'ant', 'cor', 'voice', 'vibr']),
           'description' : 'alveolar flap' },
  u'kʲ' : { 'features' :    set(['high', 'obstr', 'cons', 'back', 'cor']),
           'description' : 'palatalized voiceless velar stop' },
  u'kʰ' : { 'features' :    set(['high', 'spread', 'cons', 'back', 'obstr']),
           'description' : 'aspirated voiceless velar stop' },
  u'kʷ' : { 'features' :    set(['high', 'cons', 'back', 'lab', 'obstr']),
           'description' : 'labialized voiceless velar stop' },
  u'θ' : { 'features' :    set(['cons', 'cont', 'ant', 'cor', 'distr', 'obstr']),
           'description' : 'voiceless dental fricative' },
  u'æ' : { 'features' :    set(['cont', 'syll', 'tense', 'low', 'front', 'voice']),
           'description' : 'near-open front unrounded vowel' },
  u'gʷ' : { 'features' :    set(['cons', 'back', 'lab', 'high', 'voice', 'obstr']),
           'description' : 'labialized voiced velar stop' },
  u'y' : { 'features' :    set(['cont', 'syll', 'lab', 'high', 'tense', 'front', 'voice']),
           'description' : 'close front rounded vowel' },
  u'gʲ' : { 'features' :    set(['cons', 'back', 'high', 'cor', 'voice', 'obstr']),
           'description' : 'palatalized voiced velar stop' },
  u'χ' : { 'features' :    set(['cons', 'cont', 'obstr']),
           'description' : 'voiceless uvular fricative' },
  u'ɨ' : { 'features' :    set(['high', 'cont', 'voice', 'syll', 'tense']),
           'description' : 'close central unrounded vowel' },
  u'ŋ' : { 'features' :    set(['high', 'voice', 'cons', 'nasal', 'back']),
           'description' : 'velar nasal' },
  u'ɲ' : { 'features' :    set(['cons', 'nasal', 'high', 'cor', 'distr', 'voice']),
           'description' : 'palatal nasal' },
  u'β' : { 'features' :    set(['voice', 'cons', 'cont', 'obstr', 'lab']),
           'description' : 'voiced bilabial fricative' },
  u'ɣ' : { 'features' :    set(['cons', 'cont', 'back', 'high', 'voice', 'obstr']),
           'description' : 'voiced velar fricative' },
  u'ɬ' : { 'features' :    set(['cons', 'cont', 'ant', 'cor', 'lat', 'obstr']),
           'description' : 'voiceless alveolar lateral fricative' },
  u'ɑ' : { 'features' :    set(['cont', 'voice', 'syll', 'low', 'back']),
           'description' : 'open back unrounded vowel' },
  u'ɐ' : { 'features' :    set(['tense', 'cont', 'voice', 'syll', 'low']),
           'description' : 'near-open central unrounded vowel' },
  u'œ' : { 'features' :    set(['front', 'cont', 'voice', 'syll', 'lab']),
           'description' : 'open-mid front rounded vowel' },
  u'ɒ' : { 'features' :    set(['cont', 'syll', 'back', 'lab', 'low', 'voice']),
           'description' : 'open back rounded vowel' },
  u'ɔ' : { 'features' :    set(['cont', 'voice', 'syll', 'lab']),
           'description' : 'open-mid back rounded vowel' },
  u'ʦ' : { 'features' :    set(['ant', 'delrel', 'cons', 'obstr', 'cor']),
           'description' : 'voicelss alveolar affricate' },
  u'ɸ' : { 'features' :    set(['cons', 'cont', 'obstr', 'lab']),
           'description' : 'voiceless bilabial fricative' },
  u'e' : { 'features' :    set(['front', 'cont', 'voice', 'syll', 'tense']),
           'description' : 'close-mid front unrounded vowel' },
  u'ɛ' : { 'features' :    set(['front', 'cont', 'voice', 'syll']),
           'description' : 'open-mid front unrounded vowel' },
  u'r' : { 'features' :    set(['cons', 'cont', 'long', 'ant', 'cor', 'voice', 'vibr']),
           'description' : 'alveolar trill' },
  u'ɟ' : { 'features' :    set(['cons', 'high', 'cor', 'distr', 'voice', 'obstr']),
           'description' : 'voiced palatal stop' },
  u'pʷ' : { 'features' :    set(['cons', 'obstr', 'lab']),
           'description' : 'labialized voiceless bilabial stop' },
  u'a' : { 'features' :    set(['cont', 'voice', 'syll', 'low']),
           'description' : 'open front unrounded vowel' },
  u'pʰ' : { 'features' :    set(['spread', 'cons', 'obstr', 'lab']),
           'description' : 'aspirated voiceless bilabial stop' },
  u'b' : { 'features' :    set(['voice', 'cons', 'obstr', 'lab']),
           'description' : 'voiced bilabial stop' },
  u'ɥ' : { 'features' :    set(['high', 'voice', 'cont', 'lab', 'cor']),
           'description' : 'labialized palatal approximant' },
  u'd' : { 'features' :    set(['ant', 'voice', 'cons', 'obstr', 'cor']),
           'description' : 'voiced alveolar stop' },
  u'g' : { 'features' :    set(['voice', 'cons', 'back', 'obstr']),
           'description' : 'voiced velar stop' },
  u'ɦ' : { 'features' :    set(['voice', 'cons', 'cont', 'obstr']),
           'description' : 'voiced glottal fricative' },
  u'i' : { 'features' :    set(['cont', 'syll', 'high', 'tense', 'front', 'voice']),
           'description' : 'close front unrounded vowel' },
  u'h' : { 'features' :    set(['cons', 'cont', 'obstr']),
           'description' : 'voiceless glottal fricative' },
  u'k' : { 'features' :    set(['voice', 'cons', 'back', 'obstr']),
           'description' : 'voiceless velar stop' },
  u'j' : { 'features' :    set(['high', 'voice', 'cont', 'cor']),
           'description' : 'palatal approximant' },
  u'm' : { 'features' :    set(['voice', 'cons', 'nasal', 'lab']),
           'description' : 'bilabial nasal' },
  u'l' : { 'features' :    set(['cons', 'cont', 'ant', 'cor', 'lat', 'voice']),
           'description' : 'alveolar lateral approximant' },
  u'o' : { 'features' :    set(['tense', 'cont', 'voice', 'syll', 'lab']),
           'description' : 'close-mid back rounded vowel' },
  u'n' : { 'features' :    set(['ant', 'voice', 'cons', 'nasal', 'cor']),
           'description' : 'alveolar nasal' },
  u'ɱ' : { 'features' :    set(['ant', 'voice', 'cons', 'nasal']),
           'description' : 'labiodental nasal' },
  u'p' : { 'features' :    set(['cons', 'obstr', 'lab']),
           'description' : 'voiceless bilabial stop' },
  u's' : { 'features' :    set(['cons', 'cont', 'ant', 'cor', 'sibilant', 'obstr']),
           'description' : 'voiceless alveolar fricative' },
  u'ʒ' : { 'features' :    set(['cons', 'cont', 'cor', 'sibilant', 'distr', 'voice', 'obstr']),
           'description' : 'voiced palatoalveolar fricative' },
  u'ɵ' : { 'features' :    set(['cont', 'voice', 'syll', 'lab']),
           'description' : 'close-mid central rounded vowel' },
  u't' : { 'features' :    set(['ant', 'cons', 'obstr', 'cor']),
           'description' : 'voiceless alveolar stop' },
  u'w' : { 'features' :    set(['high', 'voice', 'cont', 'back']),
           'description' : 'labiovelar approximant' },
  u'v' : { 'features' :    set(['ant', 'voice', 'cons', 'cont', 'obstr']),
           'description' : 'voiced labiodental fricative' },
  u'ɹ' : { 'features' :    set(['ant', 'voice', 'cons', 'cont', 'cor']),
           'description' : 'alveolar approximant' },
  u'x' : { 'features' :    set(['high', 'cons', 'cont', 'back', 'obstr']),
           'description' : 'voiceless velar fricative' },
  u'z' : { 'features' :    set(['cons', 'cont', 'ant', 'cor', 'sibilant', 'voice', 'obstr']),
           'description' : 'voiced alveolar fricative' },
  u'ɶ' : { 'features' :    set(['cont', 'syll', 'lab', 'low', 'front', 'voice']),
           'description' : 'open front rounded vowel' },
  u'f' : { 'features' :    set(['ant', 'cons', 'cont', 'obstr']),
           'description' : 'voiceless labiodental fricative' },
  u'ʔ' : { 'features' :    set(['cons', 'obstr', 'constr']),
           'description' : 'glottal stop' },
}


def load_IPA(filename):
    with file(filename) as handler:
        IPA = json.load(handler)

    for entry in IPA:
        IPA[entry]['features'] = feats2phoneme(IPA[entry]['features'])

    return IPA

def ipa2phoneme(ipa):
    return IPA[ipa]['features']

def phoneme2ipa(phoneme, slash=True):
    for entry in IPA:
        print entry, IPA[entry]['features'], phoneme
        if IPA[entry]['features'] == phoneme:
            if slash:
                return '/' + entry + "/"
            else:
                return entry

    return "!!!"

def ipa2sequence(ipa):
    seq = {'phonemes': [], 'syllables': []}

    # assume each char is an IPA
    for char in ipa:
        seq['phonemes'].append(ipa2phoneme(char))

    return seq

def sequence2ipa(seq):
    buf = ''.join([phoneme2ipa(p, False) for p in seq['phonemes']])
    return '/' + buf + '/'

def get_description(phoneme):
    for entry in IPA:
        if IPA[entry]['features'] == phoneme:
            return IPA[entry]['description']

    return "!!!"


def feats2phoneme(features):
    features = features.replace(' ', '')
    features = features.split(',')
    features = [feat[1:] for feat in features]

    return set(features)

def set_feature(feature_string, phoneme):
    op, feature = feature_string[0], feature_string[1:]
            
    if op == '+':
        # adds feature, if possible
        phoneme.add(feature)
    elif op == '-':
        # removes feature, if possible
        phoneme.discard(feature)
    elif op == '!':
        # inverts the feature
        if feature in phoneme:
            phoneme.discard(feature)
        else:
            phoneme.add(feature)
    else:
        # invalid operator
        raise Exception("Invalid operator '%s' in '%s'." %
            (op, feature_string))

    return phoneme

####

# load default IPA mapping
#IPA = load_IPA('ipa.json')

ph1 = ipa2phoneme('a')
ph2 = feats2phoneme('+cont, +voice, +cor, +high')
print ph1, phoneme2ipa(ph1)
print get_description(ph1)
print ph2, phoneme2ipa(ph2)
print get_description(ph2)


ph2 = set_feature('+distr', ph2)
print ph2, phoneme2ipa(ph2)
print get_description(ph2)
ph2 = set_feature('-distr', ph2)
print ph2, phoneme2ipa(ph2)
print get_description(ph2)
ph2 = set_feature('!cor', ph2)
print ph2, phoneme2ipa(ph2)
print get_description(ph2)
ph2 = set_feature('!cor', ph2)
print ph2, phoneme2ipa(ph2)
print get_description(ph2)

s = ipa2sequence("pata")
print s
print sequence2ipa(s)

#print 'IPA = {'
#for entry in IPA:
#    f = str(IPA[entry]['features'])
#    f = f.replace("u'", "'")

#    print "  u'%s' : { 'features' :    %s,\n           'description' : '%s' }," % (entry, f, IPA[entry]['description'])
#print '}'

print [s]
for entry in IPA:
    if IPA[entry]['features'] == s['phonemes'][0]:
        print ">>", entry

# encoding: utf-8

import csv

FEATURES = ['advancedTongueRoot', 'anterior', 'approximant', 'back', 'click',
    'consonantal', 'constrictedGlottis', 'continuant', 'coronal', 'delayedRelease',
    'distributed', 'dorsal', 'epilaryngealSource', 'fortis', 'front', 'high',
    'labial', 'labiodental', 'lateral', 'long', 'low', 'loweredLarynxImplosive',
    'nasal', 'periodicGlottalSource', 'raisedLarynxEjective', 'retractedTongueRoot',
    'round', 'short', 'sonorant', 'spreadGlottis', 'stress', 'strident', 'syllabic',
    'tap', 'tense', 'tone', 'trill']

VALUE_MAP = { '-': 0.04,
              '+': 0.96,
              '0': 0.50, }
    
# From http://stackoverflow.com/questions/5004687/
# python-csv-dictreader-with-utf-8-data
def unicode_csv_reader(utf8_data, **kwargs):
    """
    An UTF-8 wrapper around Python's csv.DictReader.
    """

    csv_reader = csv.DictReader(utf8_data, **kwargs)
    for row in csv_reader:
        yield {unicode(key, 'utf-8'): unicode(value, 'utf-8') for key, value in row.iteritems()}
        
def read_mielke():
    data = {}

    # read phoible segments
    filename = 'input/dist.ipa-mielke-acoustic.csv'

    with file(filename) as handler:
        reader = unicode_csv_reader(handler, delimiter=',')
        for row in reader:
            ipa = row.pop('unicode-ipa')
            data[ipa] = row

    return data

def read_phonemes():
    data = {}

    # read phoible segments
    filename = 'output/phonemes.csv'

    with file(filename) as handler:
        reader = unicode_csv_reader(handler, delimiter=',')
        for row in reader:
            phoneme = row.pop('Phoneme')
            
            # manual fix, adjusting phoible to mielke
            if phoneme == u't̠ʃ':
                phoneme = u'tʃ'
            elif phoneme == u'd̠ʒ':
                phoneme = u'dʒ'
                
            data[phoneme] = row

    return data
    
def run():
    mielke = read_mielke()
    phonemes = read_phonemes()
    
    handler = file('output/distance_scores.csv', 'w')
    handler.write('ph1_ph2,')
    for feature in FEATURES:
        handler.write('%s_++,' % feature)
        handler.write('%s_--,' % feature)
        handler.write('%s_+-,' % feature)
    handler.write('distance\n')
    
    # using range(len()) to guarantee that no permutations are written
    sorted_mielke = sorted(mielke)
    for phoneme1_idx in range(len(sorted_mielke)):
        phoneme1 = sorted_mielke[phoneme1_idx]
        for phoneme2_idx in range(phoneme1_idx, len(sorted_mielke)):
            phoneme2 = sorted_mielke[phoneme2_idx]
            dist = float(mielke[phoneme1][phoneme2])

            values = []
            for feature in FEATURES:
                feat1 = phonemes[phoneme1][feature]
                feat2 = phonemes[phoneme2][feature]
                if feat1 == '0':
                    feat1 = '-'
                if feat2 == '0':
                    feat2 = '-'
                    
                if feat1 == feat2 == '+':
                    # + / +
                    values.append('T,F,F')
                elif feat1 == feat2 == '-':
                    # - / -
                    values.append('F,T,F')
                else:
                    # + / -
                    values.append('F,F,T')
            
            # build value strings
            buf = '%s_%s,%s,%.6f\n' % (phoneme1,
                phoneme2,
                ','.join(values),
                dist)
            handler.write(buf.encode('utf-8'))

    handler.close()
        
if __name__ == '__main__':
    run()
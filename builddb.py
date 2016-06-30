# encoding: utf-8

"""
Module for aggregating Phoible data into the datasets needed for the
research.
"""

import csv
import operator

# From http://stackoverflow.com/questions/5004687/
# python-csv-dictreader-with-utf-8-data
def unicode_csv_reader(utf8_data, **kwargs):
    """
    An UTF-8 wrapper around Python's csv.DictReader.
    """

    csv_reader = csv.DictReader(utf8_data, **kwargs)
    for row in csv_reader:
        yield {key: unicode(value, 'utf-8') for key, value in row.iteritems()}

def read_ipa_names():
    """
    Read the list of IPA names.

    Returns a dictionary with IPA glyphs as keys and strings as values.
    """

    # TODO: add to documentation
    #   nasal are written as nasal stop
    #   implosives and ejectives are stops
    #   ejectives are marked as voiceless
    #   ɡ for voiced velar stop
    #   sibilant / non-sibilant
    #   epiglottal is marked as pharyngeal
    #   some are not in PHOIBLE

    data = {}

    # read phoible segments
    filename = 'input/ipa.csv'

    with file(filename) as handler:
        reader = unicode_csv_reader(handler, delimiter=',')
        for row in reader:
            data[row['glyph']] = row['description']

    return data

def read_langinfo():

    data = {}

    # for each line in the soruce
    with file('input/phoible-aggregated.tsv') as handler:
        reader = unicode_csv_reader(handler, delimiter='\t')
        for row in reader:
            inventory_id = int(row.pop('InventoryID'))
            data[inventory_id] = row
    
    return data
    
def run():
    """
    Reads the 'phoible-by-phoneme' database line by line, parsing and aggregating data.
    """

    # variables for collecting the data that is structured into an output
    # at the end
    lang_data = read_langinfo()
    inv_data = []
    phon_data = {}
    allophone_data = {}
    cooccurence_data = {}
    
    # auxiliary variables
    phon_count = {}
    
    # external source for phoneme description
    ipa_names = read_ipa_names()

    # for each line in the soruce
    with file('input/phoible-by-phoneme.tsv') as handler:
        reader = unicode_csv_reader(handler, delimiter='\t')
        for row in reader:
            # extract fields which are not binary features; 'row'
            # will end only with them
            allophones = row.pop('Allophones')
            glyph_id = row.pop('GlyphID')
            inventory_id = int(row.pop('InventoryID'))
            language_code = row.pop('LanguageCode')
            language_name = row.pop('LanguageName')
            source = row.pop('Source')
            specific_dialect = row.pop('SpecificDialect')       
            phoneme = row.pop('Phoneme')
            
            # append new language entry if needed; the '_phonemes' field
            # is internal, intended to later compute the phoneme by phoneme
            # matrix; not the best check...
            if '_phonemes' not in lang_data[inventory_id]:
                if specific_dialect == 'NA':
                    lang_data[inventory_id]['SpecificDialect'] = ''
                else:
                    lang_data[inventory_id]['SpecificDialect'] = specific_dialect
                lang_data[inventory_id]['_phonemes'] = []
                    
            # append inventory data
            inv_data.append( {
                'InventoryID' : inventory_id,
                'GlyphID' : glyph_id,
                'Phoneme' : phoneme,
                'Allophones' : allophones,
            })
            
            # add phoneme data, if any
            if glyph_id not in phon_data:
                if phoneme in ipa_names:
                    desc = ipa_names[phoneme]
                else:
                    desc = 'NA'
            
                phon_data[glyph_id] = {
                    'Phoneme' : phoneme,
                    'Description' : desc,
                    'Features' : row }
            
            # add the phoneme to the current inventory, to later
            # compute the phoneme by phoneme matrix
            lang_data[inventory_id]['_phonemes'].append(phoneme)
                    
            # allophone counts
            if allophones != 'NA':
                # if phoneme not in inventory, add it
                if glyph_id not in allophone_data:
                    allophone_data[glyph_id] = {}
                    
                # add counts
                for ap in allophones.split():
                    if ap not in allophone_data[glyph_id]:
                        allophone_data[glyph_id][ap] = 1
                    else:
                        allophone_data[glyph_id][ap] += 1

            # update phoneme counts
            if glyph_id not in phon_count:
                phon_count[glyph_id] = 1
            else:
                phon_count[glyph_id] += 1

    # once finished reading the entire file, add phoneme counts
    for glyph_id in phon_count:
        phon_data[glyph_id]['Count'] = phon_count[glyph_id]

    # compute the phoneme co-occurance matrix (phoneme by phoneme)
    for inventory_id in lang_data:
        for phoneme1 in lang_data[inventory_id]['_phonemes']:
            # add to rows if needed
            if phoneme1 not in cooccurence_data:
                cooccurence_data[phoneme1] = {}
                
            # add columns; the diagonals will hold the global count
            for phoneme2 in lang_data[inventory_id]['_phonemes']:
                # add to columns if needed
                if phoneme2 not in cooccurence_data[phoneme1]:
                    cooccurence_data[phoneme1][phoneme2] = 1
                else:
                    cooccurence_data[phoneme1][phoneme2] += 1
    
    # ## OUTPUTS ############################################

    # lang data
    handler = file('output/languages.csv', 'w')
    header = ['InventoryID', 'LanguageCode', 'LanguageName', 'Glottocode',
        'GlottologName', 'LanguageFamilyRoot', 'LanguageFamilyGenus', 'SpecificDialect',
        'Area', 'Country', 'Latitude', 'Longitude', 'Population', 'Phonemes',
        'Consonants', 'Vowels', 'Tones', 'Trump', 'Source', '_phonemelist', 'Notes']
    handler.write(','.join(header) + '\n')
    
    for inventory_id in sorted(lang_data):
        notes_str = ''
    
        # extract population
        population_str = lang_data[inventory_id]['Population']
        if population_str in ["No_known_speakers", "Extinct",
            "Ancient", "No_estimate_available", "Missing E16 page"]:
            notes_str += 'Population: %s' % population_str.replace('_', ' ')
            population_str = ''
        else:
            population_str = str(int(population_str.replace(',', '')))

        # build phoneme string
        phoneme_str = u'|'.join(sorted(lang_data[inventory_id]['_phonemes']))
        
        # clean versions
        latitude = lang_data[inventory_id]['Latitude']
        if latitude == 'NULL':
            latitude = ''
            
        longitude = lang_data[inventory_id]['Longitude']
        if longitude == 'NULL':
            longitude = ''
        
        buf = u','.join([
            str(inventory_id),
            lang_data[inventory_id]['LanguageCode'],
            '"%s"' % lang_data[inventory_id]['LanguageName'],
            lang_data[inventory_id]['Glottocode'],
            '"%s"' % lang_data[inventory_id]['GlottologName'],
            '"%s"' % lang_data[inventory_id]['LanguageFamilyRoot'],
            '"%s"' % lang_data[inventory_id]['LanguageFamilyGenus'],
            '"%s"' % lang_data[inventory_id]['SpecificDialect'],
            '"%s"' % lang_data[inventory_id]['Area'],
            '"%s"' % lang_data[inventory_id]['Country'],
            latitude,
            longitude,
            population_str,
            lang_data[inventory_id]['Phonemes'],
            lang_data[inventory_id]['Consonants'],
            lang_data[inventory_id]['Vowels'],
            lang_data[inventory_id]['Tones'],
            lang_data[inventory_id]['Trump'],
            lang_data[inventory_id]['Source'],
            phoneme_str,
            notes_str])
    
        handler.write(buf.encode('utf-8') + '\n')
        
    # inv data - output in order (somewhat)
    handler = file('output/inventories.csv', 'w')
    header = ['InventoryID', 'Glottocode', 'GlyphID', 'Phoneme', 'Allophones']
    handler.write(','.join(header) + '\n')
    
    for inventory_id in lang_data:
        collect = []
    
        for entry in inv_data:
            if entry['InventoryID'] == inventory_id:
                if entry['Allophones'] == 'NA':
                    allophones = []
                else:
                    allophones = entry['Allophones'].split()
            
                collect.append([
                    entry['GlyphID'],
                    entry['Phoneme'],
                    allophones
                    ])
                    
        # sort by phoneme and output
        collect.sort(key=lambda x: x[1])
        for entry in collect:
            buf = '%i,%s,%s,%s,%s' % (
                inventory_id,
                lang_data[inventory_id]['Glottocode'],
                entry[0],
                entry[1],
                '|'.join(entry[2]) )
            handler.write(buf.encode('utf-8') + '\n')
            
    handler.close()

    # phoneme data
    features = sorted(phon_data['2C71']['Features'].keys())
    
    handler = file('output/phonemes.csv', 'w')
    header = ['GlyphID', 'Phoneme', 'Count', 'Description', ','.join(features)]
    handler.write(','.join(header) + '\n')
    
    for glyph_id in sorted(phon_data):
        if phon_data[glyph_id]['Description'] in ['NA', '#NAME ERROR#']:
            description = ''
        else:
            description = phon_data[glyph_id]['Description']
            
        feat_str = [str(phon_data[glyph_id]['Features'][f]) for f in features]
        feat_str = [f.replace(',', '|') for f in feat_str]
        feat_str = [f.replace('NA', '') for f in feat_str]
        
        buf = '%s,%s,%i,%s,%s' % (
            glyph_id,
            phon_data[glyph_id]['Phoneme'],
            phon_data[glyph_id]['Count'],
            description,
            ','.join(feat_str)
        )
        handler.write(buf.encode('utf-8')+'\n')
        
    handler.close()

    # allophone data
    handler = file('output/allophones.csv', 'w')
    header = ['GlyphID', 'Allophone', 'Count', 'Frequency']
    handler.write(','.join(header) + '\n')
    
    for glyph_id in sorted(allophone_data):
        # ordered list
        sorted_ad = sorted(allophone_data[glyph_id].items(),
            key=operator.itemgetter(1),
            reverse=True)
            
        # total count (for percentage below)
        counts = float(sum([v[1] for v in allophone_data[glyph_id].items()]))
            
        # output allophone
        for entry in sorted_ad:
            buf = '%s,%s,%i,%.4f' % (glyph_id, entry[0], entry[1], entry[1]/counts)
            handler.write(buf.encode('utf-8') + '\n')
            
    handler.close()
    
    # cooccurence
    phonemes = sorted(cooccurence_data)
    
    handler = file('output/cooccurrence.csv', 'w')
    header = ['Phoneme', ','.join(phonemes)]
    handler.write(','.join(header).encode('utf-8') + '\n')
    
    for phoneme1 in phonemes:
        counts = []
        for phoneme2 in phonemes:
            if phoneme2 not in cooccurence_data[phoneme1]:
                counts.append(0)
            else:
                counts.append(cooccurence_data[phoneme1][phoneme2])
                
        buf = '%s,%s' % (phoneme1, ','.join([str(c) for c in counts]))
        handler.write(buf.encode('utf-8') + '\n')
    
    handler.close()
        
if __name__ == '__main__':
    run()

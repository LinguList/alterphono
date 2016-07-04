# encoding: utf-8

import csv

TYPOLOGY = 'input/typology.csv'
DATASET1 = 'input/pnas.1424033112.sd01.txt'
DATASET2 = 'input/pnas.1424033112.sd02.txt'
CREANZA_LANG = 'output/creanza.lang.csv'
CREANZA_PHON = 'output/creanza.phon.csv'

# reads Ruhlen's typology, for complementing Creanza's data
def read_typology():
	typology = []

	# read phoible data
	with file(TYPOLOGY) as handler:
		reader = csv.DictReader(handler, delimiter=',')
		for row in reader:
			row['Language'] = row['Language'].decode('utf-8')

			# there are some errors in the data file, where the
			# cedilla is expressed by the visually similar
			# 'CYRILLIC SMALL LETTER ES WITH DESCENDER' (U+04AB)
			row['Language'] = row['Language'].replace(u'\u04ab', u'ç')

			# remove erroneus line feed
			row['Language'] = row['Language'].replace(u'\u000a', u'')

			typology.append(row)

	return typology

# fixes the language name as written in dataset1 to a unicode
# version according to the Ruhlen dataset
def fix_lang_name(text):
	text = text.replace('u^',                  u'û') # Qxu^
	text = text.replace('//',                  u'ǁ') # G//abake
	text = text.replace('\\u450?',             u'ǂ') # \u450?Hû
	text = text.replace('\\sub 1\\nosupersub', u'1')
	text = text.replace('\\sub 2\\nosupersub', u'2')
	text = text.replace('\\sub 3\\nosupersub', u'3')
	text = text.replace('a~',                  u'ã') # Doya~yo
	text = text.replace('\\u-3609?',           u'ç') # Franco-Provençal
	text = text.replace('u~',                  u'ũ') # Brũ
	text = text.replace('o\\u-3322?',          u'ŏ') # Paco\u-3322?h
	text = text.replace('e^',                  u'ê') # Hre^
	text = text.replace('\\u-3588?',           u'ü') # Kh\u-3588?n
	text = text.replace('O\\u-3320?',          u'Ö') # O\u-3320?mie
	text = text.replace('\u-3594?',            u'ö') # Ag\u-3594?b
	text = text.replace('n~',                  u'ñ') # Dieguen~o

	# full name substituion
	if text == 'Gaanda':
		text = u"Ga'anda"
	if text == 'Paa':
		text = u"Pa'a"
	if text == 'Maa':
		text = u"Ma'a"
	if text == 'Plains Gta':
		text = u"Plains Gta'"
	if text == 'Puman2':
		text = u"P'uman2"
	if text == 'Khmu':
		text = u"Khmu'"
	if text == 'Che Wong':
		text = u"Che' Wong"
	if text == 'Kenta Bong':
		text = u"Kenta' Bong"
	if text == 'Sadan':
		text = u"Sa'dan"
	if text == 'Saban':
		text = u"Sa'ban"
	if text == 'Maanyan':
		text = u"Ma'anyan"
	if text == 'Urak Lawoi':
		text = u"Urak Lawoi'"
	if text == 'Toabaita':
		text = u"To'abaita"
	if text == 'Kwaraae':
		text = u"Kwara'ae"
	if text == 'Saa':
		text = u"Sa'a"
	if text == 'Paumotu':
		text = u"Pa'umotu"
	if text == 'Wik-Meanha':
		text = u"Wik-Me'anha"
	if text == 'Coeur dAlene':
		text = u"Coeur d'Alene"
	if text == 'Eseejja':
		text = u"Ese'ejja"

	return text

# reads the first dataset, which contains the list of languages, language
# typology information and the list of phonemes in the language
def read_dataset1():
	# as there are comments, we can't easily use the 'csv' library, so
	# we need to do it "the old way", very explicitly to make it clear
	dataset1 = []
	with file(DATASET1) as handler:
		for num_line, line in enumerate(handler):
			if num_line <= 19:
				# comments and header, just skip
				continue

			# parse actual contents 'manually'
			line = line[:-1].decode('utf-8') # [:-1] for '\n'
			fields = line.split('\t')

			data = {
				'record' : fields[0],
				'lang_name' : fix_lang_name(fields[1]),
				'iso' : fields[2],
				'iso_a3' : fields[3],
				'el' : fields[4],
				'pop' : fields[5],
				'region' : fields[6],
				'lat' : fields[7],
				'lon' : fields[8],
				'phonemes' : fields[9:]
			}

			dataset1.append(data)

	return dataset1

# reads the second dataset, which contains the list of phonemes that will
# be used as column names
def read_dataset2():
	# as there are comments, we can't easily use the 'csv' library, so
	# we need to do it "the old way", very explicitly to make it clear
	dataset2 = []
	with file(DATASET2) as handler:
		for num_line, line in enumerate(handler):
			if num_line <= 15:
				# comments and header, just skip
				continue

			# actual contents
			line = line[:-1].decode('utf-8') # [:-1] for '\n'
			fields = line.split('\t')

			# don't use the index
			fields = fields[1:]

			# append to the results, thus keeping the order
			# for later using the phonemes as column names
			dataset2.append(fields)

	return dataset2

def output_lang(typology, dataset1, dataset2):
	handler = file(CREANZA_LANG, 'w')

	# collect the phonemes in the right order for the column names
	phonemes = [p[0] for p in dataset2]

	header = [
		u'language',
		u'ruhlen',
		u'iso',
		u'iso_a3',
		u'family',
		u'population',
		u'region',
		u'location',
		u'latitude',
		u'longitude',
		u','.join(phonemes),
	]

	buf = u','.join(header)
	handler.write(buf.encode('utf-8'))
	handler.write('\n')

	# for each entry in the first dataset
	for d1 in dataset1:
		ruhlen = int(d1['record'])

		# deal with encoding problems -- the source file actually has
		# different encodings in each cell...
		location = typology[ruhlen-1]['Location'].decode('latin-1')
		classifi = typology[ruhlen-1]['Classification'].decode('latin-1')

		if classifi.endswith('batulabal'):
			classifi = u'Amerind: Central: Uto-Aztecan: Tübatulabal'

		# correct errors
		classifi = classifi.replace('cKhoisan:', 'Khoisan:')

		fields = [
			u'"%s"' % d1['lang_name'],
			str(ruhlen),
			u'"%s"' % d1['iso'],
			u'"%s"' % d1['iso_a3'],
			u'"%s"' % classifi,
			d1['pop'],
			u'"%s"' % d1['region'],
			u'"%s"' % location,
			d1['lat'],
			d1['lon'],
			u','.join(d1['phonemes']),
		]

		buf = u','.join(fields)
		handler.write(buf.encode('utf-8'))
		handler.write('\n')

	handler.close()

def output_phon(dataset2):
	handler = file(CREANZA_PHON, 'w')

	header = 'ipa,occurences,consonant,vowel,mod_consonant,mod_vowel,click'
	handler.write(header)
	handler.write('\n')

	for phoneme in dataset2:
		row = ','.join(phoneme)
		handler.write(row.encode('utf-8'))
		handler.write('\n')

	handler.close()

if __name__ == '__main__':
	typology = read_typology()
	dataset1 = read_dataset1()
	dataset2 = read_dataset2()

	output_lang(typology, dataset1, dataset2)
	output_phon(dataset2)


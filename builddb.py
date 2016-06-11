# encoding: utf-8

import csv

# set source files
PHOIBLE_SEGS = 'input/phoible-segments-features.tsv'
FONETIKODE_SEGS = 'input/phoible_Features_Fonetikode.csv'

# FK_STR maps between feature codes, as defined in this system,
# and a textual description; textual descriptions are single,
# exclusive words, with optional dashes in them; some entries
# are included even though there is no entry using them in the
# Fonetikode database of Dediu & Moisik (2015)
FK_STR = {
	# Default (empty feature)
	''     : '',
	# General Class - gc
	'cons' : 'consonant',
	'vowl' : 'vowel',
	'sseg' : 'suprasegmental',
	# Vowel Vertical - V-V.
	'clos' : 'close',
	'ncls' : 'nearclose',
	'cmid' : 'closemid',
	'vmid' : 'mid',
	'omid' : 'openmid',
	'nopn' : 'nearopen',
	'open' : 'open',
	# Vowel Horizontal - V-H.
	'frnt' : 'front',
	'nfrt' : 'nearfront',
	'cntr' : 'central',
	'nbck' : 'nearback',
	'back' : 'back',
	# Vowel Modifiers - V-C.
	'vnsl' : 'nasal-vowel',
	'roun' : 'round',
	'urrd' : 'unrounded-rounded',
	'rdur' : 'rounded-unrounded',
	'unns' : 'unnasal-nasal',
	'nsun' : 'nasal-unnasal',
	# Consonantal Place of Articulation - C-P.
	'blab' : 'bilabial',
	'blbd' : 'bilabio-labiodental',
	'balv' : 'bilabio-alveolar',
	'bpav' : 'bilabio-postalveolar',
	'lbdt' : 'labiodental',
	'lvlr' : 'labiovelar',
	'luvl' : 'labiouvular',
	'lglb' : 'linguolabial', # no entries in database
	'idnt' : 'interdental',
	'dntl' : 'dental',
	'alvr' : 'alveolar',
	'palv' : 'postalveolar',
	'rtfx' : 'retroflex',
	'dtvl' : 'dentivelar',
	'avvl' : 'alveolovelar',
	'avpl' : 'alveolopalatal',
	'palt' : 'palatal',
	'pavv' : 'postalveolar-velar',
	'velr' : 'velar',
	'uvlr' : 'uvular',
	'phry' : 'pharyngeal',
	'gltl' : 'glottal',
	# Consonantal Manner of Articulation - C-M.
	'stop' : 'stop',
	'frct' : 'fricative',
	'affr' : 'affricate',
	'nasl' : 'nasal',
	'appr' : 'approximant',
	'flap' : 'flap',
	'tril' : 'trill',
	'clck' : 'click',
	# Consonantal Sequencer - C-S.
	'smpx' : 'simplex',
	'cmpx' : 'complex',
	'pnsz' : 'pre-nasalized',
	'tnsz' : 'post-nasalized',
	'pglz' : 'pre-glottalized',
	'tglz' : 'post-glottalized',
	'pasp' : 'pre-aspirated',
	'tasp' : 'post-aspirated',
	# Phonation - Phon.
	'voil' : 'voiceless',
	'void' : 'voiced',
	'brth' : 'breathy',
	'crky' : 'creaky',
	# Initiation - Init.
	'plme' : 'pulmonic-egressive',
	'glti' : 'glottal-ingressive',
	'glte' : 'glottal-egressive',
	'veli' : 'velaric-ingressive',
	# Primary Articulation Diacritics - Pri.
	'retr' : 'retracted',
	'advc' : 'advanced',
	'mctr' : 'mid-centralized',
	'lwrd' : 'lowered',
	'razd' : 'raised',
	'apcl' : 'apical',
	'lmnl' : 'laminal',
	'frts' : 'fortis',
	'lens' : 'lenis',
	'ctrz' : 'centralized',
	'nasz' : 'nasalized',
	# Secondary Articulation Diacritics - 2nd
	'lblz' : 'labialized',
	'pltz' : 'palatalized',
	'vlrz' : 'velarized',
	'phrz' : 'pharyngealized',
	'latr' : 'lateral-release',
	'rhtz' : 'rhotacized',
	'gltz' : 'glottalized',
	'uvla' : 'uvular-affrication',
	'vlrs' : 'velar-stop', # no entries in db
	'vlrf' : 'velar-frication', # no entries in db
	'vlra' : 'velar-affrication', # no entried in db
	'uvls' : 'uvular-stop', # no entries in db
	'uvlf' : 'uvular-frication', # no entries in db
	# Prosodic Properties - Pros.
	'syll' : 'syllabic',
	'nsyl' : 'non-syllabic', # no entries in db
	'brev' : 'brief',
	'long' : 'long',
	'dwns' : 'downstep',
	'hlng' : 'half-long',
}

# FK_MAP is a mapping between the codes used in Fonetikode
# and this system; this system uses exclusively four-letter
# codes, distinct among the classes
FK_MAP = {
	# General Class
	'General Class' : {
		'c' :	'cons',
		'v' :	'vowl',
		'ss' :	'sseg',
	},

	# Vowel Vertical - no dashes in descriptions
	'V-V.' : {
		'c' :	'clos',
		'nc' :	'ncls',
		'cm' :	'cmid',
		'm' :	'vmid',
		'om' :	'omid',
		'no' :	'nopn',
		'o' :	'open',
	},

	# Vowel Horizontal - no dashes in descriptions
	'V-H.' : {
		'f' :	'frnt',
		'nf' :	'nfrt',
		'c' :	'cntr',
		'nb' :	'nbck',
		'b' :	'back',
	},

	# Vowel Modifiers
	'V-C.' : {
		# the feature 'nr' in Fonetikode is combined
		# in this system as 'n' + 'r'; the features
		# 'nur' (nasalized-u) and 'nru' (nasalized-r)
		# are converted to 'r' (round)
		'n' :	'vnsl',
		'r' :	'roun',
		'ur' :	'urrd',
		'ru' :	'rdur',
		'un' :	'unns',
		'nu' :	'nsun',
	},

	# Consonantal Place of Articulation
	'C-P.' : {
		# the feature 'e' (epiglottal) in Fonetikode is
		# converted into 'ph' (pharyngeal) in this
		# system
		'b' :	'blab',
		'bld' :	'blbd',
		'ba' :	'balv',
		'bpa' :	'bpav',
		'ld' :	'lbdt',
		'lv' :	'lvlr',
		'lu' :	'luvl',
		'll' :	'lglb', # no entries in database
		'i' :	'idnt',
		'd' :	'dntl',
		'a' :	'alvr',
		'pa' :	'palv',
		'r' :	'rtfx',
		'dv' :	'dtvl',
		'av' :	'avvl',
		'ap' :	'avpl',
		'p' :	'palt',
		'pav' :	'pavv',
		'v' :	'velr',
		'u' :	'uvlr',
		'ph' :	'phry',
		'g' :	'gltl',
	},

	# Consonantal Manner of Articulation
	'C-M.' : {
		's':	'stop',
		'f' :	'frct',
		'af' :	'affr',
		'n' :	'nasl',
		'a' :	'appr',
		't' :	'flap',
		'tr' :	'tril',
		'clk' :	'clck',
	},

	# Consonantal Sequencer
	'C-S.' : {
		# features 'prs' (pre-stopped) and 'pos' (post-stopped) were
		# removed, as there were no entries in the database
		's' :		'smpx',
		'c' :		'cmpx',
		'prn' :		'pnsz',
		'pon' :		'tnsz',
		'prg' :		'pglz',
		'pog' :		'tglz',
		'pra' :		'pasp',
		'poa' :		'tasp',
		'prag' :	'pasg',# , 'pre-aspirated&glottalized'], # no entries
#		'poag' :	'tasg' 'post-aspirated&glottalized'],
	},

	# Phonation
	'Phon.' : {
		# feature 'pvd'( pre-voiced-voiceless) was removed,
		# as there were no entries in the database
		'vl' :	'voil',
		'vd' :	'void',
		'b' :	'brth',
		'c' :	'crky',
	},

	# Initiation
	'Init.' : {
		'p' :	'plme',
		'gi' :	'glti',
		'ge' :	'glte',
		'vi' :	'veli',
	},

	# Primary Articulation Diacritics
	'Pri.' : {
		# feature 'dhb' (double-horizontal-bar-below) was
		# removed from primary articulation, and the consonantal
		# place of articulation is set to alveolar when it is
		# found in the database; likewise, 'd' (dental-articulation)
		# was removed and the consonantal place of articulation is
		# set to dental when found, and 'r' (rhotacized) was
		# removed setting the secundary articulation to
		# rhotacized when found
		'ret' :	'retr',
		'adv' :	'advc',
		'mc' :	'mctr',
		'lwd' :	'lwrd',
		'rzd' :	'razd',
		'ap' :	'apcl',
		'lam' :	'lmnl',
		'dvb' :	'frts',
		'ola' :	'lens',
		'c' :	'ctrz',
		'nas' :	'nasz',
	},

	# Secondary Articulation Diacritics
	'2nd' : {
		# features 'ret2' and 'nas' were removed, as they were not used in
		# the database and overlap with the retraction and
		# nasalization, respectively, set in first articulation;
		# combined features 'jw' ('palatalized-labialized'),
		# 'jv' ('palatalized-velarized'), 'wv' ('labialized-velarized'),
		# 'wph' ('labialized-pharyngealized'), 'wr'
		# ('labialized-with-rhotic-release'), 'jr'
		# ('palatalized-with-rhotic-release'), 'lv'
		# ('lateral and velarized'), 'lj'
		# ('lateral and palatalized'), 'lw' ('lateral and labialized'),
		# and 'lph' ('lateral and pharyngealized'), were removed and both
		# their constituents are set when found in the database
		'w' :	'lblz',
		'j' :	'pltz',
		'v' :	'vlrz',
		'ph' :	'phrz',
		'l' :	'latr',
		'r' :	'rhtz',
		'glt' :	'gltz',
		'vs' :	'vlrs', # no entries in db
		'vf' : 	'vlrf', # no entries in db
		'va' :	'vlra', # no entried in db
		'us' :	'uvls', # no entries in db
		'uf' :	'uvlf', # no entries in db
		'ua' :	'uvla',
	},

	# Prosodic Properties
	'Pros.' : {
		'syl' :		'syll',
		'nsyl' :	'nsyl', # no entries in db
		'brev' :	'brev',
		'long' :	'long',
		'ds' :		'dwns',
		'hl' :		'hlng',
	},

}

def read_phoible():
	phoible = {}

	# read phoible data
	with file(PHOIBLE_SEGS) as f:
		reader = csv.DictReader(f, delimiter='\t')
		for row in reader:
			ipa = row.pop('segment', None).decode('utf-8')
			phoible[ipa] = row

	return phoible

def read_fonetikode():
	fonetikode = {}

	# read fonetikode data and normalize Nones
	with file(FONETIKODE_SEGS) as f:
		reader = csv.DictReader(f, delimiter='\t')
		for row in reader:
			ipa = row.pop('Name', None).decode('utf-8')
			fonetikode[ipa] = row

	# iterate over all characters if 'fonetikode' to correct
	# errors, apply changes and normalize
	for ipa in fonetikode:
		# replace 'none' (a string) for empty string in Fonetikode;
		for key in fonetikode[ipa]:
			if fonetikode[ipa][key] == 'none':
				fonetikode[ipa][key] = ''

		# correct typo
		if fonetikode[ipa]['Pros.'] == 'breve':
			fonetikode[ipa]['Pros.'] = 'brev'

		# correct combined descriptors into single descriptors
		if fonetikode[ipa]['V-C.'] == 'nr':
			fonetikode[ipa]['V-C.'] = 'n r'

		if fonetikode[ipa]['2nd'] == 'jw':
			fonetikode[ipa]['2nd'] = 'j w'
		elif fonetikode[ipa]['2nd'] == 'jv':
			fonetikode[ipa]['2nd'] = 'j v'
		elif fonetikode[ipa]['2nd'] == 'wv':
			fonetikode[ipa]['2nd'] = 'w v'
		elif fonetikode[ipa]['2nd'] == 'wph':
			fonetikode[ipa]['2nd'] = 'w ph'
		elif fonetikode[ipa]['2nd'] == 'wr':
			fonetikode[ipa]['2nd'] = 'w r'
		elif fonetikode[ipa]['2nd'] == 'jr':
			fonetikode[ipa]['2nd'] = 'j r'
		elif fonetikode[ipa]['2nd'] == 'lv':
			fonetikode[ipa]['2nd'] = 'l v'
		elif fonetikode[ipa]['2nd'] == 'lj':
			fonetikode[ipa]['2nd'] = 'l j'
		elif fonetikode[ipa]['2nd'] == 'lw':
			fonetikode[ipa]['2nd'] = 'l w'
		elif fonetikode[ipa]['2nd'] == 'lph':
			fonetikode[ipa]['2nd'] = 'l ph'

		# split each entry (strings) into lists of features
		fk_classes = ['Pros.', 'Phon.', 'Pri.', '2nd', 'V-C.', 'V-V.',
			'V-H.', 'C-P.', 'Init.', 'C-M.', 'C-S.', 'General Class']

		for fk_class in fk_classes:
			fonetikode[ipa][fk_class] = fonetikode[ipa][fk_class].split()

	# correct what seems to be errors in the Fonetikode database;
	# an issue was opened on GitHub
	fonetikode[u'ɤ̃ː']['V-H.'] = ['b'] # was 'v'
	fonetikode[u'ᶑ']['C-M.'] = ['s'] # 'i'mplosive to 's'top, for consistency
	fonetikode[u'ʄ']['C-M.'] = ['s'] # ditto
	fonetikode[u'l̪̤']['Phon.'] = ['b'] # breathy
	fonetikode[u'k̟ʲʰ']['Phon.'] = ['vl'] # voiceless
	fonetikode[u'kʷʰː']['Phon.'] = ['vl'] # ditto
	fonetikode[u'p̃']['Pri.'] = ['nas'] # and not 'naas'

	# map the old codes to the new ones; even with the list
	# comprehension it is not particularly efficient, but should
	# be clear
	for ipa in fonetikode:
		for cl in fonetikode[ipa]:
			# tone, notes and id not needed now
			if cl in ['Tone.', 'Notes', 'ID']:
				continue

			# 'o' - old feature, 'n' - new feature
			for o in FK_MAP[cl]:
				n = FK_MAP[cl][o]
				tmp = [n if f == o else f for f in fonetikode[ipa][cl]]
				fonetikode[ipa][cl] = tmp

	# final corrections, for features not included in the mapping;
	# while doing it manually might be a bit more error-prone, it
	# should make it more clear to phonologists what we are doing
	for ipa in fonetikode:
		# simplification: dental articulation to dental
		if 'd' in fonetikode[ipa]['Pri.']:
			fonetikode[ipa]['Pri.'].remove('d')
			fonetikode[ipa]['C-P.'] = ['dntl'] # exclusive

		# simplification: alveolar articulation to dental
		if 'dhb' in fonetikode[ipa]['Pri.']:
			fonetikode[ipa]['Pri.'].remove('dhb')
			fonetikode[ipa]['C-P.'] = ['alvr'] # exclusive

		# simplification: rhotic only as secondary
		if 'r' in fonetikode[ipa]['Pri.']:
			fonetikode[ipa]['Pri.'].remove('r')
			if 'rhtz' not in fonetikode[ipa]['2nd']:
				fonetikode[ipa]['2nd'].append('rhtz')

		# simplification: retracted-2 as retracted
		if 'ret' in fonetikode[ipa]['2nd']:
			fonetikode[ipa]['2nd'].remove('ret')
			if 'ret' not in fonetikode[ipa]['Pri.']:
				fonetikode[ipa]['Pri.'].append('retr')

		# simplification: two categories
		if 'poag' in fonetikode[ipa]['C-S.']:
			fonetikode[ipa]['C-S.'].remove('poag')
			if 'tasp' not in fonetikode[ipa]['C-S.']:
				fonetikode[ipa]['C-S.'].append('tasp')
			if 'tglz' not in fonetikode[ipa]['C-S.']:
				fonetikode[ipa]['C-S.'].append('tglz')

		# simplification: epiglottal to pharyngeal
		if 'e' in fonetikode[ipa]['C-P.']:
			fonetikode[ipa]['C-P.'] = ['phry'] # exclusive

		# simplification: nasalized-u and nasalized-r to nasalized
		fonetikode[ipa]['V-C.'] = \
			['vnsl' if f in ['nur', 'nru'] else f \
				for f in fonetikode[ipa]['V-C.']]

	return fonetikode

def fk2str(fk):
	desc = []

	# prosodic properties
	s = ' and '.join([FK_STR[f] for f in fk['fk.pros'].split('|')])
	desc.append('(%s)' % s)
	# phonation
	s = ' and '.join([FK_STR[f] for f in fk['fk.phon'].split('|')])
	desc.append('(%s)' % s)
	# primary articulation diacritics
	s = ' and '.join([FK_STR[f] for f in fk['fk.pri'].split('|')])
	desc.append('(%s)' % s)
	# secundary articulation diacritics
	s = ' and '.join([FK_STR[f] for f in fk['fk.sec'].split('|')])
	desc.append('(%s)' % s)
	# vowel modifier
	s = ' and '.join([FK_STR[f] for f in fk['fk.vm'].split('|')])
	desc.append('(%s)' % s)
	# vowel vertical
	s = ' and '.join([FK_STR[f] for f in fk['fk.vv'].split('|')])
	desc.append('(%s)' % s)
	# vowel horizontal
	s = ' and '.join([FK_STR[f] for f in fk['fk.vh'].split('|')])
	desc.append('(%s)' % s)
	# consonantal place of articulation
	s = ' and '.join([FK_STR[f] for f in fk['fk.cp'].split('|')])
	desc.append('(%s)' % s)
	# initiation
	s = ' and '.join([FK_STR[f] for f in fk['fk.init'].split('|')])
	desc.append('(%s)' % s)
	# consonantal manner of articulation
	s = ' and '.join([FK_STR[f] for f in fk['fk.cm'].split('|')])
	desc.append('(%s)' % s)
	# consonantal sequencer
	s = ' and '.join([FK_STR[f] for f in fk['fk.cs'].split('|')])
	desc.append('(%s)' % s)
	# general class
	s = ' and '.join([FK_STR[f] for f in fk['fk.gc'].split('|')])
	desc.append('(%s)' % s)

	# remove empty descriptors
	desc = [d for d in desc if d != '()']

	# tone
	if fk['fk.tone']:
		desc.append('(#%s)' % fk['fk.tone'])

	# build final string, removing duplicates with no regex
	text = ' '.join(desc).strip()
	text = ' '.join(text.split())

	return text

def missing(phoible, fonetikode):
	# phonemes in common
	common = set(phoible).intersection(set(fonetikode))

	print 'extra phoible'
	for ipa in phoible:
		if ipa not in common:
			print '->', ipa

	print 'extra fonetikode'
	for ipa in fonetikode:
		if ipa not in common:
			print '->', ipa

def output(phoible, fonetikode):
	# phonemes in common
	common = set(phoible).intersection(set(fonetikode))

	header = True
	for ipa in common:
		d = {
			'ph.anterior' :		phoible[ipa]['anterior'],
			'ph.labiodental' :	phoible[ipa]['labiodental'],
			'ph.tone' :			phoible[ipa]['tone'],
			'ph.labial' :		phoible[ipa]['labial'],
			'ph.back' :			phoible[ipa]['back'],
			'ph.high' :			phoible[ipa]['high'],
			'ph.tap' :			phoible[ipa]['tap'],
			'ph.ejective' :		phoible[ipa]['raisedLarynxEjective'],
			'ph.implosive' :	phoible[ipa]['loweredLarynxImplosive'],
			'ph.click' :		phoible[ipa]['click'],
			'ph.spread' :		phoible[ipa]['spreadGlottis'],
			'ph.trill' :		phoible[ipa]['trill'],
			'ph.lateral' :		phoible[ipa]['lateral'],
			'ph.distributed' :	phoible[ipa]['distributed'],
			'ph.long' :			phoible[ipa]['long'],
			'ph.fortis' :		phoible[ipa]['fortis'],
			'ph.low' :			phoible[ipa]['low'],
			'ph.syllabic' :		phoible[ipa]['syllabic'],
			'ph.atr' :			phoible[ipa]['advancedTongueRoot'],
			'ph.delrel' :		phoible[ipa]['delayedRelease'],
			'ph.constr' :		phoible[ipa]['constrictedGlottis'],
			'ph.continuant' :	phoible[ipa]['continuant'],
			'ph.nasal' :		phoible[ipa]['nasal'],
			'ph.sonorant' :		phoible[ipa]['sonorant'],
			'ph.coronal' :		phoible[ipa]['coronal'],
			'ph.tense' :		phoible[ipa]['tense'],
			'ph.front' :		phoible[ipa]['front'],
			'ph.strident' :		phoible[ipa]['strident'],
			'ph.dorsal' :		phoible[ipa]['dorsal'],
			'ph.periodic' :		phoible[ipa]['periodicGlottalSource'],
			'ph.stress' :		phoible[ipa]['stress'],
			'ph.short' :		phoible[ipa]['short'],
			'ph.approximant' :	phoible[ipa]['approximant'],
			'ph.consonantal' :	phoible[ipa]['consonantal'],
			'ph.pharyngeal' :	phoible[ipa]['epilaryngealSource'],
			'ph.rtr' :			phoible[ipa]['retractedTongueRoot'],
			'ph.round' :		phoible[ipa]['round'],
			'fk.vm' :			'|'.join(fonetikode[ipa]['V-C.']),
			'fk.vh' : 			'|'.join(fonetikode[ipa]['V-H.']),
			'fk.init' : 		'|'.join(fonetikode[ipa]['Init.']),
			'fk.cm'	:			'|'.join(fonetikode[ipa]['C-M.']),
			'fk.pri' :			'|'.join(fonetikode[ipa]['Pri.']),
			'fk.sec' : 			'|'.join(fonetikode[ipa]['2nd']),
			'fk.pros' : 		'|'.join(fonetikode[ipa]['Pros.']),
			'fk.cs' :			'|'.join(fonetikode[ipa]['C-S.']),
			'fk.phon' :			'|'.join(fonetikode[ipa]['Phon.']),
			'fk.vv' :			'|'.join(fonetikode[ipa]['V-V.']),
			'fk.gc' :			'|'.join(fonetikode[ipa]['General Class']),
			'fk.cp' :			'|'.join(fonetikode[ipa]['C-P.']),
			'fk.tone' :			fonetikode[ipa]['Tone.'],
			'id' :				fonetikode[ipa]['ID'],
			'notes' :			fonetikode[ipa]['Notes'],
		}

		# get the list of all keys and sort it
		ph_keys = sorted([f for f in d if f.startswith('ph.')])
		fk_keys = sorted([f for f in d if f.startswith('fk.')])

		# print header if it is the first line
		if header:
			header = False

			buf = 'ipa,id,description,%s,%s,notes' % \
				(','.join(ph_keys), ','.join(fk_keys))
			print buf

		fields = [ipa, d['id'], fk2str(d)]
		fields += [d[f] for f in ph_keys]
		fields += [d[f] for f in fk_keys]
		fields += [d['notes']]

		# change commas in fields, such as in complex phoible
		fields = [v.replace(',', '|') for v in fields]

		# output to stdout
		print ','.join(fields).encode('utf-8')

if __name__ == '__main__':
	phoible = read_phoible()
	fonetikode = read_fonetikode()
	#missing(phoible, fonetikode)
	output(phoible, fonetikode)

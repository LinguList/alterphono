Alterphono
==========

## tl;dr

This project offers a (ultimately arbitrary) model for dimensionless distances between phonemes, available in files `minset.csv` (the most common phonemes) and `fullset.csv` (all phonemes in PHOIBLE). More info is available in the draft paper in this repository and on ArXiV, but, in short, the matrix looks something like this:

|   |   /a/  |  /i /  |  /j/   |    /k/ | /m/    |    /n/ |    /p/ |   /s/  |    /u/ | /w/    |
|:--|-------:|-------:|-------:|-------:|-------:|-------:|-------:|-------:|-------:|-------:|
| /a/ | 0.00 |      |      |      |      |      |      |      |      |      |
| /i/ | 0.29 | 0.00 |      |      |      |      |      |      |      |      |
| /j/ | 0.27 | 0.01 | 0.00 |      |      |      |      |      |      |      |
| /k/ | 0.38 | 0.31 | 0.32 | 0.00 |      |      |      |      |      |      |
| /m/ | 0.25 | 0.25 | 0.23 | 0.41 | 0.00 |      |      |      |      |      |
| /n/ | 0.25 | 0.25 | 0.20 | 0.43 | 0.12 | 0.00 |      |      |      |      |
| /p/ | 0.37 | 0.29 | 0.35 | 0.11 | 0.41 | 0.45 | 0.00 |      |      |      |
| /s/ | 0.89 | 0.77 | 0.80 | 0.64 | 0.99 | 0.99 | 0.69 | 0.00 |      |      |
| /u/ | 0.21 | 0.19 | 0.22 | 0.32 | 0.23 | 0.26 | 0.31 | 0.94 | 0.00 |      |
| /w/ | 0.24 | 0.22 | 0.22 | 0.34 | 0.19 | 0.24 | 0.29 | 0.97 | 0.01 | 0.00 |


## General info

This is a work in progress. You are probably here for the CSV files that compile information
from the Phoible database. The files are in the output directory, and are:

  - allophones: lists all phonemes found in the Phoible database along with the
    allophones for each phoneme across language inventories, with their absolute and
    relative counts
  - co-occurrence: a large phoneme by phoneme matrix with global counts of phoneme
    co-occurrences across language inventories; the diagonals are the global counts for
    each phoneme
  - inventories: list of all phonemes in all language inventories in Phoible, including
    each single allophone for each phoneme in the inventory
  - languages: informations on the languages in the database, such as languages names and
    codes, family, geographic location (including a center point with latitude and
    longitude), speaker population, etc.
  - phonemes: list of all phonemes in the database, with IPA representation (not complete),
    phoneme count across inventories and binary distinctive features

## Description of files in 'output'

### output/allophones.csv

Fields:
  - GlyphID - the unique ID for phonemes, to be used as index; it represents the 'base'
    (or most common) phoneme for a collection of allophones
  - Allophone - the allophone of the current row; this is expressed as an IPA symbol,
    and thus includes the phoneme that actually matches the GlyphID
  - Count - the count of the number of phonemic inventories that include the given
    phoneme as an allophone of GlyphID
  - Frequency - the frequency of the given phoneme as an allophone of GlyphID (i.e.,
    count of the given allophone divided by total count for the GlyphID)

### output/cooccurrence.csv

Each row and column are a phoneme found in Phoible inventories, with cells indicating
co-occurrences counts. The diagonals are thus the absolute count for each phoneme, that
can be used for calculating relative frequencies. 

### output/inventories.csv

Fields:
  - InventoryID: the unique ID for the phonemic inventory
  - Glottocode: the glottocode for the language of the current inventory
  - GlyphID: the GlyphID for a phoneme found in the current inventory
  - Phoneme: the IPA representation of the current glyph ID; this is only intended
    for database exploration by researchers, code should use the GlyphID field
  - Allophones: list of all allophones of the current glyph id for the current
    inventory, separated by vertical bars; the firts item is a copy of field 'Phoneme'

### output/languages.csv

Fields:
  - InventoryID: the unique ID for the phonemic inventory
  - LanguageCode: Ethnologue languagecode, three letters
  - LanguageName: language name, may contain spaces and punctuation
  - Glottocode: Glottocode for the current language, four letters and three numbers
  - GlottologName: language name in the Glottolog database
  - LanguageFamilyRoot: four letter code for the language family
  - LanguageFamilyGenus: description for the language family, intended for exploration
    by researchers (index with the LanguageFamilyRoot fields)
  - SpecificDialect: the specific dialect of the reported phonemic inventory, if any
  - Area: description of geographic area/continent
  - Country: description of the main political division
  - Latitude: floating point for the latitude
  - Longitude: floating point for the longitude
  - Population: population speaking the language as a first language
  - Phonemes: number of phonemes in the phonemic inventory
  - Consonants: number of consonants in the phonemic inventory
  - Tones: number of tones in the phonemic inventory
  - Trump: PHOIBLE Trump field
  - Source: Source for the phonemic inventory
  - phonemeslist: IPA representation of all phonemes in the inventory, ordered and
    separeted by vertical bars; intended for exploration by researchers, use the
    inventory database in code
  - Notes: notes on the language/inventory, if any

### output/phonemes.csv

Fields:
  - GlyphID
  - Phoneme: IPA phoneme representation
  - Count: count of phoneme across language inventories
  - Description: description of the phoneme; not intended for code use, only a guide
    in (some) cases from hard-coded names
  - Binary distinctive features:
    - advanced tongue root
    - anterior
    - approximant
    - back
    - click
    - consonantal
    - constricted glottis
    - continuant
    - coronal
    - delayed release
    - distributed
    - dorsal
    - epilaryngeal source
    - fortis
    - front
    - high
    - labial
    - labiodental
    - lateral
    - long
    - low
    - lowered larynx implosive
    - nasal
    - periodic glottal source
    - raised larynx ejective
    - retracted tongue root
    - round
    - short
    - sonorant
    - spread glottis
    - stress
    - strident
    - syllabic
    - tap
    - tense
    - tone
    - trill


# AlterPhono

AlterPhono is a software tool for developing and testing models of regular sound change, particularly suited for investigation of historical sound changes. It allows the development of models, consisting of ordered sets of sound-change rules, which are applied to one or more ancestor words; the final descendant form is shown along with any successive stages of development. While it does not share source code with it, AlterPhono is a descendent of a similar system called AlteruPhono developed by Tresoldi and Garcia in 2004; both systems are heavily inspired by the Phono system developed by Lee Hartman in conjunction with a model for Latin-to-Spanish (based mainly on Otero 1971 and Hartman 1974; see also Hartman 1985), which allowed not only to test the contents and order of proposed sound-change rules, but also the proposed forms of reconstructed ancestor words. This was the case when bin Muzaffar (1996a and 1996b) used Phono to model the development of Shawnee from Proto-Algonquian.

As was the case with Hartman's Phono, the prospect 

> of modeling language evolution often raises questions that make it necessary to clarify what [AlterPhono] will *not* do. [AlterPhono] deals only with regular change, although the derivation of some exceptional words can be simulated by temporarily masking a single rule in the chronological sequence (see Hartman 1986). The program deals with just one line of descendancy at a time (rather than deriving several sister-language forms simultaneously). It simulates only "downstream" derivation (that is, [it] cannot put a sound-change model "into reverse" and project upstream to generate ancestor words). Thus [AlterPhono] does not carry out directly the process of comparative reconstruction of one ancestor word from several descendants in different daughter languages, although it may indirectly help with that enterprise by testing hypotheses.

It is important to remember that, while it is inspired by and shares many ideias with Phono, AlterPhono is *not* compatible with any version of Hartman's software. Two main differences are the fact that AlterPhono allows to directly enter IPA symbols (by using Unicode) and that it uses a *parsing expression grammar* (or PEG) for rule descriptions: in other words, an analytical formal grammar, which is guaranteed to not be ambiguous, is used for expressing the rules.

## Theory

### SPE

Each sound is classified according to its binary values (`+` or `–`) with regard to twenty features, described as below, most of which are adopted from SPE, pp. 298-329 and 354. Although some of these features are now regarded as controversial, they are chosen here because SPE represents a unique moment of near-consensus in the development of phonological theory.  Thus the SPE features, while not universally preferred, come closest to being universally known.

The features are:

- *cons* (consonantal): "Consonantal sounds are produced with a radical obstruction in the midsagittal region of the vocal tract; nonconsonantal sounds are produced without such an obstruction" (SPE, p. 302). Consonants are `[+cons]`; vowels and glides are `[–cons]`.

- *syll* (syllabic): Indicating a syllabic peak. Vowels are `[+syll]`; glides are `[–syll]`; and consonants are normally also `[–syll]`, but liquids and nasal consonants "could become syllabic under special circumstances" (SPE, p. 354). This feature replaces the feature `[vocalic]` proposed on p. 302 of SPE.

The combination of the *cons* and *syll* features allow to distinguish, roughly, between consonants, glides and vowels, however making possible to have syllabic consonants and non-syllabic vowels, and even "syllabic glides" or "non-consonantal consonants". In our standard, we are treating only /j/ (palatal approximant), /ɰ/ (velar approximant), /ʍ/ (voiceless labiovelar approximant), /w/ (voiced labiovelar approximant) and /ɥ/ (labialized palatal approximant) as glides (i.e., non-syllabic and non-consonantal approximants), but this is subject to revision.

- *obstr* (obstruent): The inverse of SPE's `[sonorant]`. "Sonorants are sounds produced with a vocal tract cavity configuration in which spontaneous voicing is possible; obstruents are produced with a cavity configuration that makes spontaneous voicing impossible" (SPE, p. 302). Obstruents are constituted by the combination of (oral) stops (including affricates) and fricatives. In obstruents, the air flow is either interrupted (in the case of stops) or narrowed sufficiently to cause turbulence, and thus air noise (fricatives). Stops (including affricates) and fricatives are `[+obstr]`; vowels, glides, and liquid or nasal consonants are `[–obstr]`.

- *high*: "High sounds are produced by raising the body of the tongue above the level that it occupies in the neutral position; nonhigh sounds are produced without such a raising of the tongue body" (SPE, p. 304). High vowels such as [i], [u], and the front-rounded [y] are `[+high]`; glides such as [w] and [j] are `[+high]`; and palatal and velar consonants are `[+high]`. Labio-velars are also set to `[+high]`.

TODO: check `near-close` and `close-mid` vowels.

- *low*: "Low sounds are produced by lowering the body of the tongue below the level that it occupies in the neutral position; nonlow sounds are produced without such a lowering of the body of the tongue" (SPE, p. 305). Low vowels such as [a] and pharyngeal consonants such as Arabic ‘ayn [ʕ] are `[+low]`.

TODO: check `near-open` and `open-mid` vowels.
TODO: should `glottal` be `[+low]`? What about `uvular` (less probable)?

- *back*: "Back sounds are produced by retracting the body of the tongue from the neutral position; nonback sounds are produced without such a retraction from the neutral position" (SPE, p. 305). "Back vowels such as [o] and [u], and velar, uvular, and pharyngeal consonants are `[+back]`" (SPE, p. 305).

TODO: what about near-back vowels, such as /ʊ/?
TODO: what about labio-velar consonants?

- *round* (rounded): "Rounded sounds are produced with a narrowing of the lip orifice; nonrounded sounds are produced without such a narrowing" (SPE, p. 309). Rounded back vowels such as [o] and [u], the rounded front vowel [y], the glide [w], and labiovelar consonants such as [kʷ] and [gʷ] are `[+round]`.

- *cor* (coronal): "Coronal consonants are produced with the blade of the tongue raised from its neutral position; noncoronal sounds are produced with the blade of the tongue in the neutral position" (SPE, p. 304). Dental, alveolar, and palatal consonants are `[+cor]`, labial and velar consonants are `[–cor]`, vowels and glides are generally `[–cor]` (but retroflex vowels can be `[+cor]`). Postalveolars and alveolopalatals were also set to `[+cor]`.

- *ant* (anterior): "Anterior sounds are produced with an obstruction that is located in front of the palato-alveolar region of the mouth; nonanterior sounds are produced without such an obstruction" (SPE, p. 304). Labial, dental, and alveolar consonants are `[+ant]`, palatal and velar consonants are `[–ant]`, vowels and glides are `[–ant]`.

TODO: what about /ɥ/ (labialized palatal approximant) and other labialized consonants?
TODO: post-alveolars were not set to this features, but what about alveolo-palatal and palato-alveolar? For the time being, these two are set, but it is subject to revision.

- *distr* (distributed): SPE's definition of this feature refers only to consonants: "Distributed sounds are produced with a constriction that extends for a considerable distance along the direction of the air flow; nondistributed sounds are produced with a constriction that extends only for a short distance in this direction" (p. 312). Among consonants, then, this feature distinguishes articulatorily between the following pairs of classes of sounds:

|                                             | +distr    | –distr       |
| ------------------------------------------- | --------- | ------------ |
| upper lip vs. edge of upper incisors        | bilabials | labiodentals |
| inner face of upper incisors vs. their edge | dentals   | interdentals |
| tongue blade vs. tip of tongue              | laminals  | apicals      |
| velum vs. uvula                             | velars    | uvulars      |

TODO: work on the distinction between dental and interdental, not set in the reference yet.
TODO: the distinction between laminals and apicals should only apply to coronals, if I am correct; work is needed, nothing was set in the reference yet.
TODO: should labiovelars be distributed? only when glides? nothing set yet.

Additionally, AlterPhono's usage extends the value `[+distr]` to vowels and glides.

TODO: check if all glides should be `[+distr]`, in particular voiceless ones.

- *cont* (continuant): Continuant sounds are those in whose production  "the primary constriction in the [vocal] tract is not narrowed to the point where the air flow past the constriction is blocked; in [both oral and nasal] stops the air flow through the [center of the] mouth is effectively blocked" (SPE, p. 317; emphasis added). The feature `[cont]` is the main distinguisher between stops `[–cont]` and fricatives `[+cont]`. Although the value of this feature in liquids is controversial, AlterPhono takes the "tap" and trilled [r] as `[+cont]`, and laterals as `[–cont]`, based on reasoning given by SPE (p. 318). Please note that the term "continuant" refers only to the ability of the airflow to continue past a primary constriction in the mouth, not broadly to just any continuation of the airflow.  On this basis, nasal and lateral consonants can be `[–cont]` and still allow the airflow to "continue", and vowels and glides are `[+cont]`.

Hartman does not explicitly mark affricates as `[+cont]`, possibly because they don't seem to be treated as a single phoneme but as a stop plus fricative in his Latin to Spanish models, but here they are set.

TODO: as with `[distr]`, check if all glides should be marked as continuant in the reference.
TODO: confirm that lateral fricatives should me marked as `[+cont]` (as currently in the reference)

- *delrel* (delayed release): SPE uses this feature to differentiate affricates and fricatives `[+delrel]`, on one hand, from plain stops `[–delrel]` on the other.  In the SPE definition, Delayed Release characterizes consonants in which "turbulence is generated in the vocal tract so that the release phase of affricates is acoustically quite similar to the cognate fricative" (p. 318). AlterPhono more broadly treats as `[+delrel]` all sounds except plain oral stops.  In addition to fricatives and affricates, all vowels, glides, and nasal or liquid consonants are `[+delrel]`.

TODO: based on Hartman's reasoning, implosives, like stops, are not marked for delayed release in my reference, but this should be checked.

- *strid* (strident): "Strident sounds are marked acoustically by greater noisiness [due to air turbulence] than their nonstrident counterparts" (SPE, p. 329). Only fricatives and affricates can be `[+strid]`; all other sounds are `[–strid]`. Among fricatives, this feature serves to differentiate acoustically between the following pairs of classes of sounds:

| `[+strid]`      | `[–strid]`    |
| --------------- | ------------- |
| labiodental     | bilabial      |
| dental/alveolar | interdental   |
| uvular          | velar         |

TODO: it is not exactly clear if Hartman treats only labiodental, dental, alveolar and uvular fricatives as strident, or all fricatives plus other sounds. Should check, nothing was set in the reference.

- *voice* (voiced): Voiced sounds, in the simplest terms, are those in whose production the vocal cords vibrate (see SPE, pp. 326-327). Vowels, glides, and sonorants tend to be `[+voice]`. This feature serves mainly to distinguish between voiceless and voiced obstruents.

TODO: Note that /ʍ/, while a glide, was not set to `[+voice]`, as it is defined as a voiceless labiovelar approximant; should check its actual syllabicity.

- *nasal* (nasal): "Nasal sounds are produced with a lowered velum which allows the air to escape through the nose; nonnasal sounds are produced with a raised velum so that the air from the lungs can escape only through the mouth" (SPE, p. 316). The nasal consonants [m] and [n], and nasal vowels such as [ã] and [õ] are `[+nasal]`.

- *lateral* (lateral): "Lateral sounds are produced by lowering the mid section of the tongue at both sides or at only one side, thereby allowing the air to flow out of the mouth in the vicinity of the molar teeth; in nonlateral sounds, no such side passage is open" (SPE, p. 317). SPE adds that this features "is restricted to coronal consonantal sounds" (p. 317).

TODO: in the reference, it was added to all coronal sounds, including approximants; should check.

- *tense*: "Tense sounds are produced with a deliberate, accurate, maximally distinct gesture that involves considerable muscular effort; nontense sounds are produced rapidly and somewhat indistinctly" (SPE, p. 324). SPE adds that one of the differences "between tense and lax [i.e. nontense] vowels is that the former are executed with a greater deviation from the neutral or rest position of the vocal tract than are the latter" (p. 324). Since the features `[high]` and `[low]` distinguish only three degrees of vowel height (the combination `[+high, +low]` is not permitted), AlterPhono uses the feature [tense] to differentiate the "upper mid" vowels, such as [e] and [o] (`[+tense]`) from the "lower mid" vowels, such as [ɛ] and [ɔ](`[–tense]`). Voiceless consonants are generally treated as `[+tense]`, and voiced ones as `[–tense]`.

TODO: voiceless consonants were not set to `[+tense]`, as per above, but this should be checked (isn't `[-voice]` enough?)
TODO: nothing was set, as Hartman's Latin to Spanish model is not clear and seems to set all vowels to tense, including low ones.

- *long*: Long sounds are of contrastively longer duration than nonlong sounds. This feature was not proposed by SPE, but AlterPhono's inventory includes this feature first implemented in Hartman's Phono, as it was developed in conjunction with a model for Spanish, as derived from Latin, and Latin has contrastive vowel length. AlterPhono also uses this feature to differentiate between the "tap" and the trilled [r], and it is potentially available to contrast geminate consonants with their simple counterparts.

- *stress*: As a "prosodic" feature (SPE, p. 68), stress is generally associated with an entire syllable, rather than a single segment. The stressed syllable of a word has relatively greater "prominence" than the other syllables of the word, based on some combination of loudness, pitch, and duration. AlterPhono's default alphabets arbitrarily allow only vowels to be marked as `[+stress]`.

- *asp*: Aspirated stops are accompanied by a short period of audible breath that immediately follows their release.  SPE does not include this feature in its inventory, but rather accounts for it as a combination of "heightened subglottal pressure" and absence of "glottal constriction" (p. 326).

### Traditional

The usage of binary features modeled after Chomsky & Halle can be difficult and not intuitive in some cases, particularly for beginners. We also implemented "standard" features like "voiced" and "fricative", whose list is given below. Traditional features are always described by three-letter codes, heavily based on those described by Evan Kirshenbaum in its paper "Representing IPA phonetics in ASCII", but we made some modification to suit our program needs.

three letters
single words (with hyphens)

| Feature               | Category            |
| --------------------- | ------------------- |
| voiced                | voiceness           |
| voiceless             | voiceness           |
| bilabial              | consonant-place     |
| labio-dental          | consonant-place     |
| dental                | consonant-place     |
| alveolar              | consonant-place     |
| retroflex             | consonant-place     |
| palato-alveolar       | consonant-place     |
| palatal               | consonant-place     |
| postalveolar          | consonant-place     |
| velar                 | consonant-place     |
| labio-velar           | consonant-place     |
| labio-palatal         | consonant-place     |
| uvular                | consonant-place     |
| pharyngeal            | consonant-place     |
| glottal               | consonant-place     |
| epiglottal            | consonant-place     |
| palato-alveolar-velar | consonant-place     |
| stop                  | consonant-manner    |
| fricative             | consonant-manner    |
| nasal                 | consonant-manner    |
| oral                  | consonant-manner    |
| approximant           | consonant-manner    |
| vowel                 | consonant-manner    |
| lateral               | consonant-manner    |
| central               | consonant-manner    |
| trill                 | consonant-manner    |
| flap                  | consonant-manner    |
| click                 | consonant-airstream |
| ejective              | consonant-airstream |
| implosive             | consonant-airstream |
| high                  | vowel-height        |
| semi-high             | vowel-height        |
| upper-mid             | vowel-height        |
| mid                   | vowel-height        |
| lower-mid             | vowel-height        |
| semi-low              | vowel-height        |
| low                   | vowel-height        |
| front                 | vowel-backness      |
| near-front            | vowel-backness      |
| central               | vowel-backness      |
| near-back             | vowel-backness      |
| back                  | vowel-backness      |
| unrounded             | roundness           |
| rounded               | roundness           |
| aspirated             | release             |
| unexploded            | release             |
| murmured              | release             |
| syllabic              | syllabicity         |
| long                  | longness            |
| velarized             | co-articulation     |
| labialized            | co-articulation     |
| palatalized           | co-articulation     |
| rhoticized            | co-articulation     |
| nasalized             | co-articulation     |
| pharyngealized        | co-articulation     |

## Rule Grammar

A grammar in AlterPhono is composed by one or more rules of sound change. A rule is composed by a unique rule name, a set of one or more IF-directives that specify a match, and a set of one or more THEN-directives that specify the changes to be performed.

Grammars are written in pure-text files. Spaces are discarded whenever possible, so you can freely use whitespaces and tabulations to align rules in your preferred way. Single line comments are allowed, using the syntax of the C programming languages: comments start with ``//`` and end at the new-line character.

A very simple grammar, with a single rule, could be described as follow:

```
// This is a comment

RULE: VOICE_RULE1
IF: i -voice
IF: i+1 +voice
THEN: i +voice
END
```

We are now going to analyze this rule, which look for occurences of unvoiced consonants followed by voices consonants, changing this into a voiced one.

Directives in AlterPhono begin with commands, which are always written with capital letters, such as in ``RULE`` and ``IF``. In the case of introduction of new commands in future versions of AlterPhono, this will be preserved.

The commands can optionally be followed by a colon, which is recommended to visually distinguish them from the command *arguments*. However, they are disregared just as any white space, so the first line could be changed as below, resulting in exactly the same rule (notice that we also removed the colon):

```
// This is a comment

       RULE            VOICE_RULE1
IF: i -voice
IF: i+1 +voice
THEN: i +voice
END
```

Rule names must follow a strict rule: they can be composed only with characters from ``a`` to ``z`` (including capitals), with digits from ``0`` to ``9`` and with the punctuation characters of ``.`` (dot), ``-`` (hyphen) and ``_`` (underscore); in particular, please note that Unicode and extended ASCII characters (such as accentuated letters, or IPA symbols) are *not* allowed. This was implemented intentionally, to avoid confusions when sharing rules with other researchers. While you can freely use the characters listed above, the convention for rule names is to only use capital letters, separating words with underscores; numbers should be only used at the end of the rule name.

An ``IF`` directive specifies a condition that must be met by a phoneme for a match by taking two obligatory arguments: (a) a position and (b) a list of features *or* an IPA phoneme representation (optionally followed by a list of modifying features).

Regarding positions, remember that when working on a word (which, interally, is a sequence of phonemes), AlterPhono scans it from the first to the last item, looking for matches and applying changes as needed. Phonemes are indexed from 1 to the end of the word, but they can also be referred to with negative indexes, counting from the end, so that -1 is the last phoneme. For example, take the word ``international`` as represented in IPA according to a standard American pronountiaion, /ˌɪntɚˈnæʃənəl/. This word is composed of eleven phonemes, each of them can be referred to by a positive index, counting from the beginning, or a negative one, counting from the end, so that, for example, you can refer to its /ʃ/ by either index 7 or 5.

| Phonemes                                               |
| ------------------------------------------------------ |
| ɪ   | n   | t  | ɚ  | n  | æ  | ʃ  | ə  | n  | ə  | l  |
| 1   | 2   | 3  | 4  | 5  | 6  | 7  | 8  | 9  | 10 | 11 |
| -11 | -10 | -9 | -8 | -7 | -6 | -5 | -4 | -3 | -2 | -1 |

If you specify the index for a phoneme that does not exist (such as giving an ``IF`` directive for the fifth phoneme in a word composed of less than five phonemes), the rule simply does not match. This indexes are used mostly to refer to rules that are applied only to the first or last phoneme in a word: for example, to make sure that a given rule is only applied to the phoneme /s/ at the beginning of a word, you could write, as we will see, ``IF: 1 /s/``. In the same way, if a rule is only to be applied when a word ends with a nasal phoneme, you could write ``IF: -1 +nasal``.

The most useful feature of position is, however, the index of the current phoneme, specified by the variable ``i``: this value is automatically updated when AlterPhono scans a word, so that the rule will match every single occurence in the word, no matter the position of the phoneme. If you recall our first example rule, you will see that we used ``i`` and ``i+1`` to refer to the current and the next character, respectively. 
```
RULE: VOICE_RULE1
IF: i -voice
IF: i+1 +voice
THEN: i +voice
END
```

It does not matter if the match is found at the beginning, in the middle or at the end of the word: by using the ``i`` variable, you will match every single occurence. These relative indexes can specify both indexes before (with negative numbers) and after (with positive numbers) the current phoneme (there is no internal limit on these values: in theory, you could even specify the 100th phoneme before the current one with ``i-100``). Once more, if the index refers to a phoneme that does not exist the rule is just skipped: this is what happens, for example, with the rule above when the scanning of the word gets to the last phoneme and the position indicated by ``i+1`` does not exist.


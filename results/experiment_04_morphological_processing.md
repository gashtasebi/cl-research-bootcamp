# Experiment 4 — Morphological Processing

## Objective

The goal of this experiment was to compare stemming,
lemmatization, and POS-aware lemmatization.

## Dataset

The experiment used a small English test corpus containing
plural nouns, verb inflections, adjectives, and irregular forms.

## Methods

### 1. Stemming

PorterStemmer was used to reduce words to stems.

Examples:

- studying → studi
- languages → languag
- useful → use

The resulting stem is not necessarily a valid word.

### 2. Lemmatization without POS

WordNetLemmatizer was initially used without explicitly
providing part-of-speech information.

Examples:

- students → student
- languages → language
- children → child
- studying → studying
- running → running

The method works well for some nouns but does not
correctly normalize many verb forms.

### 3. POS-aware Lemmatization

The tokens were first POS-tagged using NLTK.

Penn Treebank tags were mapped to WordNet POS tags:

- N* → noun
- V* → verb
- J* → adjective
- R* → adverb

Examples:

- studying → study
- studied → study
- running → run
- played → play
- writing → write
- children → child
- mice → mouse
- better → good

## Observations

POS information substantially improved lemmatization
of inflected verb forms.

Stemming produced shorter strings, but some were not
valid lexical forms, such as "studi" and "languag".

POS-aware lemmatization produced linguistically meaningful
lemmas for many inflected forms.

## Error Analysis

The POS tagger assigned:

- mice → NN

although "mice" is plural in the sentence
"The cats are chasing mice."

The correct lemma was nevertheless produced:

mice → mouse

This demonstrates that errors in an upstream NLP component
can potentially affect downstream processing.

## Research Observation

Morphological normalization is not independent of
syntactic information.

The experiment demonstrates a pipeline:

Tokenization
→ POS Tagging
→ POS Mapping
→ Lemmatization

The quality of later processing can depend on the quality
of earlier processing.

## Conclusion

Stemming is simple and fast but may produce non-word stems.

Lemmatization produces linguistically meaningful base forms,
but POS information can be necessary for accurate processing.

POS-aware lemmatization therefore provides a more
linguistically informed normalization strategy for this
dataset.

# Experiment 8 — Computational Semantics

## Research Question

Can a small rule-based interpreter map simple English sentences to semantic representations containing entities, properties, and relations?

## Hypothesis

For sentences that match its supported patterns and vocabulary, the interpreter will create entity identifiers, represent nouns as unary predicates, and represent verbs as relations whose arguments preserve the subject–object order.

## Dataset

The manually constructed dataset in `data/semantics_test.txt` contains ten sentences:

- Six initial examples covering transitive and intransitive sentences
- Two examples containing an unsupported verb or plural noun
- Two additional sentences that reverse the subject and object noun types

The examples include sentences such as `A student reads a book.`, `The student sleeps.`, and `A teacher sees a student.`

## Method

The interpreter uses regular-expression patterns to recognize two sentence forms:

- Determiner + singular noun + transitive verb + determiner + singular noun
- Determiner + singular noun + intransitive verb

A small lexicon lists the supported nouns and verbs. The interpreter normalizes sentence case and removes final punctuation. Each sentence-internal entity receives an identifier such as `e1` or `e2`. Nouns become unary predicates, and verbs become predicates with one or two arguments.

For example:

`A student reads a book.`

is represented as:

`student(e1) AND book(e2) AND read(e1, e2)`

The first argument of a transitive predicate corresponds to the subject, and the second corresponds to the object. Verb forms such as `reads` are mapped to a normalized predicate such as `read`.

## Results

| Outcome | Count |
|---|---:|
| Sentences interpreted | 8 |
| Sentences unsupported | 2 |
| Total sentences | 10 |

The two unsupported sentences were:

- `The student admires a teacher.` — the transitive verb `admires` was not in the lexicon.
- `The students read a book.` — the plural noun `students` was not in the supported noun list and sentence pattern.

The subject–object comparison produced:

| Sentence | Semantic representation |
|---|---|
| `A student sees a teacher.` | `student(e1) AND teacher(e2) AND see(e1, e2)` |
| `A teacher sees a student.` | `teacher(e1) AND student(e2) AND see(e1, e2)` |

The changed noun predicates show that reversing the subject and object changes the entities occupying the first and second argument positions of `see`.

## Interpretation

For the supported sentence patterns, the interpreter represented entities, noun properties, and verb relations. The argument order of transitive predicates preserved the subject–object order in the input sentence. Intransitive verbs were represented with a single entity argument; for example, `The student sleeps.` became `student(e1) AND sleep(e1)`.

The sentence `The book sees a student.` was interpreted as `book(e1) AND student(e2) AND see(e1, e2)`. This is useful evidence about the system's scope: it maps the recognized sentence structure and lexical items to predicates, but does not use world knowledge to determine whether the resulting situation is plausible.

## Limitations

The dataset is small and manually constructed. The interpreter recognizes only a narrow set of sentence patterns, singular nouns, and explicitly listed verb forms. Unsupported inputs are rejected rather than parsed more generally.

The determiners `a` and `the` are treated identically. Entity identifiers are local to each sentence, and the representation does not model quantifier scope, definite reference, or links between entities across sentences. The program also does not evaluate semantic plausibility or compare its output with a manually annotated gold semantic representation.

Therefore, this experiment demonstrates a basic rule-based mapping to predicate representations; it is not a general semantic parser.

## Conclusion

Experiment 8 implemented a small rule-based semantic interpreter for simple English sentences. It interpreted eight of ten test sentences, representing nouns as properties of entities and verbs as relations between entities. It preserved subject–object order in transitive predicates and represented intransitive predicates with one argument.

The experiment also exposed clear limits: coverage depends on the hand-written patterns and lexicon, and a structurally interpretable sentence may still be semantically implausible. The results provide a practical introduction to entities, predicates, relations, and semantic representations.

## Files

- `data/semantics_test.txt` — test sentences
- `src/semantic_interpreter.py` — rule-based semantic interpreter
- `results/experiment_08_computational_semantics.md` — experiment report

# Experiment 7 — Formal Languages and Finite Automata

## Research Question

Can a deterministic finite automaton (DFA) and an equivalent regular expression recognize the same language of strings over `{a, b}` that end in `ab`?

## Hypothesis

The DFA and the regular expression `[ab]*ab` will agree on whether each test string belongs to the language.

## Language

The experiment defines the language:

> All strings over the alphabet `{a, b}` whose final two symbols are `ab`.

The empty string is not in the language. Strings containing symbols outside `{a, b}` are also rejected.

## DFA Design

The DFA has three states:

- `q0` is the start state. It represents that the input read so far does not end in a useful `a`.
- `q1` represents that the input read so far ends in `a`.
- `q2` is the accepting state. It represents that the input read so far ends in `ab`.

The transition function is:

| Current state | Input `a` | Input `b` |
|---|---|---|
| `q0` | `q1` | `q0` |
| `q1` | `q1` | `q2` |
| `q2` | `q1` | `q0` |

The start state is `q0`, and the accepting state is `q2`.

## Regular Expression

The equivalent regular expression used in the experiment is:

`[ab]*ab`

Python's `re.fullmatch` was used so that the entire input string had to match the pattern.

## Dataset and Method

Ten test strings were stored in `data/automata_test.txt`. The dataset included:

- Strings expected to be accepted, such as `ab`, `aab`, `bab`, and `babab`
- Strings over `{a, b}` that do not end in `ab`, such as `a`, `b`, `ba`, and `abb`
- The empty string
- `abc`, which contains a symbol outside the alphabet

For each input, the program recorded the states visited by the DFA, its acceptance decision, the regular expression's decision, and whether the two methods agreed.

## Results

| Input | DFA | Regular expression | Agreement |
|---|---|---|---|
| Empty string | Rejected | Rejected | Yes |
| `ab` | Accepted | Accepted | Yes |
| `aab` | Accepted | Accepted | Yes |
| `bab` | Accepted | Accepted | Yes |
| `babab` | Accepted | Accepted | Yes |
| `a` | Rejected | Rejected | Yes |
| `b` | Rejected | Rejected | Yes |
| `ba` | Rejected | Rejected | Yes |
| `abb` | Rejected | Rejected | Yes |
| `abc` | Rejected | Rejected | Yes |

The DFA accepted 4 of the 10 test strings. The DFA and regular expression agreed on all 10 inputs, with no disagreements.

## Interpretation

The results are consistent with the hypothesis for the tested examples. The DFA's accepting state `q2` represents that the input read so far ends in `ab`. For example, `abb` reaches `q2` after reading `ab`, but the final `b` moves it to `q0`, so the complete string is rejected.

The invalid symbol in `abc` caused the DFA to reject the string because `c` is not part of the alphabet. The regular expression also rejected it because the complete string does not match `[ab]*ab`.

This experiment illustrates the relationship between regular expressions and finite automata: both can specify and recognize regular languages. The state trace makes explicit how the automaton processes a string one symbol at a time.

## Limitations

The experiment used a small, manually selected set of ten strings. Agreement on these examples is evidence that the implementations behave consistently on this test set; it is not a formal proof that the DFA and regular expression define exactly the same language.

The language itself is intentionally simple, and the experiment does not cover nondeterministic finite automata or automaton minimization.

## Conclusion

Experiment 7 implemented a DFA for strings over `{a, b}` that end in `ab`, compared it with the regular expression `[ab]*ab`, and visualized the DFA's states and transitions.

The DFA accepted four test strings. It agreed with the regular expression on all ten test cases. The state diagram and state traces demonstrated how states, transitions, the start state, and an accepting state determine whether an input belongs to a formal language.

## Files

- `data/automata_test.txt` — test strings
- `src/finite_automaton.py` — DFA, regex comparison, summary, and state diagram
- `results/experiment_07_formal_languages_automata.md` — experiment report

# Experiment 2 — Tokenization Error Analysis

## Objective

The goal of this experiment is to identify limitations
of a simple regular-expression-based tokenizer.

## Test Cases

The tokenizer was tested on:

- abbreviations
- decimal numbers
- URLs
- email addresses
- hyphenated expressions
- contractions
- uppercase abbreviations

## Observed Problems

### Abbreviations

Example:

Dr. Smith

The tokenizer separates "Dr" and ".".

### Decimal Numbers

Example:

12.50

The tokenizer separates the number into:

12
50

### URLs

Example:

https://example.com

The URL is split into multiple tokens.

### Email Addresses

Example:

test@example.com

The email address is split into multiple tokens.

### Hyphenated Expressions

Example:

state-of-the-art

The expression is split into several tokens.

## Research Observation

A tokenizer cannot be evaluated independently from the
task and dataset.

A tokenization strategy that is useful for one NLP task
may not be optimal for another task.

## Next Step

Compare the custom tokenizer with a standard NLP tokenizer
and investigate which tokenization strategy is more suitable
for the dataset.

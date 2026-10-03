from pathlib import Path
import re

from nltk.stem import PorterStemmer, WordNetLemmatizer


# Load the test dataset.
data_path = Path("data/morphology_test.txt")
text = data_path.read_text(encoding="utf-8")


# Extract word tokens.
tokens = re.findall(r"\b[a-zA-Z]+\b", text.lower())


# Initialize NLP tools.
stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()


print("=== MORPHOLOGICAL PROCESSING ===")
print()

print(f"{'WORD':<15} {'STEM':<15} {'LEMMA':<15}")
print("-" * 45)

for token in tokens:
    stem = stemmer.stem(token)
    lemma = lemmatizer.lemmatize(token)

    print(f"{token:<15} {stem:<15} {lemma:<15}")

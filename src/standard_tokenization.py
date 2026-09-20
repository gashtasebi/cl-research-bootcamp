from pathlib import Path
import nltk
from nltk.tokenize import word_tokenize

# Download the tokenizer data requierd by NLTK.
nltk.download("punkt_tab", quiet=True)


# Load the test text.
test_path = Path("data/tokenization_test.txt")
text = test_path.read_text(encoding="utf-8")


#Tokenize the text with NLTK.
tokens = word_tokenize(text)


print("-- STANDARD NLP TOKENIZATION ---")
print()
print("Original text:")
print(text)

print("Tokens:")
for token in tokens:
    print(f"-{token}")

print()
print("Number of tokens: ", len(tokens))

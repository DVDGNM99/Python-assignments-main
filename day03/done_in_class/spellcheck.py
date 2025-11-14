from difflib import get_close_matches

# List of correct words (the "dictionary")
word_list = ["House", "Cat", "Dog", "Tree", "Sun", "Moon", "Flower", "Book", "School", "Sea"]

# Text to check
text = "Hous and Cta sleep under the Son and look at the Mon"

# Split the text into words
words = text.split()

# Simple spellchecker
for word in words:
    # If the word is not in the dictionary
    if word not in word_list:
        # Find the closest match
        suggestion = get_close_matches(word, word_list, n=1, cutoff=0.6)
        if suggestion:
            print(f"❌ '{word}' not found. Did you mean '{suggestion[0]}'?")
        else:
            print(f"❌ '{word}' not found. No suggestion available.")
    else:
        print(f"✅ '{word}' is correct.")

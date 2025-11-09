# notes for the third lecture of python in Weizmann

1. how to know your code work? - write a second program that can take an input and run the first program, then compare the output to some expected output we already know. sometimes the output isn't always the same (like telling time, or value of gold) [arad zulti]
2. file.toml used like an env.yml file in my day 02 project
3. mkdirname creates a directory
4. uv init creates files in the directory with all the necessary files to make sure that whoever uses the program can run it in the correct way
5. create a spellchecker (create a list of words and compare, if a word isnt included then is a typo and referes to the closest word to the one typed)
6. open a couple of project on my PC
7. methos of strings (look up what it means exactly, for example string.lower)-> look: string methods in python. in this case lower can trasform Capital letters in a word into lowercase letters

```python
# this is code:
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
```
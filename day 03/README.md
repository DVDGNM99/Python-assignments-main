# notes for the third lecture of python in Weizmann

1. how to know your code work? - write a second program that can take an input and run the first program, then compare the output to some expected output we already know. sometimes the output isn't always the same (like telling time, or value of gold) [arad zulti]
2. file.toml used like an env.yml file in my day 02 project, but interactive and changes and updates itself
3. mkdirname creates a directory
4. uv init creates files in the directory with all the necessary files to make sure that whoever uses the program can run it in the correct way
5. create a spellchecker (create a list of words and compare, if a word isnt included then is a typo and referes to the closest word to the one typed)
6. open a couple of project on my PC
7. methos of strings (look up what it means exactly, for example string.lower)-> look: string methods in python. in this case lower can trasform Capital letters in a word into lowercase letters
---
## how to visualize code in MD
```python
# this is code:
for n in range (0, 4):
 print (n)
#this is a list
frutti = ["apple", "ananas", "dog"]
# this creates a list of zeros that are as may as characters in len (in the example len was a word)
[0] * (len+1)
# to create a matrix 
[0] * (len+1) for _ in range (len1 +1)
```
---

8. how to check that spellcheck works in the correct way: Pytest library (check what it does)
9. list are changeble while touple is unchangable 
10. **assert** tool in python (check it)
11. find a library to match your code Goal (before making a script, its likely someone already did)-> [pypy](https://pypi.org/)
12. remember always to explain in the readme how to download the dependenceis
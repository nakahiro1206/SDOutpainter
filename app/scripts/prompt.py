import random
def prompt_generate():
    word_file = '../misc/nouns.txt' 
    words = open(word_file).read().splitlines()
    length = len(words)
    prompt = ""
    for _ in range(30):
        idx = random.randint(0, length - 1)
        prompt += f"{words[idx]};"
    print(prompt)
    print("!!NEED TO EXCLUDE INAPPRORIATE WORDS!!")
    return prompt

def negative_prompt_generate():
    return "ugly"
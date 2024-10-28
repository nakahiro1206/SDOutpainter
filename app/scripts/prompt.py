import random
def prompt_generate():
    #return "A surreal dreamscape with floating islands, cascading waterfalls into the void, and fantastical creatures soaring through a colorful, ethereal sky."
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
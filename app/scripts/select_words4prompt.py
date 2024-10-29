import random

noun_list = ["flower", "car", "volcano", "dog", "cat", "bridge", "lake", "sunset", "castle", "waterfall", "cactus", "jungle", "aquarium", "campfire", "lighthouse", "galaxy", "zoo", "fireworks", "tree", "pumpkin", "planet", "octopus", "skyscraper", "elephant", "giraffe", "fish", "vegetable", "tower", "penguin", "cake", "helicopter", "windmill", "canyon", "oasis", "ship", "violin"]

adjective_list = ["aesthetic", "serene", "majestic", "gorgeous", "luminous", "vibrant", "tranquil", "gloomy", "icy", "cozy", "peaceful", "tropical", "abandoned", "nostalgic", "colorful", "harmonious", "absorbing", "astonishing", "energetic", "exotic", "playful", "provoking"]

def gen_prompt():
    noun = noun_list[random.randint(0, len(noun_list)-1)]
    adj = adjective_list[random.randint(0, len(adjective_list)-1)]
    theme = adj + " " + noun
    return theme + ", drawing"

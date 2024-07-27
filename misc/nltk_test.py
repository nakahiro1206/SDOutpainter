from nltk import download
from itertools import chain
from nltk.corpus import wordnet

# download('wordnet')

synsets = wordnet.all_synsets('n')
chained = []
for synset in synsets:
    print(synset.name())
    l = [n.replace('_', ' ') for n in synset.lemma_names()]
    chained = chain(chained, l)
exit()

nouns = set(chained)
# nouns = sorted(list(set(
#             itertools.chain.from_iterable([n.replace('_', ' ') for n in synset.lemma_names()] for synset in wordnet.all_synsets('n'))
#         )), key=str.casefold)

"""with open('nouns.txt', 'w', encoding='utf-8') as outfile:
    print(*nouns, sep='\n', file=outfile)

from profanity_check import predict, predict_prob

predict(['predict() takes an array and returns a 1 for each string if it is offensive, else 0.'])
# [0]

predict(['fuck you'])
# [1]

predict_prob(['predict_prob() takes an array and returns the probability each string is offensive'])
# [0.08686173]

predict_prob(['go to hell, you scum'])
# [0.7618861]"""
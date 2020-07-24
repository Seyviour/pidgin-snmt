import pprint
pidgin_words = set()

alignment_dict = {}

with open('unique.vcb.pcm', 'r') as f: 
    for line in f: 
        pidgin_words.add(line.strip())

with open('100mostcommon.pcm', 'r') as f: 
    for line in f: 
        pidgin_words.add(line.strip())

with open('lex.f2e', 'r') as f: 
    for line in f: 
        values = line.strip().split(' ')
        if values[1] in pidgin_words and values[1] not in alignment_dict.keys():
            alignment_dict[values[1]] = {'words': [], 'probs': []}
        
        if values[1] in pidgin_words and values[1] in alignment_dict.keys():
            alignment_dict[values[1]]['words'].append(values[1])
            alignment_dict[values[1]]['probs'].append(values[2])


for keyvalue in alignment_dict.keys(): 
    prob_list = alignment_dict[keyvalue]['probs']
    word_list = alignment_dict[keyvalue]['words']

    prob_list, word_list = (list(t) for t in zip(*sorted(zip(prob_list, word_list)))   )

    try: 
        alignment_dict[keyvalue]['probs'] = prob_list[-5:]
        alignment_dict[keyvalue]['words'] = word_list[-5:]
    except: 
        alignment_dict[keyvalue]['probs'] = prob_list[0:]
        alignment_dict[keyvalue]['words'] = word_list[0:]

    alignment_dict[keyvalue]['probs'].reverse()
    alignment_dict[keyvalue]['words'].reverse()
    
with open('alignment-values', 'w') as f: 
     pprint.pprint(alignment_dict, stream=f)

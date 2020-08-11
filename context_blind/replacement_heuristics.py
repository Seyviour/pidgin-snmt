import numpy as np
from nltk.metrics import *
import re
"""
Several methods to perform pre-translation
Abstracted into this file for ease in applying the heuristics, and potentially increase readability.

input to heuristic:  a tokenized line ( a list of tokens), 'alignment-values' for all words in the line

output from heuristic: a list with the replacement heuristic applied to each word

Generating a dictionary at every call is probably expensive, but God no go shame us /\. Mek I finish project first
"""
def soft_max (x): 
    return np.exp(x) /np.sum(np.exp(x), axis = 0)

"""
def heuristic_1 (align_dict, word_list, most_common_words, unique_words ) : 
    for (idx, word) in enumerate(word_list):

        alignment_softs = align_dict[word]['soft']
        alignment_words = align_dict[word]['words']
        
        if (word in most_common_words and word in unique_words) or (word in most_common_words and most_common_words.index(word) < 75) :
            choice = [x for x in range(0, len(alignment_words))]
            chosen = np.random.choice(choice, min(2, len(choice)),  alignment_softs).tolist()

            rep = ""
            rep = [(rep + alignment_words[x] + " ") for x in chosen]
            rep = "".join(p for p in rep)
            rep = rep.strip()
            word_list[idx] = rep 

   return word_list
"""
def heuristic_2 (align_dict, word_list, most_common_words, unique_words, lookup_range = 1 ): 

    most_common_words = most_common_words[0:10]

    check_range = [x for x in range (-lookup_range, lookup_range + 1)]
    
    first_half = [ 2**x for x in range (0, lookup_range + 1)]
    second_half = first_half[0: lookup_range]
    second_half.reverse()
    weights = first_half + second_half
    weights = np.array([weights]).T

    return_list = []

    for (idx, word) in enumerate(word_list):

        if word not in align_dict.keys(): 
            return_list.append(word)
            continue 

        align_words = align_dict[word]['words']
        align_probs = [float(x) for x in align_dict[word]['probs']]
        """
        for i, word in enumerate(align_words): 
            if word in most_common_words: 
                align_probs[i] = align_probs[i]/2
        #print(align_probs)
        """
        # implement edge case where look_left or look_right is not possible
        
        replace_probs = np.zeros((2 * lookup_range + 1, len(align_words)))
        replace_probs[lookup_range] = align_probs

        for i in check_range: 

            try: 
                check_idx = idx + i
                word_list[check_idx] = word_list[check_idx]
            except: 
                continue

            if word_list[check_idx] in align_dict.keys():
                check_key = word_list[check_idx]
                check_words = align_dict[check_key]['words']
                check_probs = align_dict[check_key]['probs']

                for (word_prob, word) in (zip(check_words, check_probs)): 
                    if word in align_words: 

                        align_word_idx = align_words.index(word)

                        replace_probs [ (lookup_range + i ), align_word_idx ] = word_prob

        #weights = np.array([[1], [2], [4], [2], [1]])
        
        support_count = (replace_probs > 0).astype(int)
        support_count = np.sum( support_count, axis = 0)
        support_nerf = np.power(support_count, 0.5)


        decision_probs = np.sum( replace_probs *  weights , axis = 0)
        decision_probs = soft_max ( np.multiply (decision_probs, 1/support_count) ).tolist()
        sort_index = np.argsort(decision_probs)[::-1]

        max_prob = max(decision_probs)
        rep_token = align_words[sort_index[0]]

        idx = 0
        #while not re.match (r'[A-Za-z]', rep_token):
        #   idx = idx + 1 
        #    rep_token = align_words[sort_index[idx]]

        #print(rep_token)

        for sort_idx in sort_index[1:]: 
            count = 1
            if  decision_probs[sort_idx] >= (max_prob/1.15) and edit_distance(align_words[sort_index[0]], align_words[sort_idx]) >= 3 and count <= 1: 
                
                #
                
                #if decision_probs[sort_idx] > 1.5 * decision_probs[sort_idx + 1]:
                rep_token = rep_token + " " + align_words[sort_idx]
                count += 1

                #print (rep_token)
            else: 
                break
        
        rep_token = rep_token.strip()
        #max_index = decision_probs.index(max(decision_probs))
        #rep_token = align_words[max_index]
        #decision_probs[max_index] = 0

        #max_index = decision_probs.index(max(decision_probs))

        #rep_token = align_words[max_index]
        #decision_probs(max_index) = 0

        return_list.append(rep_token)

    return return_list

def heuristic_3 (align_dict, word_list, most_common_words, rep_candidates, lookup_range = 1 ): 
    
    check_range = [x for x in range (-lookup_range, lookup_range + 1)]
    
    first_half = [ 2**x for x in range (0, lookup_range + 1) ]
    second_half = first_half[0: lookup_range]
    second_half.reverse()
    weights = first_half + second_half
    weights = np.array([weights]).T

    return_list = []

    for (idx, word) in enumerate(word_list):

        if word not in rep_candidates or word not in align_dict.keys(): 
            return_list.append(word)
            continue 

        

        align_words = align_dict[word]['words']
        align_probs = [float(x) for x in align_dict[word]['probs']]
        
        for i, word in enumerate(align_words): 
            if word in most_common_words: 
                align_probs[i] = align_probs[i]/2
    
        # implement edge case where look_left or look_right is not possible
        
        replace_probs = np.zeros((2 * lookup_range + 1, len(align_words)))
        replace_probs[lookup_range] = align_probs

        for i in check_range: 
            try: 
                check_idx = idx + i
                word_list[check_idx] = word_list[check_idx]
            except: 
                continue

            if word_list[check_idx] in align_dict.keys():
                check_key = word_list[check_idx]
                check_words = align_dict[check_key]['words']
                check_probs = align_dict[check_key]['probs']

                for (word_prob, word) in (zip(check_words, check_probs)): 
                    if word in align_words: 
                        align_word_idx = align_words.index(word)
                        replace_probs [ (lookup_range + i ), align_word_idx ] = word_prob
        
        support_count = (replace_probs > 0).astype(int)
        support_count = np.sum( support_count, axis = 0)
        support_nerf = np.power(support_count, 0.5)


        decision_probs = np.sum( replace_probs *  weights , axis = 0)
        decision_probs = soft_max ( np.multiply (decision_probs, 1/support_count) ).tolist()
        sort_index = np.argsort(decision_probs)[::-1]

        max_prob = max(decision_probs)
        rep_token = align_words[sort_index[0]]

        idx = 0
        count = 1
        for sort_idx in sort_index[1:]: 
            
            if  decision_probs[sort_idx] >= (max_prob/1.15) and edit_distance(align_words[sort_index[sort_idx-1]], align_words[sort_idx]) >= 3 and count <= 1: 
                
                rep_token = rep_token + " " + align_words[sort_idx]
                count += 1
                
            else: 
                break
        
        rep_token = rep_token.strip()
        return_list.append(rep_token)

    return return_list




if __name__ == "__main__":
    pass



            












# calculating probabilities:  soft_max (2*prob(word_list) + prob(word_list +- 1) + 0.5*prob(word_list +-2))
# decision factor: If  prob(word) > prob(highest_word)/decision_factor: include word
# if word is in 2 left of list or 2 right of list, don't include word, include second word
# 
        
if __name__ == "__main__":
    pass

"""
Robot Programmable, multifunctional manipulator designed to move materials, paths, tools, etc through variable programmed motions to perform
a variety of tasks 

What makes a Machine a Robot

    Programmability is the defining feature of a robot

    Capacity to perform a variety of tasks (depending on how it's been programmed)

    Ability to move in a variety of ways to carry out its task

Classification of Robots
** according to Japanese Industrial Robots Association **


    1. Manual Robots:           |     Multiple degrees of freedom, but all actions are performed under direct control of a human operator. Lack Autonomy
    2. Fixed sequence robots:   | Repeat actions (the actions are in a fixed sequence). No need for operator control. Have Autonomy
    3. Variable sequence robots:|  Sequence of actions can be reprogrammed easily. Can be easily programmed to perform new tasks
    4. Numerical robots:        |   Controlled via numerical information
    5. Playback robots.
    6. Intelligent Robots


"""

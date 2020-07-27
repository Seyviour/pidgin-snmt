import ast
import nltk


most_common_pidgin = list()
unique_pidgin = set()
alignment_dict = dict()

with open('alignment-values', 'r') as f: 
    f_contents = f.read()
    alignment_dict = ast.literal_eval(f_contents)

with open ('100mostcommon.pcm', 'r') as f: 
    for line in f: 
        most_common_pidgin.append(line.strip())

with open ('unique_voc.pcm' , 'r') as f: 
    for line in f: 
        unique_pidgin.add(line.strip())


def do_word_replacement (file_name, new_file_name): 
    with open (file_name, 'r') as f: 
        with open(new_file_name, 'w') as e: 
            for line in f:

                word_list =  line.strip().split(" ")
                #print(word_list)
                for (idx, word) in enumerate(word_list):
                    #print(idx, word)
                    if word in alignment_dict.keys():
                       # print(word)

                        alignment_words = alignment_dict[word]['words']
                        moses_translation = alignment_dict[word]['moses_trans']

                        if (word in unique_pidgin) or (word in most_common_pidgin and most_common_pidgin.index(word) < 30) :
                            #print(most_common_pidgin.index(word))
                            #print(word)
                            if len(moses_translation.strip().split(" ")) == 2: 
                                word_list[idx] = moses_translation

                            else:
                                #word_list[idx] = alignment_words[0] + " " + alignment_words[1] + " " + alignment_words[2]
                                x = len(alignment_words) - 1
                                word_list[idx] = " ".join(alignment_words[0: min(3,x)])
                                
                        elif word in most_common_pidgin: 
                            if word == alignment_words[0]:
                                word_list[idx] = word
                                print(word_list)

                            elif  word != alignment_words[0] :
                                if len(moses_translation.strip().split(" ")) == 1: 
                                    word_list[idx] = alignment_words[0]
                                elif len(moses_translation.strip().split(" ")) == 2: 
                                    word_list[idx] = moses_translation
                                else:
                                    x = len(alignment_words) - 1 
                                    word_list[idx] = " ".join(alignment_words[0: min(3, x)])
                        
            
                    
                
                e.write(" ".join(word_list) + '\n')

do_word_replacement('JW300train.pcm-en.clean.pcm', 'snmt.train.pcm')
do_word_replacement('JW300tune.pcm-en.low.pcm', 'snmt.tune.pcm')
do_word_replacement('test.pcm-en.low.pcm', 'snmt.test.pcm')

do_word_replacement('testfile', 'snmt.testfile')                                                                                                                                                                                                                                                                                         
import re
import sys
import os
import argparse
import nltk
import pandas as pd

parser = argparse.ArgumentParser()

corpus_l1 = sys.argv[1]
corpus_l2 = sys.argv[2]
testfile = sys.argv[3]

dir = os.getcwd()
scripture_finder = re.compile(r'(?:\d|I{1,3})?\s*\w{2,}\s*\.?\s*\d{1,}\s*\:\s*\d{1,}\s*-?,?\s*\d{0,2}(?:,\d{0,2}){0,2}')

def get_scripture_finder(): 
	return scripture_finder

test_set = set()
with open (testfile, 'r') as f: 
	for line in f: 
		test_set.add(line.strip())


def return_from_first_word ( in_line ):

	in_line = in_line.strip()
	#line_list = re.split(r'(\W+)', in_line)
	if re.search(r'[A-Za-z]+', in_line):

		line_list = nltk.word_tokenize(in_line)
		if len(line_list) == 1: 
			return (in_line)

		else: 
			for i in range (0, len(line_list)-1): 
				if re.match (r'[A-Za-z]', line_list[i]): 
					return_string = " ".join(line_list[i:])
					return return_string
					break

	else: 
		return ''
	     	
def remove_test_sentences(): 

		prev_e_line = ''
		prev_f_line = ''
		prev_check_line = ''

		for (i, (f_line, e_line)) in enumerate(zip(f, e)) : 
			f_line = f_line.strip()
			e_line = e_line.strip() 


			if (i == 0): # intitialize previous lines. Reading through the code should reveal the reason for this
				prev_check_line = f_line	
				prev_e_line = '' + scripture_finder.sub (' scrptr ' , e_line , count = 0)
				prev_f_line = '' + scripture_finder.sub (' scrptr ' , f_line , count = 0)
				continue

			# match and replace scripture references in current line, if there are any
			curr_check_line = f_line
			curr_e_line = '' + scripture_finder.sub (' scrptr ', e_line, count = 0) 
			curr_f_line = '' + scripture_finder.sub (' scrptr ', f_line, count = 0)

			# match and replace scripture references that occur across multiple lines - a quirk of the JW300 dataset
			if scripture_finder.search ( prev_e_line + curr_e_line ): 
				prev_e_line, curr_e_line = scripture_finder.split( prev_e_line + curr_e_line)
				prev_e_line = prev_e_line + ' scrptr'

			if scripture_finder.search ( prev_f_line + curr_f_line): 
				prev_f_line, curr_f_line = scripture_finder.split( prev_f_line + curr_f_line )
				prev_f_line = prev_f_line + ' scrptr'

			# every sentence should start with a word 
			prev_e_line = return_from_first_word( prev_e_line )
			prev_f_line = return_from_first_word( prev_f_line )

			# filter out empty sentences
			if not ( prev_e_line == '' or prev_f_line == '' or prev_e_line == None or prev_f_line == None): 

				if prev_check_line in test_set: 
					f_test.write(prev_f_line + '\n')
					e_test.write(prev_e_line + '\n')
				
				else: 
					f_train.write(prev_f_line + '\n')
					e_train.write(prev_e_line + '\n')

			prev_e_line = curr_e_line
			prev_f_line =  curr_f_line
			prev_check_line = curr_check_line

		if not ( prev_e_line == '' or prev_f_line == ''): 

			if (prev_check_line in test_set): 
				f_test.write(prev_f_line + '\n')
				e_test.write(prev_e_line + '\n')
			else: 
				f_train.write(prev_f_line + '\n')
				e_train.write(prev_e_line + '\n')

## There's a lot of abstractions missing from here right now but I need to finish my project. God no go shame us |\

## Remove duplicate translations from the test set because they may affect BLEU score computation

def drop_duplicates(file1, file2): 
	with open (file1, 'r') as en_file,\
		open (file2, 'r') as pcm_file:

		en = en_file.readlines()
		pcm = pcm_file.readlines()

		en = [x.strip() for x in en]
		pcm = [x.strip() for x in pcm]

		df = pd.DataFrame(zip(en, pcm), columns=['en_sentence', 'pcm_sentence'])
		df = df.drop_duplicates()

	with open (file1, 'w') as en_file,\
		open (file2, 'w') as pcm_file:

		for index, row in df.iterrows():
			en_file.write (str(row["en_sentence"]) + '\n')
			pcm_file.write (str(row["pcm_sentence"]) + '\n')


if __name__ == "__main__": 

	test_l1 = 'test.pcm-en.en'
	test_l2 = 'test.pcm-en.pcm'
	train_l1 = 'train_tune.pcm-en.en'
	train_l2 = 'train_tune.pcm-en.pcm'
	
	with open(corpus_l1, 'r') as f,\
		open(corpus_l2, 'r') as e,\
		open(test_l1, 'w') as f_test,\
		open(test_l2, 'w') as e_test,\
		open(train_l1, 'w') as f_train,\
		open(train_l2, 'w') as e_train: 

		remove_test_sentences()

	drop_duplicates (test_l1, test_l2 )
	drop_duplicates (train_l1, train_l2)
import random

random.seed(12)

pcm_file = 'train_tune.pcm-en.pcm'
en_file = 'train_tune.pcm-en.en'
en_train_file = 'train.pcm-en.en'
en_tune_file = 'tune.pcm-en.en'
pcm_train_file = 'train.pcm-en.pcm'
pcm_tune_file = 'tune.pcm-en.pcm'



with open(en_file, 'r') as en,\
	open(pcm_file, 'r') as pcm,\
     	open(en_train_file, 'w') as en_train,\
     	open(en_tune_file, 'w') as en_tune,\
     	open(pcm_train_file, 'w') as pcm_train,\
     	open(pcm_tune_file, 'w') as pcm_tune: 
     
		en_list = en.readlines()
		pcm_list = pcm.readlines()

		idxs = random.sample(range(0, len(en_list)), 1000)
	
		for i in range (0, len(en_list)): 
			if i in idxs: 
				en_tune.write(en_list[i])
				pcm_tune.write(pcm_list[i])		
			else: 
				en_train.write(en_list[i])
				pcm_train.write(pcm_list[i])

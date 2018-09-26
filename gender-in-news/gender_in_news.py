#!/usr/bin/env python3.6
# coding=<utf-8>
from __future__ import division
import pandas as pd 
import os
import zipfile

import glob
import nltk
from string import punctuation
import sys


def gender_check(pandas_content, publication_name):
    
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

    #Two lists  of words that are used when a man or woman is present, based on Danielle Sucher's https://github.com/DanielleSucher/Jailbreak-the-Patriarchy
    male_words=set(['guy','spokesman','chairman',"men's",'men','him',"he's",'his','boy','boyfriend','boyfriends','boys','brother','brothers','dad','dads','dude','father','fathers','fiance','gentleman','gentlemen','god','grandfather','grandpa','grandson','groom','he','himself','husband','husbands','king','male','man','mr','nephew','nephews','priest','prince','son','sons','uncle','uncles','waiter','widower','widowers'])
    female_words=set(['heroine','spokeswoman','chairwoman',"women's",'actress','women',"she's",'her','aunt','aunts','bride','daughter','daughters','female','fiancee','girl','girlfriend','girlfriends','girls','goddess','granddaughter','grandma','grandmother','herself','ladies','lady','lady','mom','moms','mother','mothers','mrs','ms','niece','nieces','priestess','princess','queens','she','sister','sisters','waitress','widow','widows','wife','wives','woman'])

    def gender_the_sentence(sentence_words):
        mw_length=len(male_words.intersection(sentence_words))
        fw_length=len(female_words.intersection(sentence_words))

        if mw_length>0 and fw_length==0:
            gender='male'
        elif mw_length==0 and fw_length>0: 
            gender='female'
        elif mw_length>0 and fw_length>0: 
            gender='both'
        else:
            gender='none'
        return gender

    def is_it_proper(word):
            if word[0]==word[0].upper():
                case='upper'
            else:
                case='lower'
            
            word_lower=word.lower()
            try:
                proper_nouns[word_lower][case] = proper_nouns[word_lower].get(case,0)+1
            except Exception:
                #This is triggered when the word hasn't been seen yet
                proper_nouns[word_lower]= {case:1}

    def increment_gender(sentence_words,gender):
        sentence_counter[gender]+=1
        word_counter[gender]+=len(sentence_words)
        for word in sentence_words:
            word_freq[gender][word]=word_freq[gender].get(word,0)+1

    ############################################
    sexes=['male','female','none','both']
    sentence_counter={sex:0 for sex in sexes}
    word_counter={sex:0 for sex in sexes}
    word_freq={sex:{} for sex in sexes}
    proper_nouns={}

    # file_list=glob.glob('singles/*.txt')
    #file_list=glob.glob(datapath+'/*.txt')
    content_list = pandas_content #efrat
    #content = dataset

    #for file_name in file_list:
    for content in content_list:
        #Open the file
        #text=open(file_name,'rb').read()
        text = content #efrat
        
        #Split into sentences
        sentences=tokenizer.tokenize(text)
        
        for sentence in sentences:
            #word tokenize and strip punctuation
            sentence_words=sentence.split()
            sentence_words=[w.strip(punctuation) for w in sentence_words 
                    if len(w.strip(punctuation))>0]
                
                #figure out how often each word is capitalized
            [is_it_proper(word) for word in sentence_words[1:]]

                #lower case it
            sentence_words=set([w.lower() for w in sentence_words])
                
                #Figure out if there are gendered words in the sentence by computing the length of the intersection of the sets
            gender=gender_the_sentence(sentence_words)

                #Increment some counters
            increment_gender(sentence_words,gender)

    proper_nouns=set([word for word in proper_nouns if  
                      proper_nouns[word].get('upper',0) / 
                      (proper_nouns[word].get('upper',0) + 
                       proper_nouns[word].get('lower',0))>.50])

    common_words=set([w for w in sorted (word_freq['female'],
                                         key=word_freq['female'].get,reverse=True)[:1000]]+[w for w in sorted (word_freq['male'],key=word_freq['male'].get,reverse=True)[:1000]])

    common_words=list(common_words-male_words-female_words-proper_nouns)

    male_percent={word:(word_freq['male'].get(word,0) / word_counter['male']) 
                  / (word_freq['female'].get(word,0) / word_counter['female']+word_freq['male'].get(word,0)/word_counter['male']) for word in common_words}

    filename = publication_name+"_results_summary" 
    print('%.1f%% gendered' % (100*(sentence_counter['male']+sentence_counter['female'])/
                               (sentence_counter['male']+sentence_counter['female']+sentence_counter['both']+sentence_counter['none']))+
                                '\n %s sentences about men.' % sentence_counter['male']+'\n %s sentences about women.' % sentence_counter['female']+
                                '\n %.1f sentences about men for each sentence about women.' % (sentence_counter['male']/sentence_counter['female'])+
                                '\n number of sentences about both %s' % sentence_counter['both']+
                                '\n number of sentences about none %s ' % sentence_counter['none'],file = open(filename, "w"))
    
    print('%.1f%% gendered' % (100*(sentence_counter['male']+sentence_counter['female'])/
                               (sentence_counter['male']+sentence_counter['female']+sentence_counter['both']+sentence_counter['none'])))
    print('%s sentences about men.' % sentence_counter['male'])
    print('%s sentences about women.' % sentence_counter['female'])
    print('%.1f sentences about men for each sentence about women.' % (sentence_counter['male']/sentence_counter['female']))

    header ='Ratio\tMale\tFemale\tWord'
    print('Male words')
    print(header)
    for word in sorted (male_percent,key=male_percent.get,reverse=True)[:50]:
        try:
            ratio=male_percent[word]/(1-male_percent[word])
        except:
            ratio=100
        print('%.1f\t%02d\t%02d\t%s' % (ratio,word_freq['male'].get(word,0),word_freq['female'].get(word,0),word))

    print('\n'*2)
    print('Female words')
    print(header)
    for word in sorted (male_percent,key=male_percent.get,reverse=False)[:50]:
        try:
            ratio=(1-male_percent[word])/male_percent[word]
        except:
            ratio=100
        print('%.1f\t%01d\t%01d\t%s' % (ratio,word_freq['male'].get(word,0),word_freq['female'].get(word,0),word))

    outfile_name='gender.tsv'
    tsv_outfile=open(outfile_name,'w')
    header='percent_male\tmale_count\tfemalecount\tword\n'
    tsv_outfile.write(header)
    for word in common_words:
        row = '%.2f\t%01d\t%01d\t%s\n' % (100*male_percent[word],word_freq['male'].get(word,0),word_freq['female'].get(word,0),word)
        tsv_outfile.write(row)
    tsv_outfile.close()

    all_words=[w for w in word_freq['none']]+[w for w in word_freq['both']]+[w for w in word_freq['male']]+[w for w in word_freq['female']]
    all_words={w:(word_freq['male'].get(w,0)+word_freq['female'].get(w,0)+word_freq['both'].get(w,0)+word_freq['none'].get(w,0)) for w in set(all_words)}

    print('word\tMale\tFemale')
    for word in sorted (all_words,key=all_words.get,reverse=True)[:100]:
        print('%s\t%.1f%%\t%.1f%%' % (word,100*word_freq['male'].get(word,0)/sentence_counter['male'],100*word_freq['female'].get(word,0)/sentence_counter['female']))


#path = "/Users/tempuser/Downloads/articles/"
#### Algorithm
## 1. Get filename form cmd
# read file names form arg

## 2. Open file in pandas
## 3. Remove not needed cloumns
## 4. get  publishers list
## 5. foreach publisher in list 
## 5.1 write to file publisher stats (name, #ofpublications) 
## 5.2 send content to "gender" (groupby param)

if len(sys.argv) == 2:
    publication_data = sys.argv[1]
else:
    sys.exit('Error! should have parameter')


df = pd.read_csv(publication_data)

g = df.groupby("publication")

publication_name = g.groups.keys()

for name in publication_name:
    print(name)
    dirname = name.replace(' ', '')
    
    content = g.get_group(name)["content"].tolist()
    num_publications = len(content)
    #ftxt = open(path+"singles/"+name+"_publication_detailes"+".txt","w+")
    ftxt = open(name+"_publication_detailes"+".txt","w+")
    ftxt.write("number of publications: "+str(num_publications))
    ftxt.close()

    gender_check(content, dirname)

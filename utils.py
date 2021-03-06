# encoding:utf-8

import re
import nltk
import pymorphy2

morph = pymorphy2.MorphAnalyzer()

def filter_noise(text):
    text = re.sub('<pre>.*?</pre>',' ', text, flags=re.DOTALL)
    text = re.sub('<code>.*?</code>',' ', text, flags=re.DOTALL)
    text = re.sub('<[^<]+?>', ' ', text, flags=re.DOTALL) 
    text = re.sub('(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z]+[A-Za-z0-9]+)', ' ', text, flags=re.DOTALL)             
    text = re.sub('(https|http)?:\/\/.*', '', text)
    return text

def process_text(text, extended_filter=False, word_len_threshold=2):
    global morph

    def process(filter, token, word_len_threshold):
        global morph

        p = morph.parse(token)[0]
        if len(p.normal_form) < word_len_threshold:
            return None
        
        # http://pymorphy2.readthedocs.io/en/latest/user/grammemes.html
        if any(tag in str(p.tag) for tag in ['PNCT', 'NUMB', 'UNKN']): # ['LATN', 'PNCT', 'NUMB', 'UNKN']
            return None
        # http://pymorphy2.readthedocs.io/en/latest/user/grammemes.html
        if str(p.tag.POS) not in filter:
            return  str(p.normal_form)  

    otput_data = ""
    if extended_filter:
        filter = ['PREP']
    else:    
        filter = ['NPRO', 'PREP', 'PRED', 'CONJ', 'PRCL', 'INTJ']

    text = filter_noise(text)
    text = text.lower()

    sent_text = nltk.sent_tokenize(text)
    for sentence in sent_text:
        tokenized_text = nltk.word_tokenize(sentence)
        for token in tokenized_text:
            
            token = token.replace('.', ' ')
            token = token.replace('/', ' ')

            for sub_token in token.split():
                processed = process(filter, sub_token, word_len_threshold)
                if processed is not None:
                    otput_data += " " + processed
        
    return otput_data

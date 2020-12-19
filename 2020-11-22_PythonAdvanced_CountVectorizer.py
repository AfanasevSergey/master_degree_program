#!/usr/bin/env python
# coding: utf-8

# In[39]:


class CountVectorizer:
    
    '''
    The class 'CountVectorizer' contains methods for converting text to a vector representation:
    1) .fit - builds the "token for indexing" dictionary from the input corpus;
    2) .transform - converts a new corpus based on the saved dictionary;
    3) .fit_transform − fit and transform on the same corpus.
    '''
    
    def __init__(self, ngram_size):
        self.__ngram_size = ngram_size
        self._dictionary = {}

        
    # .fit - builds the "token for indexing" dictionary from the input corpus
    def fit(self, corpus):
        self._dictionary = {}
        
        for sequence in corpus:
            for i in range(len(sequence) - self.__ngram_size + 1):
                self._dictionary[sequence[i:i + self.__ngram_size]] = None
        
        for idx, token in enumerate(sorted(self._dictionary)):
            self._dictionary[token] = idx

            
    # .transform - converts a new corpus based on the saved dictionary
    def transform(self, corpus):
        transform_corpus = []
      
        for sequence in corpus:
            token_cnt = [0] * len(self._dictionary)
            for i in range(len(sequence) - self.__ngram_size + 1):
                idx = self._dictionary.get(sequence[i:i + self.__ngram_size])
                if idx is not None:
                    token_cnt[idx] += 1
            transform_corpus.append(token_cnt)
        
        return transform_corpus

    
    # .fit_transform − fit and transform on the same corpus
    def fit_transform(self, corpus):
        self.fit(corpus)
        return self.transform(corpus)


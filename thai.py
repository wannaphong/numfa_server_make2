# -*- coding: utf-8 -*-
from pythainlp.word_vector import thai2vec
from pythainlp.tokenize import word_tokenize
from sklearn.metrics.pairwise import cosine_similarity
from chatterbot.comparisons import Comparator
import numpy as np
model=thai2vec.get_model()
def sentence_vectorizer(ss,dim=300,use_mean=True):
    s = word_tokenize(ss)
    vec = np.zeros((1,dim))
    for word in s:
        if word in model.wv.index2word:
            vec+= model.wv.word_vec(word)
        else: pass
    if use_mean: vec /= len(s)
    return vec
def sentence_similarity(s1,s2):
    return cosine_similarity(sentence_vectorizer(str(s1)),sentence_vectorizer(str(s2)))
class Thai(Comparator):
    """
    Compare two statements based on thai2vec using word2vec
	
	by wannaphong
    """

    def compare(self, statement, other_statement):
        return sentence_similarity(statement,other_statement)

thai=Thai()
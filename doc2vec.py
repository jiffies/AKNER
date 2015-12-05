#!-*- coding:utf-8 -*-
import jieba
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence
import logging
from sklearn.metrics import pairwise_distances
import os
import tools
import numpy as np

logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
logging.root.setLevel(level=logging.INFO)

def train():
    model = Word2Vec(LineSentence('corpus.txt'),workers=4,iter=30,min_count=1)
    model.save("word2vec.model")
    return model

def ne2vec(model,ne):
    '''
    输入一个实体，各部分以空格分割
    '''
    parts = ne.split(' ')
    parts = [p for p in parts if not tools.is_other(p)]
    vec = reduce(lambda x,y: x+y,[model[part] for part in parts])
    return vec

def doc2vec(model,fname):
    vecs = []
    with file(fname) as f:
        lines = f.readlines()
        for line in lines:
            line = line.decode('utf-8')
            vecs.append(ne2vec(model,line.strip('\n')))
    result = reduce(lambda x,y: x+y,vecs)/len(vecs)
    return result

def doc_similarity(model,nedocset):
    vec_matrix = [doc2vec(model,doc) for doc in nedocset]
    similarity_matrix = pairwise_distances(vec_matrix,metric='cosine')
    print nedocset
    print similarity_matrix
    return similarity_matrix

def closest_to(similarity_matrix,doc2id,docname):
    maxvalue = similarity_matrix.max()
    for i in xrange(len(similarity_matrix)):
        similarity_matrix[i,i] = maxvalue
    id2doc = {b:a for a,b in doc2id.iteritems()}
    simi = np.min(similarity_matrix[doc2id[docname]])
    fname = id2doc[np.argmin(similarity_matrix[doc2id[docname]])]
    return fname,simi



    

if __name__ == "__main__":
    model = Word2Vec.load('word2vec.model')
    neset = [os.path.join('test/NE',doc) for doc in os.listdir('test/NE/') if doc.endswith('ne')]
    doc2id = {ne:index for index,ne in enumerate(neset)}
    doc_similarity(model,neset)
    #train()

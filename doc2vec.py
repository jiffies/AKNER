#!-*- coding:utf-8 -*-
import jieba
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence
import logging
from sklearn.metrics import pairwise_distances
from sklearn.metrics.pairwise import cosine_similarity
import os
import tools
import numpy as np
import pandas as pd


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
    #parts = [p for p in parts if not tools.is_other(p)]
    #if not parts:
        #return np.array([])
    #vec = reduce(lambda x,y: x+y,[model[part] for part in parts])
    vec = []
    for part in parts:
        try:
            vec.append(model[part])
        except KeyError:
            print "model no token %s" % part
    if vec:
        return reduce(lambda x,y: x+y,vec)
    else:
        return np.array([])

def doc2vec(model,fname):
    '''
    fname是命名实体集合文件
    '''
    vecs = []
    with file(fname) as f:
        lines = f.readlines()
        for line in lines:
            line = line.decode('utf-8')
            v = ne2vec(model,line.strip('\n'))
            if v.any():
                vecs.append(v)
    if vecs:
        result = reduce(lambda x,y: x+y,vecs)/len(vecs)
    else:
        result = np.array([])
    return result

def docset2vecs(model,fname_map_txt):
    vecs = []
    files = []
    for fname,txt in fname_map_txt.iteritems():
        v = doc2vec(model,fname)
        if v.any():
            vecs.append(v)
            files.append(txt)
    print "共 %d个文件" % len(vecs)
    m = pd.DataFrame(vecs)
    m['txt'] = files
    return m

def search(docset_vectors,key_vector,top_n=3,include_self=True):
    start = 0 if include_self else 1
    vec_matrix = docset_vectors[range(0,100)]
    docset_vectors['similarity'] = cosine_similarity(vec_matrix,key_vector).ravel()
    return docset_vectors.sort(columns='similarity',ascending=False)[start:top_n+start]['txt']

def keyword_search(model,docset_vectors,keyword,top_n=3):
    vecs = []
    for t in jieba.cut(keyword):
        vecs.append(model[t])
    keyword_vector = np.sum(vecs,axis=0)
    return search(docset_vectors,keyword_vector,top_n)

def doc_search(model,docset_vectors,docname,top_n=3,include_self=True):
    doc_vector = doc2vec(model,docname)
    return search(docset_vectors,doc_vector,top_n,include_self=include_self)
    


def doc_similarity(model,fname_map_txt):
    df = docset2vecs(model,fname_map_txt)
    vec_matrix = df[range(0,100)]
    similarity_matrix = pairwise_distances(vec_matrix,metric='cosine')
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
    neset = [os.path.join('test/data/txt',doc) for doc in os.listdir('test/data/txt') if doc.endswith('ne')]
    #doc2id = {ne:index for index,ne in enumerate(neset)}
    fname_map_txt = {ne:file(ne.replace('.ne','.txt')).read(100) for ne in neset}
    #print docset2vecs(model,fname_map_txt)
    
    #doc_similarity(model,neset)
    #train()

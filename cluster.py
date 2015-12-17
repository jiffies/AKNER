#!-*- coding:utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import scale
from doc2vec import docset2vecs
import os
from gensim.models import Word2Vec
import pandas as pd

def cluster_img(matrix,n_clusters=7):
    reduced_data = PCA(n_components=2).fit_transform(matrix)
    kmeans = KMeans(init='k-means++', n_clusters=n_clusters, n_init=10)
    kmeans.fit(reduced_data)
    h = .02     # point in the mesh [x_min, m_max]x[y_min, y_max].

# Plot the decision boundary. For that, we will assign a color to each
    x_min, x_max = reduced_data[:, 0].min() - 1, reduced_data[:, 0].max() + 1
    y_min, y_max = reduced_data[:, 1].min() - 1, reduced_data[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

# Obtain labels for each point in mesh. Use last trained model.
    Z = kmeans.predict(np.c_[xx.ravel(), yy.ravel()])

# Put the result into a color plot
    Z = Z.reshape(xx.shape)
    plt.figure(1)
    plt.clf()
    plt.imshow(Z, interpolation='nearest',
               extent=(xx.min(), xx.max(), yy.min(), yy.max()),
               cmap=plt.cm.Paired,
               aspect='auto', origin='lower')

    plt.plot(reduced_data[:, 0], reduced_data[:, 1], 'k.', markersize=2)
# Plot the centroids as a white X
    centroids = kmeans.cluster_centers_
    plt.scatter(centroids[:, 0], centroids[:, 1],
                marker='x', s=169, linewidths=3,
                color='w', zorder=10)
    #plt.title('K-means clustering on the digits dataset (PCA-reduced data)\n'
              #'Centroids are marked with white cross')
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)
    plt.xticks(())
    plt.yticks(())
    plt.show()

if __name__ == '__main__':
    #model = Word2Vec.load('word2vec.model')
    #neset = [os.path.join('test/data/txt',doc) for doc in os.listdir('test/data/txt') if doc.endswith('ne')]
    #doc2id = {ne:index for index,ne in enumerate(neset)}
    #m = docset2vecs(model,neset)

    n_clusters = 7
    model = Word2Vec.load('word2vec.model')
    neset = [os.path.join('test/data/txt',doc) for doc in os.listdir('test/data/txt') if doc.endswith('ne')]
    #doc2id = {ne:index for index,ne in enumerate(neset)}
    fname_map_txt = {ne:file(ne.replace('.ne','.txt')).read() for ne in neset}
    df = docset2vecs(model,fname_map_txt)
    cluster_img(df[range(0,100)],n_clusters=n_clusters)
    k = KMeans(init='k-means++',n_clusters=n_clusters,n_init=10)
    k.fit(df[range(0,100)])
    s=pd.Series(k.labels_).value_counts().sort_index()
    s.plot(kind='bar',rot=0)
    plt.show()
    txt = df['txt']
    for i in range(n_clusters):
        txt[k.labels_==i].to_csv('cluster/%s.txt'%i)

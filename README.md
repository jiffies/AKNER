# AKNER
Algorithmic knowledge named entity recognition for my thesis.

数据:txt文件夹下是所有15000余网页正文
test/data下是随机挑选的200篇
result下是crf++训练先关的train,test,model
dict下是一些词典
cluster是聚类结果，每个类一个文件
corpus.txt是生成的word2vec语料
word2vec.model是词向量模型
template是crf++特征模板
evaluate是crf++显示结果

代码:
1.standoff2crd.py brat到crf++格式转换以及交叉训练
2.preword2vec.py 准备word2vec训练语料
3.doc2vec 生成文本向量
4.cluster.py 聚类实验
5.tools.py 工具函数
6.analysis.py 分析命名实体结果

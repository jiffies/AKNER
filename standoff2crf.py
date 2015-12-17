#! -*- coding:utf-8 -*-
import jieba
import jieba.posseg as pseg
import os
import random
import codecs
import pandas as pd
import csv
import copy

NAMES = ['token','pos','isknowledge','isoj','nertag','predict']

knowledge_dict = codecs.open('dict/算法知识词典.txt','r','utf-8').readlines()
knowledge_dict = [item.strip('\n') for item in knowledge_dict]
oj_dict = codecs.open('dict/oj.txt','r','utf-8').readlines()
oj_dict = [item.strip('\n') for item in oj_dict]


def extract_ann(filename):
    '''
    In [176]: extract_ann('reportb11936.ann')
    Out[176]: {'0': ('7', 'OJ'), '15': ('19', 'KNOWLEDGE')}
    '''
    annmap = {}
    with file(filename) as f:
        for line in f:
            _,info,_ = line.split('\t')
            entity,start,end = info.split(' ')
            annmap[int(start)] = (int(end),entity)
    return annmap

def trans_txt(filename,tagmode=False):
    '''
    从txt文本转换为standoff格式，tagmode默认False代表有标记ann文件
    '''
    curr_pos = 0
    if not tagmode:
        annmap = extract_ann(filename.split('.')[0]+'.ann')
    with file(filename) as f:
        document = f.read()
        #document = document.replace('\r\n','\n')
        #document = document.replace('\t','    ')
        words = pseg.cut(document)
    result = []
    last_tag = None
    last_word = None
    for word,flag in words:
        if word == '\t':
            word = ' '
        if not tagmode:
            if annmap.has_key(curr_pos):
                nertag = 'B-'+annmap[curr_pos][1]
                last_tag = (curr_pos,annmap[curr_pos][0],annmap[curr_pos][1])
            elif last_tag and last_tag[0] < curr_pos < last_tag[1]:
                nertag = 'I-' + last_tag[2]
            else:
                nertag = 'O'
        else:
            nertag='O'
        if last_word == u'。' and word != '\n' and word!=last_word:
            result.append('')
        for item in knowledge_dict:
            if item.find(word)>=0 and len(word)>1:
                inKnowledgeDict = 'Y'
                break;
        else:
            inKnowledgeDict = 'N'

        
        for item in oj_dict:
            if word.find(item)>=0 and len(word)>1:
                inOjDict = 'Y'
                break;
        else:
            inOjDict = 'N'

        if not tagmode:
            result.append('\t'.join([word,flag,inKnowledgeDict,inOjDict,nertag]))
        else:
            result.append('\t'.join([word,flag,inKnowledgeDict,inOjDict,nertag]))

        curr_pos+=len(word)
        last_word = word

    output = '\n'.join(result)
    output = output.replace('\r\n','\n')
    with file(filename.split('.')[0]+'.crf','w') as f:
        f.write(output.encode('utf8'))
    return output

    
def gen_dataset(fold,outputfilename):
    result = []
    for filename in fold:
        result.append(trans_txt(filename))
    final = '\n'.join(result).encode('utf8')
    print "处理了%d个文件,%d行" % (len(result),len(final))
    with file(outputfilename,'w') as f:
        final = final.replace('\r\n','\n')
        f.write(final)


def cross_validation(data,num=5):
    total = len(data)
    sample_num = total/num
    for i in range(num):
        testset = random.sample(data,sample_num)
        trainset = list(set(data).difference(set(testset)))
        #trainset = random.sample(data,total-sample_num)
        #testset = random.sample(data,sample_num)
        
        yield (trainset,testset)


def test(data):
    for index,(train,test) in enumerate(cross_validation(data,num=5)):
        os.system('echo -e "new round\n\n" >> evaluate')
        gen_dataset(train,'result/train'+str(index))
        gen_dataset(test,'result/test'+str(index))
        os.system("crf_learn -t -p8 -f 1 -c 4.0 template result/train%s result/model%s" % (index,index))
        os.system("crf_test -m result/model%s result/test%s > result/result%s"%(index,index,index))
        os.system("perl conlleval.pl -d '\t' < result/result%s 2>&1 | tee -a evaluate"%index)

def train(trainset):
    pass

#def join_ne(x):
    #if x.startswith('B'):

def get_ne(test_result,tagmode=False):
    '''
    从standoff格式的result中提取预测的实体
    '''
    NE = []
    curtag = None
    if not tagmode:
        names = NAMES
    else:
        names = copy.copy(NAMES)
        #names.remove('nertag')
    df = pd.read_csv(test_result,sep='\t',header=None,quoting=csv.QUOTE_NONE,names=names)
    predict = zip(df['token'],df['predict'])
    for token,tag in predict:
        if tag.startswith('B-'):
            if curtag:
                NE.append(curtag)
                curtag = None
            curtag = token
        elif tag.startswith('I-'):
            if curtag:
                curtag += ' '
                curtag += token
        elif tag == 'O':
            if curtag:
                NE.append(curtag)
                curtag = None
        else:
            print 'error'
    output = '\n'.join(NE)

    with file(test_result.split('.')[0]+'.ne','w') as f:
        f.write(output)
    return NE

def generate_ne(docset):
    for doc in docset:
        trans_txt(doc,tagmode=True)
        testname = doc.split('.')[0]+'.crf'
        resultname = doc.split('.')[0]+'.result'
        os.system("crf_test -m result/model1 %s > %s"%(testname,resultname))
        get_ne(resultname,tagmode=True)
        





    


if __name__ == '__main__':
    #data = [os.path.join('test/data/txt',filename) for filename in os.listdir('test/data/txt') if filename.endswith('.txt')]
    #generate_ne(data)
    data = [os.path.join('test/data',filename) for filename in os.listdir('test/data') if filename.endswith('.txt')]
    test(data)
    #print trans_txt('test/reportb09877.txt')
    #result = []
    #for filename in os.listdir('test/data'):
        #if filename.endswith('.txt'):
            #result.append(trans_txt(os.path.join('test/data',filename)))
    #final = '\n'.join(result).encode('utf8')
    #final = final.replace('\r\n','\n')

    #print "处理了%d个文件" % len(result)
    #with file('train.ori','w') as f:
        #final = final.replace('\r\n','\n')
        #f.write(final)
    #linenum = int(os.popen('wc -l train.ori').read().split(' ')[0])
    #tail = linenum*0.2
    #head = linenum - tail
    #os.system("tail -%d train.ori > test.crf" % tail)
    #os.system("head -%d train.ori > train.crf" % head)
    #print "训练集%d行" % head
    #print "测试集%d行" % tail
    

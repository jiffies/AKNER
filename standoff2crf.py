#! -*- coding:utf-8 -*-
import jieba
import jieba.posseg as pseg
import os


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

def trans_txt(filename):
    curr_pos = 0
    annmap = extract_ann(filename.split('.')[0]+'.ann')
    with file(filename) as f:
        document = f.read()
        document = document.replace('\r\n','\n')
        document = document.replace('\t','    ')
        words = pseg.cut(document)
    result = []
    last_tag = None
    last_word = None
    for word,flag in words:
        if annmap.has_key(curr_pos):
            nertag = 'B-'+annmap[curr_pos][1]
            last_tag = (curr_pos,annmap[curr_pos][0],annmap[curr_pos][1])
        elif last_tag and last_tag[0] < curr_pos < last_tag[1]:
            nertag = 'I-' + last_tag[2]
        else:
            nertag = 'O'
        if last_word == u'。' and word != '\n' and word!=last_word:
            result.append('')
        result.append('\t'.join([word,flag,nertag]))

        curr_pos+=len(word)
        last_word = word

    output = '\n'.join(result)
    with file(filename.split('.')[0]+'.crf','w') as f:
        f.write(output.encode('utf8'))
    return output

    


if __name__ == '__main__':
    #print trans_txt('test/reportb11936.txt')
    result = []
    for filename in os.listdir('test/data'):
        if filename.endswith('.txt'):
            result.append(trans_txt(os.path.join('test/data',filename)))
    final = '\n'.join(result).encode('utf8')
    with file('train','w') as f:
        f.write(final)
    

#!-*- coding:utf-8 -*-
import jieba
import os
import tools
import codecs
keyword_dict = codecs.open('dict/C关键字.txt','r','utf-8').readlines()
keyword_dict = [item.strip('\n') for item in keyword_dict]
CUR = os.path.abspath('.')
FOLD = 'txt'
def cut(filename):
    with file(filename,'U') as f:
        doc = f.read()
        seg = jieba.cut(doc)
        segs=[]
        for i in seg:
            if len(i)==1:
                if tools.is_chinese(i):
                    segs.append(i)
            else:
                if i not in keyword_dict and [c for c in i if not tools.is_other(c)]:
                    segs.append(i)

        #seg = [i for i in seg if (len(i)!=1 and tools.is) and i not in keyword_dict and [c for c in i if not tools.is_other(c)]]#去除标点符号
        return ' '.join(segs)

def preprocessing(docset,out='corpus.txt'):
    result = []
    for index,doc in enumerate(docset):
        result.append(cut(doc))
        print "正在处理第%d个文档" % index
    print "处理了%d个文档" % len(result)
    output = '\n'.join(result).encode('utf-8')
    with file(out,'w') as f:
        f.write(output)
    return output


if __name__ == "__main__":
    docset = os.listdir(FOLD)
    docset = [os.path.join(CUR,FOLD,doc) for doc in docset if doc.endswith('.txt')]
    preprocessing(docset)




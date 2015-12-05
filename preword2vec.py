#!-*- coding:utf-8 -*-
import jieba
import os
import tools
CUR = os.path.abspath('.')
FOLD = 'txt'
def cut(filename):
    with file(filename,'U') as f:
        doc = f.read()
        seg = jieba.cut(doc)
        seg = [i for i in seg if not tools.is_other(i)]#去除标点符号
        return ' '.join(seg)

def preprocessing(docset):
    result = []
    for index,doc in enumerate(docset):
        result.append(cut(doc))
        print "正在处理第%d个文档" % index
    print "处理了%d个文档" % len(result)
    output = '\n'.join(result).encode('utf-8')
    with file('corpus.txt','w') as f:
        f.write(output)


if __name__ == "__main__":
    docset = os.listdir(FOLD)
    docset = [os.path.join(CUR,FOLD,doc) for doc in docset if doc.endswith('.txt')]
    preprocessing(docset)




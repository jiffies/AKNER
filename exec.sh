#!/bin/sh
crf_learn -t -p2 -f 3 -c 4.0 template train.crf model
crf_test -m model test.crf > ouput
perl conlleval.pl -d '\t' < ouput 2>&1 | tee evaluate


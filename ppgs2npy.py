import numpy as np
import os
import string
import sys
npy_dir = sys.argv[2]
#'./libri251-ppgs176'
if not os.path.exists(npy_dir):
    os.makedirs(npy_dir)
#filename = 'tts_arctic_test_nnet_output_353_no-log.txt'
filename = sys.argv[1]
f = open(filename)
lines = f.readlines()
n = 0
value = []
def write_to_np(value):
    value =np.array(value)
    npy_file = os.path.join(npy_dir,'%s.npy'%tag)
    np.save(npy_file,value)
    print("save",npy_file)

for line in lines:
    print('begin')
    index = line.find('[')
    end = line.find(']')
    #import pdb;pdb.set_trace()
    #import pdb;pdb.set_trace()
    if index >= 0:
        n = 0;
        tag = line[0:index-1].split()[0]
        #tag = string.join(tag)
        #tag.split('[',']')
        tag = str(tag)
        print("tag",tag)
        #value.append(line[index+1:-1].split());
#        print value
    #end = line.find(']')
    elif end >= 0:
        a = line[:end-1].split()
        print("a",a[0])
        m=[]
        for i in range(len(a)):
            m.append(float(a[i]))
        value.append(m)
        write_to_np(value)
        value=[]
    else :
        print(len(line))

        b=line[:-1].split()
        print('len',len(b))
        #print('b[]',b[0])
        #print("type",type(b[0]))
        n=[]
        for j in range(len(b)):
            n.append(float(b[j]))
        value.append(n)

import os
import sys
import numpy as np
source = sys.argv[1]
x = sys.argv[2]
y = sys.argv[3]
#tar_dir = sys.argv[2]
#if not os.path.exists(tar_dir):
#    os.makedirs(tar_dir)
a = open(source)
for line in a.readlines():
    #print line
    print('===========next=============')
    index = line.find('[')
    end = line.find(']')
    if (index >= 0)&(end>0):
        n = 0;
        tag = line[0:index-1].split()[0]
        #tag = str(tag)
        name = tag[:4]
        #tag = filter(str.isalpha, tag)
        print('name',name)
        #tar_path = os.path.join(tar_dir, name)
        #print("tar_path", tar_path)
        c = line[index+1:end-1].split()
        #q = []
        print(c)
        #for i in range(len(c)):
        #    q.append(float(c[i]))

        #print('q',q)
        os.system('echo %s>>%s'%(name,y))
        os.system('echo %s>>%s'%(c, x))

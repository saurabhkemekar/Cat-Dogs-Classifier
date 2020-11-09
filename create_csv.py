import os
import numpy as np


path = os.getcwd()
path = path + '/dogs-vs-cats/train/'

list = os.listdir(path)
labels = []
for i in list:
    if i[:3] == 'cat':
        labels.append([i,0])
    else:
        labels.append([i,1])


np.savetxt('train_label.csv',labels,delimiter=',',fmt = "%s")

import os
import numpy as np
import pandas as pd
from os.path import isfile, join, isdir
from sklearn.preprocessing import Imputer

#myPath = './'
myPath = '../Outputs'

subDirectories = [f for f in os.listdir(myPath) if isdir(join(myPath, f)) and f[0] != '.']
subDirectories.sort()

currentFeatures = []

'''
def numpy_fillna(data):
    # Get lengths of each row of data
    lens = np.array([len(i) for i in data])

    # Mask of valid places in each row
    mask = np.arange(lens.max()) < lens[:,None]

    # Setup output array and put elements from data into masked positions
    out = np.full(mask.shape, fill_value=np.nan, dtype=data.dtype)
    out[mask] = np.concatenate(data)
    return out
'''

for dir in subDirectories:
    print(dir)
    filesDegrees = [f for f in os.listdir('../Outputs/'+dir) if isfile(join('../Outputs/'+dir, f)) if "degrees" in f]
    filesDegrees.sort()

    filesCloseness = [f for f in os.listdir('../Outputs/'+dir) if isfile(join('../Outputs/'+dir, f)) if "closeness" in f]
    filesCloseness.sort()

    for counter in range(len(filesDegrees)):
        print(counter)
        degrees = []
        with open('../Outputs/'+dir+'/'+filesDegrees[counter], "r") as f:
            for line in f:
                line = [int(i) for i in line[:-1].split(',')]
                degrees.append(line)

        closeness = []
        with open('../Outputs/'+dir+'/'+filesCloseness[counter], "r") as f:
            for line in f:
                line = [float(i) for i in line[:-1].split(',')]
                closeness.append(line)

        histograms = []
        
        for x in range(len(degrees)):
            indexList = []
            for i in list(set(degrees[x])):
                indexes = [z for z,j in enumerate(degrees[x]) if j==i]
                indexList.append(indexes)

            for i in indexList:
                sums = 0.
                for j in i:
                    sums += closeness[x][j]
                histograms.append(sums)

        currentFeatures.append(histograms)

        '''
        if not currentFeatures:
            print('vazio')
            currentFeatures.append(histograms)

        else:
            lengthEarly = len(currentFeatures[0])
            lengthCurrent = len(histograms)

            if lengthEarly > lengthCurrent:
                print('if')
                histograms.extend([np.nan]*(lengthEarly-lengthCurrent))
                currentFeatures.append(histograms)
            elif lengthEarly < lengthCurrent:
                print('elif')
                for i in currentFeatures:
                    i.extend([np.nan]*(lengthCurrent-lengthEarly))
                    currentFeatures.append(histograms)
            else:
                print('else')
                currentFeatures.append(histograms)
        '''

'''
max_len = np.max([len(a) for a in currentFeatures])
currentFeatures = np.asarray([np.pad(a, (0, max_len - len(a)), 'constant', constant_values=np.nan) for a in currentFeatures])
'''

df = pd.DataFrame(currentFeatures,dtype=float)
currentFeatures = df.values

#filling nans
imputer = Imputer(missing_values = 'NaN', strategy = 'mean', axis=1)
imputer.fit(currentFeatures)
currentFeatures = imputer.transform(currentFeatures)

#hist2 = np.array(currentFeatures)
np.save('histogramsMedia2',currentFeatures)
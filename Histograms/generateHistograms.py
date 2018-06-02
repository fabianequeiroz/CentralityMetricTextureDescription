import os
import numpy as np
from os.path import isfile, join, isdir

myPath = './'

subDirectories = [f for f in os.listdir(myPath) if isdir(join(myPath, f)) and f[0] != '.']
subDirectories.sort()

histograms = []

count = 0

for dir in subDirectories:
    print(dir)
    filesDegrees = [f for f in os.listdir(dir) if isfile(join(dir, f)) if "degrees" in f]
    filesDegrees.sort()

    filesCloseness = [f for f in os.listdir(dir) if isfile(join(dir, f)) if "closeness" in f]
    filesCloseness.sort()

    for counter in range(len(filesDegrees)):
        print(counter)
        degrees = []
        with open(dir+'/'+filesDegrees[counter], "r") as f:
            for line in f:
                line = [int(i) for i in line[:-1].split(',')]
                degrees.extend(line)

        
        closeness = []
        with open(dir+'/'+filesCloseness[counter], "r") as f:
            for line in f:
                line = [float(i) for i in line[:-1].split(',')]
                closeness.extend(line)

        indexList = []

        for i in list(set(degrees)):
            indexes = [z for z,j in enumerate(degrees) if j==i]
            indexList.append(indexes)

            '''
            for j in range(len(degrees)):
                if i == degrees[j]:
                    indexes.append(j)
            indexList.append(indexes)
            '''

        histogram = []

        for i in indexList:
            sums = 0.
            for j in i:
                sums += closeness[j]
            histogram.append(sums)

        if count == 0:
            histograms.append(histogram)
            count += 1
        else:
            lengthEarly = len(histograms[0])
            lengthCurrent = len(histogram)

            if lengthEarly > lengthCurrent:
                histogram.extend([np.nan]*(lengthEarly-lengthCurrent))
                histograms.append(histogram)
            elif lengthEarly < lengthCurrent:
                for i in histograms:
                    i.extend([np.nan]*(lengthCurrent-lengthEarly))
                histograms.append(histogram)
            else:
                histograms.append(histogram)

        #print(histograms,'\n\n')

hist2 = np.array(histograms)
np.save('histograms',hist2)
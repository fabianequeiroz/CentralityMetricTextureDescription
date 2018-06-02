import os
import numpy as np
import pandas as pd
from os.path import isfile, join, isdir
from sklearn.preprocessing import Imputer, MinMaxScaler

myPath = './'

subDirectories = [f for f in os.listdir(myPath) if isdir(join(myPath, f)) and f[0] != '.']
subDirectories.sort()

currentFeatures = []

imputer = Imputer(missing_values = 'NaN', strategy = 'mean', axis=1)

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
                degrees.append(line)

        closeness = []
        with open(dir+'/'+filesCloseness[counter], "r") as f:
            for line in f:
                line = [float(i) for i in line[:-1].split(',')]
                closeness.append(line)

        histograms = []
        oneline_histograms = []

        for x in range(len(degrees)):
            indexList = []
            for i in list(set(degrees[x])):
                indexes = [z for z,j in enumerate(degrees[x]) if j==i]
                indexList.append(indexes)

            histogram = []

            for i in indexList:
                sums = 0.
                for j in i:
                    sums += closeness[x][j]
                histogram.append(sums)

            if not histograms:
                histograms.append(histogram)

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
            
            if (len(histograms) == 6):
                df = pd.DataFrame(histograms)
                np_histograms = df.values
                np_histograms = imputer.fit_transform(np_histograms)

                for i in np_histograms:
                    oneline_histograms.extend(i)
                histograms = []

        currentFeatures.append(oneline_histograms)
            
'''
        #filling nans
        imputer = Imputer(missing_values = 'NaN', strategy = 'mean', axis=1)
        imputer.fit(histograms)
        filled_histograms = imputer.transform(histograms)

        oneline_histograms = []
        for i in filled_histograms:
            oneline_histograms.extend(i)

        currentFeatures.append(oneline_histograms)
'''

hist2 = np.array(currentFeatures)
min_max_scaler =  MinMaxScaler()
hist2 = min_max_scaler.fit_transform(hist2)
np.save('histogramsCorreto',hist2)
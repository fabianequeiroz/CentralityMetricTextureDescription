import os
from math import sqrt
from PIL import Image
import numpy
from matplotlib import pyplot as plt
import time
from graph_tool import Graph
from graph_tool import centrality


def selectDirectory(file_path):
    imgList = []

    for file in os.listdir(file_path):
        if file.endswith(".png"):
            imgList.append(file_path + "/" + file)

    return imgList


def generateEmptyGraph(width, height):
    graph = Graph()
    graph.add_vertex(width * height)

    pos = graph.new_vertex_property("vector<double>")

    for x in range(0, width):
        for y in range(0, height):
            pos[graph.vertex((x * width) + (y))] = (x, y)

    graph.vertex_properties["position"] = pos
    return graph


def generateGraph(graph, img, width, height, radius, threshold):
    r = sqrt(radius)

    edge_weights = graph.new_edge_property('int')

    for x in range(0, width):
        for y in range(0, height):
            for i in range(int(x - r), int(x + r) + 1):
                for j in range(int(y - r), int(y + r) + 1):
                    if (i >= 0 and i < width and j >= 0 and j < height and (i != x or j != y)):
                        weightVertex = int(img[x][y]) - int(img[i][j])
                        d = float((x - i) ** 2 + (y - j) ** 2)
                        if (weightVertex <= threshold and weightVertex > 0 and d <= radius):
                            edge = graph.add_edge(graph.vertex((x * width) + (y)), graph.vertex((i * width) + (j)))
                            edge_weights[edge] = weightVertex
    graph.edge_properties["weight"] = edge_weights

    return graph


def mudaValor(x):
    x = 2


if __name__ == "__main__":
    maxRadius = 10
    startingThreshold = 10
    x = 4
    thresholdIncrement = 60
    finalThreshold = startingThreshold + x * thresholdIncrement

    betDict = dict()

    imgList = selectDirectory('Datasets/Brodatz')
    # /KTHTIPS2part2
    output_directory = 'Outputs/Teste'
    # /KTHTIPS2/Closeness/

    for file in imgList:

        img = Image.open(file)
        img = img.convert('L')
        width, height = img.size
        imgArray = numpy.array(img)
        emptyGraph = generateEmptyGraph(width, height)

        fileTime = open(
            output_directory + "/close_" + str(maxRadius) + "_" + str(thresholdIncrement) + "_" + str(x) + "_" +
            file.split('/')[-1] + '.txt', 'a')
        fileTime.write('radius, threshold, execution time\n')

        for r in range(1, maxRadius + 1):
            for t in range(startingThreshold, finalThreshold + 1, thresholdIncrement):
                print("Generating graph: radius = " + str(r) + " threshold = " + str(t))

                startTime = time.time()

                graph = generateGraph(Graph(emptyGraph), imgArray, width, height, r, t)

                # ,weight=graph.ep.weight
                closeness_vp = centrality.closeness(graph, weight=graph.ep.weight, harmonic=False)

                text = (str(r) + ',' + str(t) + ',' + str(time.time() - startTime) + '\n')

                fileTime.write(text)
                fileTime.flush()

                betDict[str(r) + " " + str(t)] = numpy.nan_to_num(closeness_vp.get_array())

        fileTime.close()

        imgDict = dict()

        for r in range(1, maxRadius + 1):
            for t in range(startingThreshold, finalThreshold + 1, thresholdIncrement):
                print("Generating images for plotting: radius = " + str(r) + " threshold = " + str(t))
                key = str(r) + " " + str(t)
                bet = betDict.get(key)
                imgMap = numpy.empty([width, height])

                for i in range(0, width):
                    for j in range(0, height):
                        imgMap[i][j] = bet[((i * width) + j)]

                key = str(r) + " " + str(t)
                imgDict[key] = imgMap

        figure, axesArray = plt.subplots(maxRadius, x + 1, figsize=(5 * maxRadius, 5 * x + 1), squeeze=False)

        plotX = 0

        for r in range(1, maxRadius + 1):
            plotY = 0
            for t in range(startingThreshold, finalThreshold + 1, thresholdIncrement):
                print("Generating subplots: radius = " + str(r) + " threshold = " + str(t))
                key = str(r) + " " + str(t)
                value = imgDict.get(key)

                img = axesArray[plotX][plotY].imshow(value, cmap='hot', clim=(value.min(), value.max()))
                figure.colorbar(img, ax=axesArray[plotX][plotY])
                axesArray[plotX][plotY].set_axis_off()
                axesArray[plotX][plotY].set_title(key)
                # axesArray[plotX,plotY+1] = figure.colorbar(axesArray[plotX,plotY])

                plotY += 1
            plotX += 1

        # fig, ax = plt.subplots()
        # cax = plt.imshow(imgMap, cmap='hot', clim=(0, 1))
        # cbar = fig.colorbar(cax)

        plt.savefig(
            output_directory + "/close_9090_" + str(maxRadius) + "_" + str(thresholdIncrement) + "_" + str(x) + "_" +
            file.split('/')[-1])
        # pos = nx.get_node_attributes(graph, 'pos')

        """"

        nx.draw(graph,pos,with_labels=True)
        labels = nx.get_edge_attributes(graph, 'weight')
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)

        plt.savefig("Outputs/test_graph.jpg")
        """
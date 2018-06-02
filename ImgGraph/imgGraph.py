from math import sqrt
from PIL import Image
import numpy
import time
from graph_tool import Graph
from graph_tool import centrality
from matplotlib import pyplot as plt


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

def computeMetric(img, metric, max_radius, starting_threshold, final_threshold,
                  threshold_increment, iteration_count,input_directory,output_directory,image_name):

    width, height = img.size
    img_array = numpy.array(img)
    empty_graph = generateEmptyGraph(width, height)
    bet_dict = dict()

    # set Outputs formats
    file_time = open(
        output_directory + "/time_" + str(max_radius) + "_" +
        str(threshold_increment) + "_" + str(iteration_count) + "_" +
        input_directory.split('/')[-1] + '.txt', 'a')
    file_time.write('radius, threshold, execution time\n')

    file_degrees = open(
        output_directory + "/degrees_" + str(max_radius) + "_" +
        str(threshold_increment) + "_" + str(iteration_count) + "_" +
        input_directory.split('/')[-1] + '.txt', 'a')

    file_metric = open(
        output_directory + "/" + metric + "_" + str(max_radius) + "_" +
        str(threshold_increment) + "_" + str(iteration_count) + "_" +
        input_directory.split('/')[-1] + '.txt', 'a')

    # Iterates in radius value
    for r in range(1, max_radius + 1):
        # Iterates in Threshold values
        for t in range(starting_threshold, final_threshold + 1, threshold_increment):
            print("Generating graph: radius = " + str(r) + " threshold = " + str(t))

            startTime = time.time()

            graph = generateGraph(Graph(empty_graph), img_array, width, height, r, t)
            vertices = graph.get_vertices().tolist()

            in_degrees = []
            closeness = []

            if (metric == 'closeness'):
                closeness_vp = centrality.closeness(graph, weight=graph.ep.weight)
                in_degrees = graph.get_in_degrees(vertices)
                closeness = numpy.nan_to_num(closeness_vp.get_array())

            final_time = (str(r) + ',' + str(t) + ',' + str(time.time() - startTime) + '\n')

            file_time.write(final_time)
            in_degrees.tofile(file_degrees, sep=",", format="%s")
            file_degrees.write('\n')

            closeness.tofile(file_metric, sep=",", format="%s")
            file_metric.write('\n')

            bet_dict[str(r) + " " + str(t)] = numpy.nan_to_num(closeness_vp.get_array())

    file_degrees.close()
    file_metric.close()
    file_time.close()

    img_dict = dict()

    for r in range(1, max_radius + 1):
        for t in range(starting_threshold, final_threshold + 1, threshold_increment):
            print("Generating images for plotting: radius = " + str(r) + " threshold = " + str(t))
            key = str(r) + " " + str(t)
            bet = bet_dict.get(key)
            img_map = numpy.empty([width, height])

            for i in range(0, width):
                for j in range(0, height):
                    img_map[i][j] = bet[((i * width) + j)]

            key = str(r) + " " + str(t)
            img_dict[key] = img_map

    figure, axesArray = plt.subplots(max_radius, iteration_count + 1, figsize=(5 * max_radius, 5 * iteration_count + 1), squeeze=False)

    plotX = 0

    for r in range(1, max_radius + 1):
        plotY = 0
        for t in range(starting_threshold, final_threshold + 1, threshold_increment):
            print("Generating subplots: radius = " + str(r) + " threshold = " + str(t))
            key = str(r) + " " + str(t)
            value = img_dict.get(key)

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
        output_directory + "/close_9090_" + str(max_radius) + "_" + str(threshold_increment) + "_" + str(iteration_count) + "_" +
        (input_directory + image_name).split('/')[-1])
    # pos = nx.get_node_attributes(graph, 'pos')

    """"

    nx.draw(graph,pos,with_labels=True)
    labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)

    plt.savefig("Outputs/test_graph.jpg")
    """

    return closeness



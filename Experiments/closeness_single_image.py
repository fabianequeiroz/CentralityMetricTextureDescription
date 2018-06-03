import sys, os
import sys, os
sys.path.insert(0, '..')
from ImgGraph import imgGraph

from PIL import Image
import numpy
from matplotlib import pyplot as plt

if __name__ == "__main__":

    # Set parameters list
    MAX_RADIUS = 4
    STARTING_THRESHOLD = 10
    ITERATION_COUNT = 3
    THRESHOLD_INCREMENT = 50
    FINAL_THRESHOLD = STARTING_THRESHOLD + ITERATION_COUNT * THRESHOLD_INCREMENT
    METRIC = 'closeness'

    # Define Directories of inputs and Outputs

    #input_directory = 'Inputs/SingleImageTests'
    input_directory = '../Inputs/Cropped/KTH_TIPS/cotton'
    #output_directory = 'Outputs/SingleImageTests'
    output_directory = '../Outputs/cotton'
    #image_name = '/test_10_10.tiff'
    image_name = '/46-scale_1_im_2_grey.png_1.png'

    # Open the image and convert it to a gray scale format
    img = Image.open(input_directory + image_name )
    img = img.convert('L')

    # Image to graph mapping and metric computation
    metric = imgGraph.computeMetric(img, METRIC,
                                    MAX_RADIUS,
                                    STARTING_THRESHOLD, FINAL_THRESHOLD, THRESHOLD_INCREMENT, ITERATION_COUNT,
                                    input_directory, output_directory,image_name)



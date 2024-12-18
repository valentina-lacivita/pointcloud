from os import environ
from point_cloud.core import calculate_C_points

input_data_file = environ["INPUT_DATA_FILE"]
output_data_file = environ["OUTPUT_DATA_FILE"]
output_plot_file = environ["OUTPUT_PLOT_FILE"]

calculate_C_points(input_data_file, output_data_file, output_plot_file)

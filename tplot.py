#!/usr/bin/python3

import argparse
import numpy as np

def parse_arguments():
    # Set up command-line argument parser for the plotting tool
    parser = argparse.ArgumentParser(description="A simple terminal plotting tool (ASCII Output)")
    # Required argument for specifying which columns to plot
    parser.add_argument("-k", required=True, help="Column numbers to plot (e.g., 1,2,3)")
    # Optional argument for adding labels from a specific column
    parser.add_argument("-b", type=int, help="Column for labels")
    # Optional argument for customizing plot dimensions
    parser.add_argument("-s", help="Plot size as height,width (e.g., 15,100)")
    # Optional argument for setting custom Y-axis range
    parser.add_argument("-y", help="Y-axis range as min,max (e.g., 0,100)")
    # Optional argument for adding custom legends
    parser.add_argument("-l", help="Legends for series (e.g., series1,series2)")
    # Optional argument for input file (can use stdin if not provided)
    parser.add_argument("file", nargs="?", help="Input file")
    return parser.parse_args()

def read_data(file_path, col_nums, label_col=None):
    # Initialize lists to store data and labels
    data = []
    labels = []
    import sys

    # Use stdin if file_path is '-', otherwise open the specified file
    f = sys.stdin if file_path is None else open(file_path, 'r')
    try:
        # Process each row of input
        for row in f:
            values = row.split()
            # Extract values from specified columns (converting to float)
            data.append([float(values[i - 1]) for i in col_nums])
            # If label column is specified, store the label
            if label_col:
                labels.append(values[label_col - 1])
    finally:
        # Ensure file is closed if we opened one
        if file_path is not None:
            f.close()

    # Return transposed data array and labels
    return np.array(data).T, labels

def get_grid_index(value, value_min, value_max, grid_size):
    # Map a value from its range (value_min to value_max) to grid coordinates (0 to grid_size-1)
    if value_min == value_max:
        return 0
    return int((value - value_min) / (value_max - value_min) * (grid_size - 1))

def plot_ascii(data, height=13, width=100, y_range=None, legends=None):
    # ANSI color codes for different series
    COLORS = [
        '\033[31m',  # Red
        '\033[32m',  # Green
        '\033[34m',  # Blue
        '\033[33m',  # Yellow
        '\033[35m',  # Magenta
        '\033[36m',  # Cyan
    ]
    RESET = '\033[0m'  # Reset color
    GRAY = '\033[90m'  # Gray color

    # Get dimensions of the data
    num_series, num_points = data.shape
    # Determine Y-axis range (either from data or user-specified)
    global_min = np.min(data) if y_range is None else y_range[0]
    global_max = np.max(data) if y_range is None else y_range[1]

    # Create empty plot grid (store both character and color)
    screen = [[(" ", None) for _ in range(width)] for _ in range(height)]

    # Determine the row index for the Y-axis value of 0
    zero_row = get_grid_index(0, global_min, global_max, height)

    # Draw horizontal line at zero on the grid with gray color
    if 0 <= zero_row < height:
        for col in range(width):
            screen[height - zero_row - 1][col] = ("-", GRAY)

    # Plot each data series
    for series_idx in range(num_series):
        color = COLORS[series_idx % len(COLORS)]  # Cycle through colors
        for i in range(num_points):
            value = data[series_idx][i]
            # Convert data point to grid coordinates
            row = get_grid_index(value, global_min, global_max, height)
            col = get_grid_index(i, 0, num_points - 1, width)

            # Place marker on grid with color
            if 0 <= row < height and 0 <= col < width:
                char, existing_color = screen[height - row - 1][col]
                if char == " " or char == "-":
                    screen[height - row - 1][col] = ("o", color)
                else:
                    screen[height - row - 1][col] = ("x", color)

    # Generate Y-axis labels with even spacing (reversed)
    y_labels = np.linspace(global_max, global_min, height)
    y_labels = [f"{v:>7.2f}" for v in y_labels]

    # Print the plot with Y-axis labels
    print("\n")
    for i in range(height):
        print(f"{y_labels[i]} | ", end="")
        for j, (char, color) in enumerate(screen[i]):
            if color:
                print(f"{color}{char}{RESET}", end="")
            else:
                print(char, end="")
        print()

    # Draw X-axis line
    x_axis = "-" * width
    print(f" " * 9 + f"+{x_axis}")
    
    # Generate and place X-axis labels
    x_labels = np.linspace(0, num_points - 1, min(10, num_points), dtype=int)
    x_positions = [get_grid_index(x, 0, num_points - 1, width) for x in x_labels]
    x_label_row = [" " for _ in range(width)]
    for pos, label in zip(x_positions, x_labels):
        label_str = f"{label}"
        for j, char in enumerate(label_str):
            if pos + j < width:
                x_label_row[pos + j] = char
    print(f" " * 9 + "".join(x_label_row))

    # Print legends if provided
    if legends:
        print("\nLegends:")
        for i, legend in enumerate(legends):
            color = COLORS[i % len(COLORS)]
            print(f"  {color}Series {i + 1}{RESET}: {legend}")
    print("\n")

def main():
    # Parse command-line arguments
    args = parse_arguments()

    # Extract column numbers to plot
    col_nums = list(map(int, args.k.split(",")))
    
    # Set default plot dimensions and handle custom size if provided
    height, width = (13, 100)

    if args.s:
        size = list(map(int, args.s.split(",")))
        if len(size) == 1:
            height = size[0]
        elif len(size) == 2:
            height, width = size

    # Handle custom Y-axis range if provided
    y_range = None
    if args.y:
        y_range = list(map(float, args.y.split(",")))

    # Set up legends (either custom or default)
    legends = args.l.split(",") if args.l else [f"Series {i + 1}" for i in range(len(col_nums))]

    # Read and plot the data
    data, labels = read_data(args.file, col_nums, label_col=args.b)
    plot_ascii(data, height=height, width=width, y_range=y_range, legends=legends)

if __name__ == "__main__":
    main()


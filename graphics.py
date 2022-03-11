import matplotlib.pyplot as plt
import numpy as np
from colour import Color
from matplotlib import colors

from graph import NodeClass


def display_marking_grid(graph, marking):
    max_marking = 0
    grid_array = []
    for y in range(0, graph.max_row + 1):
        row_array = []
        for x in range(0, graph.max_column + 1):
            id_str = str(y) + ":" + str(x)
            node = graph.get_node(id_str)
            if node:
                if node.kind == NodeClass.FATAL:
                    row_array.append(1)
                elif marking.get_marking(id_str):
                    max_marking = max(max_marking, marking.get_marking(id_str))
                    row_array.append(marking.get_marking(id_str) + 1)
                else:
                    row_array.append(-1)
            else:
                row_array.append(0)
        grid_array.append(row_array)

    red = Color("red")
    gradient = list(red.range_to(Color("green"), max_marking + 1))

    gradient_str = ["#000000"]
    for c in gradient:
        gradient_str.append(c.get_hex_l())
    gradient_str.append("#ffffff")
    print(gradient_str)

    for row in range(len(grid_array)):
        for i in range(len(grid_array[row])):
            if grid_array[row][i] < 0:
                grid_array[row][i] = max_marking + 2

    data = np.array(grid_array)
    print(data)

    # create discrete colormap
    cmap = colors.ListedColormap(gradient_str)
    bounds = list(range(0, max_marking + 4))
    norm = colors.BoundaryNorm(bounds, cmap.N)

    fig, ax = plt.subplots()
    ax.imshow(data, cmap=cmap, norm=norm)

    # draw gridlines
    ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=2)
    ax.set_xticks(np.arange(-.5, graph.max_column, 1))
    ax.set_yticks(np.arange(-.5, graph.max_row, 1))

    for i in range(data.shape[0]):  # rows
        for j in range(data.shape[1]):  # columns
            label = data[i, j] - 1
            if label == max_marking + 1:
                label = "∞"
            text = ax.text(j, i, label, ha="center", va="center", color="black")

    plt.show()

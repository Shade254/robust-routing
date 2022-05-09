import matplotlib.pyplot as plt
import numpy as np
from colour import Color
from matplotlib import colors
from matplotlib.patches import Circle

from graph import EdgeClass, NodeClass
from utils import get_edge_direction


def display_instance(graph, marking, strategy=None, path=None, position=None, end=None,
                     title=None):
    if path:
        if not position:
            position = (
                int(path.path_nodes[0].split(":")[1]),
                int(path.path_nodes[0].split(":")[0]))
        if not end:
            end = (int(path.path_nodes[-1].split(":")[1]),
                   int(path.path_nodes[-1].split(":")[0]))

    ax = display_marking_grid(graph, marking, strategy, show_numbers=False)
    if position:
        ax = display_circle(ax, position, "black")
    if end:
        ax = display_circle(ax, end, "blue")

    if path:
        kind = path.path_edges[0].kind
        y = [int(path.path_nodes[0].split(":")[0])]
        x = [int(path.path_nodes[0].split(":")[1])]
        for e in path.path_edges:
            if e.kind == kind:
                y.append(int(e.to_id.split(":")[0]))
                x.append(int(e.to_id.split(":")[1]))
            else:
                ax = plot_line(ax, x, y, kind)
                kind = e.kind
                y = [int(e.from_id.split(":")[0]), int(e.to_id.split(":")[0])]
                x = [int(e.from_id.split(":")[1]), int(e.to_id.split(":")[1])]
        ax = plot_line(ax, x, y, kind)
    plt.title(title)
    plt.show()


def plot_line(ax, xs, ys, kind):
    color = "blue"
    if kind == EdgeClass.DISTURBANCE:
        color = "purple"
    ax.plot(xs, ys, lw=3, color=color)
    return ax


def display_circle(ax, position, color):
    drawObject = Circle(position, 0.48, fill=False, color=color, lw=3)
    ax.add_patch(drawObject)
    return ax


def display_marking_grid(graph, marking, strategy=None, show_numbers=True):
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

    for row in range(len(grid_array)):
        for i in range(len(grid_array[row])):
            if grid_array[row][i] < 0:
                grid_array[row][i] = max_marking + 2

    data = np.array(grid_array)

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
    for y in range(0, graph.max_row + 1):
        for x in range(0, graph.max_column + 1):
            id_str = str(y) + ":" + str(x)
            if graph.get_node(id_str) and graph.get_node(id_str).kind == NodeClass.FATAL:
                text = ax.text(x, y, "X", ha="center", va="center", color="black")

    if show_numbers and strategy:
        print("Cannot display both numbers and strategy")
        return ax

    if show_numbers:
        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                label = data[i, j] - 1
                if label == max_marking + 1:
                    label = "∞"
                text = ax.text(j, i, label, ha="center", va="center", color="black")

    if strategy:
        for y in range(0, graph.max_row + 1):
            for x in range(0, graph.max_column + 1):
                id_str = str(y) + ":" + str(x)
                if graph.get_node(id_str) and graph.get_node(
                        id_str).kind == NodeClass.FATAL:
                    continue
                edge = strategy.get_move(id_str)
                if not edge:
                    label = "?"
                else:
                    dir = get_edge_direction(edge)
                    if dir == "r":
                        label = "→"
                    elif dir == "l":
                        label = "←"
                    elif dir == "b":
                        label = "↓"
                    elif dir == "u":
                        label = "↑"
                    else:
                        label = "?"
                text = ax.text(x, y, label, ha="center", va="center", color="black")

    return ax

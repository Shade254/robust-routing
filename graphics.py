import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
from colour import Color
from matplotlib import colors

import utils
from graph import EdgeClass, NodeClass
from utils import get_edge_direction


def display_instance(graph, marking, strategy=None, path=None, position=None, end=None,
                     title="", wind_directions=None):
    if path:
        if not position:
            position = (
                int(path.path_nodes[0].split(":")[1]),
                int(path.path_nodes[0].split(":")[0]))
        if not end:
            end = (int(path.path_nodes[-1].split(":")[1]),
                   int(path.path_nodes[-1].split(":")[0]))
    fig, ax = plt.subplots()
    if position and not path:
        display_icon(ax, position, "icons/start.png")
    elif path:
        dir = utils.get_edge_direction(path.path_edges[0])
        if dir == 'b':
            display_icon(ax, position, "icons/down.png")
        elif dir == 'u':
            display_icon(ax, position, "icons/up.png")
        elif dir == 'l':
            display_icon(ax, position, "icons/left.png")
        elif dir == 'r':
            display_icon(ax, position, "icons/right.png")

        dir = utils.get_edge_direction(path.path_edges[-1])
        position = (
            int(path.path_nodes[-2].split(":")[1]),
            int(path.path_nodes[-2].split(":")[0]))
        if dir == 'b':
            display_icon(ax, position, "icons/down.png")
        elif dir == 'u':
            display_icon(ax, position, "icons/up.png")
        elif dir == 'l':
            display_icon(ax, position, "icons/left.png")
        elif dir == 'r':
            display_icon(ax, position, "icons/right.png")
    if end:
        if graph.get_node(str(end[1]) + ":" + str(end[0])).kind == NodeClass.FATAL:
            display_icon(ax, end, "icons/fatal.png")
        else:
            display_icon(ax, end, "icons/end.png")
    ax = display_marking_grid(ax, graph, marking, strategy, show_numbers=False,
                              leave_out=[position, end])
    if wind_directions:
        title += "\nWind direction:"
        if "r" in wind_directions:
            title += "→"
        if "l" in wind_directions:
            title += "←"
        if "b" in wind_directions:
            title += "↓"
        if "u" in wind_directions:
            title += "↑"
    plt.title(title)

    if path:
        kind = path.path_edges[0].kind
        y = [int(path.path_nodes[0].split(":")[0])]
        x = [int(path.path_nodes[0].split(":")[1])]
        for e in path.path_edges[:-1]:
            if e.kind == kind:
                y.append(int(e.to_id.split(":")[0]))
                x.append(int(e.to_id.split(":")[1]))
            else:
                ax = plot_line(ax, x, y, kind)
                kind = e.kind
                y = [int(e.from_id.split(":")[0]), int(e.to_id.split(":")[0])]
                x = [int(e.from_id.split(":")[1]), int(e.to_id.split(":")[1])]
        ax = plot_line(ax, x, y, kind)
    plt.show()


def plot_line(ax, xs, ys, kind):
    color = "blue"
    if kind == EdgeClass.DISTURBANCE:
        color = "purple"
    ax.plot(xs, ys, lw=3, color=color)
    return ax


def display_icon(ax, position, path):
    img = mpimg.imread(path)
    ax.imshow(img,
              extent=(
                  position[0] - 0.5, position[0] + 0.5, position[1] + 0.5,
                  position[1] - 0.5),
              zorder=2)


def display_marking_grid(ax, graph, marking, strategy=None, show_numbers=True,
                         leave_out=[]):
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

    ax.imshow(data, cmap=cmap, norm=norm)

    # draw gridlines
    ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=2)
    ax.set_xticks(np.arange(-.5, graph.max_column, 1))
    ax.set_yticks(np.arange(-.5, graph.max_row, 1))
    for y in range(0, graph.max_row + 1):
        for x in range(0, graph.max_column + 1):
            id_str = str(y) + ":" + str(x)
            if graph.get_node(id_str) and graph.get_node(id_str).kind == NodeClass.FATAL:
                if (x, y) in leave_out:
                    continue
                text = ax.text(x, y, "X", ha="center", va="center", color="black")

    if show_numbers and strategy:
        print("Cannot display both numbers and strategy")
        return ax

    if show_numbers:
        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                if (j, i) in leave_out:
                    continue
                label = data[i, j] - 1
                if label == max_marking + 1:
                    label = "∞"
                text = ax.text(j, i, label, ha="center", va="center", color="black")

    if strategy:
        for y in range(0, graph.max_row + 1):
            for x in range(0, graph.max_column + 1):
                if (x, y) in leave_out:
                    continue
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

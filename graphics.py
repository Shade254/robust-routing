import os

import matplotlib
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
from colour import Color
from matplotlib import colors
from matplotlib.axes import Axes

import utils
from graph import EdgeClass, Graph, NodeClass
from marking import Marking
from path import Path
from strategy import Strategy
from utils import get_edge_direction


def generate_filename(graph: Graph, strategy: Strategy, path: Path,
                      position=None, goal=None, output_folder="./output/", strategy_name=None,
                      dist_name=None):
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)
    file_path = output_folder + graph.name
    if position:
        file_path += "_" + position
    if goal:
        file_path += "_" + goal
    if strategy:
        file_path += "_" + strategy.name + "_strategy.png"
    if path:
        if strategy_name:
            file_path += "_" + strategy_name

        if True in (edge.kind == EdgeClass.DISTURBANCE for edge in path.path_edges):
            if dist_name:
                file_path += "_" + dist_name
            file_path += "_executed.png"
        else:
            file_path += "_planned.png"
    return file_path


def display_instance(graph: Graph, marking: Marking, strategy=None, path=None,
                     position=None, goal=None,
                     title="", display=True, save=False,
                     strategy_name=None, dist_name=None, show_numbers=False):
    if not display and not save:
        return

    matplotlib.rcParams["figure.dpi"] = 240
    fig, ax = plt.subplots()

    if position:
        display_icon(ax, position, "icons/start.png")

    if goal:
        display_icon(ax, goal, "icons/end.png")

    if path:
        dir = utils.get_edge_direction(path.path_edges[0])
        if dir == 'b':
            display_icon(ax, path.path_nodes[0], "icons/down.png")
        elif dir == 'u':
            display_icon(ax, path.path_nodes[0], "icons/up.png")
        elif dir == 'l':
            display_icon(ax, path.path_nodes[0], "icons/left.png")
        elif dir == 'r':
            display_icon(ax, path.path_nodes[0], "icons/right.png")

        dir = utils.get_edge_direction(path.path_edges[-1])
        if dir == 'b':
            display_icon(ax, path.path_nodes[-2], "icons/down.png")
        elif dir == 'u':
            display_icon(ax, path.path_nodes[-2], "icons/up.png")
        elif dir == 'l':
            display_icon(ax, path.path_nodes[-2], "icons/left.png")
        elif dir == 'r':
            display_icon(ax, path.path_nodes[-2], "icons/right.png")

        if graph.get_node(path.path_nodes[-1]).kind == NodeClass.FATAL:
            display_icon(ax, path.path_nodes[-1], "icons/fatal.png")

    ax = display_marking_grid(ax, graph, marking, strategy, show_numbers=show_numbers,
                              leave_out=[position, goal])
    if "_" in graph.name:
        wind_directions = graph.name.split("_")[-1]
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
    fig.tight_layout()

    if save:
        filepath = generate_filename(graph, strategy, path, position, goal, strategy_name=strategy_name,
                                     dist_name=dist_name)
        print("Saving " + filepath)
        plt.savefig(filepath)
    if display:
        plt.show()

    plt.close()


def plot_line(ax: Axes, xs, ys, kind: EdgeClass):
    color = "blue"
    if kind == EdgeClass.DISTURBANCE:
        color = "purple"
    ax.plot(xs, ys, lw=3, color=color)
    return ax


def display_icon(ax: Axes, position, file_path):
    position = (int(position.split(":")[1]), int(position.split(":")[0]))
    img = mpimg.imread(file_path)
    ax.imshow(img,
              extent=(
                  position[0] - 0.5, position[0] + 0.5, position[1] + 0.5,
                  position[1] - 0.5),
              zorder=2)


def display_marking_grid(ax: Axes, graph: Graph, marking: Marking, strategy=None,
                         show_numbers=True,
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
    plt.tick_params(labelleft=False, left=False, labelbottom=False, bottom=False)
    for y in range(0, graph.max_row + 1):
        for x in range(0, graph.max_column + 1):
            id_str = str(y) + ":" + str(x)
            if graph.get_node(id_str) and graph.get_node(id_str).kind == NodeClass.FATAL:
                if (x, y) in leave_out:
                    continue
                text = ax.text(x, y, "x", ha="center", va="center", color="black")

    if show_numbers and strategy:
        print("Cannot display both numbers and strategy")
        return ax

    if show_numbers:
        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                if str(j) + ":" + str(i) in leave_out:
                    continue
                label = data[i, j] - 1
                if label == max_marking + 1:
                    label = "∞"
                if label != 0:
                    text = ax.text(j, i, label, ha="center", va="center", color="black")

    if strategy:
        for y in range(0, graph.max_row + 1):
            for x in range(0, graph.max_column + 1):
                id_str = str(y) + ":" + str(x)
                if id_str in leave_out:
                    continue
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

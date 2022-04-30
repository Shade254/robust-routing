import matplotlib.pyplot as plt
import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from graph import Graph
from graphics import display_instance
from marking import Marking


class MainWindow:
    def __init__(self):
        sg.theme("DarkBlue3")
        self.canvas = sg.Graph((640, 480), (0, 0), (640, 480), key='Graph1')
        self.file_input = sg.InputText("./test_cases/basic.txt", enable_events=True,
                                       key="file_input", size=(30, 1))
        self.file_button = sg.Button("Load", disabled_button_color="gray")

        first_line = [sg.Text("Graph file:"), self.file_input, self.file_button]

        self.disturbance_directions = {
            "u": sg.Checkbox("Up"),
            "b": sg.Checkbox("Down"),
            "l": sg.Checkbox("Left"),
            "r": sg.Checkbox("Right")
            }

        second_line = [sg.Text("Directions:")]

        for v in self.disturbance_directions.values():
            second_line.append(v)

        third_line = []
        self.force_min_input = sg.InputText("1", size=(8, 1))
        self.force_max_input = sg.InputText("2", size=(8, 1))
        self.disturbance_button = sg.Button("Disturb", disabled=True,
                                            disabled_button_color="gray")
        third_line.append(sg.Text("Min force:"))
        third_line.append(self.force_min_input)
        third_line.append(sg.Text("Max force:"))
        third_line.append(self.force_max_input)
        third_line.append(self.disturbance_button)

        fourth_line = [sg.Text("Start:")]
        self.position_input = sg.InputText("0:0", size=(8, 1))
        self.goal_input = sg.InputText("0:0", size=(8, 1))
        self.od_button = sg.Button("Change")
        fourth_line.append(self.position_input)
        fourth_line.append(sg.Text("Goal:"))
        fourth_line.append(self.goal_input)
        fourth_line.append(self.od_button)

        fifth_line = [sg.Text("Display:")]
        self.marking_radio = sg.Radio('Marking', "ImageRadio", default=True,
                 k='ImageRadioMarking', enable_events=True)
        self.strategy_radio = sg.Radio('Strategy', "ImageRadio", k='ImageRadioStrategy', enable_events=True)
        fifth_line.append(self.marking_radio)
        fifth_line.append(self.strategy_radio)

        self.layout = [[self.canvas, sg.VerticalSeparator(),
                        sg.Column([first_line, second_line, third_line, fourth_line, fifth_line],
                                  size=(300, 300), expand_y=True)]]
        self.window = sg.Window("Console", self.layout, finalize=True)

        self.graph = None
        self.marking = None

        plt.ioff()
        fig1 = plt.figure(1)
        ax1 = plt.subplot(111)
        self.pack_figure(fig1)

    def draw_figure(self):
        start = (int(self.position_input.get().split(":")[0]), int(self.position_input.get().split(":")[1]))
        end = (int(self.goal_input.get().split(":")[0]), int(self.goal_input.get().split(":")[1]))

        fig, ax = display_instance(self.graph, self.marking, position=start, end=end, show_numbers=self.marking_radio.get(), in_gui=True)
        fig.canvas.draw()

    def load_graph(self):
        self.file_button.update(disabled=True)
        path = self.file_input.get()
        self.graph = Graph(path)
        self.marking = None
        self.draw_figure()
        self.file_button.update(disabled=False)
        self.disturbance_button.update(disabled=False)

    def pack_figure(self, figure):
        canvas = FigureCanvasTkAgg(figure, self.canvas.Widget)
        plot_widget = canvas.get_tk_widget()
        plot_widget.pack(side='top', fill='both', expand=1)
        return plot_widget

    def add_disturbances(self):
        self.disturbance_button.update(disabled=True)
        self.graph.delete_all_disturbance_edges()
        min_force = self.force_min_input.get()
        max_force = self.force_max_input.get()
        directions = ""
        for k, v in self.disturbance_directions.items():
            if v.get():
                directions += k
        self.graph.create_disturbance_edges(directions, int(min_force), int(max_force))
        self.marking = Marking(self.graph)
        self.draw_figure()
        self.disturbance_button.update(disabled=False)


if __name__ == "__main__":
    w = MainWindow()
    while True:
        event, values = w.window.read(timeout=100)
        if event == sg.WINDOW_CLOSED:
            break
        if event and event is not sg.TIMEOUT_EVENT:
            print(event)
            if event == "Load":
                w.load_graph()
            elif event == "Disturb":
                w.add_disturbances()
            elif event == "Change":
                w.draw_figure()
            elif "ImageRadio" in event:
                w.draw_figure()
    w.window.close()

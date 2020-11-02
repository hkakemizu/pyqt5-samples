import matplotlib
import matplotlib.animation as animation
import numpy as np
import qtawesome as qta
import seaborn as sns
import sys

from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar,
)
from matplotlib.figure import Figure
from PyQt5.QtWidgets import (
    QApplication,
    QCheckBox,
    QHBoxLayout,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

matplotlib.use('Qt5Agg')
sns.set()


class PlotCanvas(FigureCanvas):
    LINES_COUNT = 2

    def __init__(self, parent=None, width=8, height=6, dpi=100):
        self._fig = Figure(figsize=(width, height), dpi=dpi)
        self._ax = self._fig.add_subplot(111)
        super().__init__(self._fig)

        sampleCount = 256
        self._xdata = np.arange(sampleCount)
        self._ydata = np.random.rand(self.LINES_COUNT, sampleCount)
        self._lines = []
        for i in range(self.LINES_COUNT):
            self._line, = self._ax.plot(self._xdata, self._ydata[i])
            self._lines.append(self._line)

        self._ani = animation.FuncAnimation(self._fig, self.update_plot, blit=True, interval=10)
        self._running = False

    def update_plot(self, _):
        if self._running:
            for i in range(self.LINES_COUNT):
                self._ydata[i] = np.append(self._ydata[i][1:], np.random.rand(1))
                self._lines[i].set_ydata(self._ydata[i])
        return self._lines

    def start(self):
        self._running = True

    def stop(self):
        self._running = False

    def enable_line(self, index, visible):
        if index >= 0 and index < self.LINES_COUNT:
            self._lines[index].set_visible(visible)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self._button = QPushButton(qta.icon('fa.play'), 'start')
        self._button.setCheckable(True)
        self._button.setChecked(False)
        self._button.clicked.connect(self.start_stop)

        self._checkbox0 = QCheckBox('show line0')
        self._checkbox0.setChecked(True)
        self._checkbox0.clicked.connect(self.enable_line0)
        self._checkbox1 = QCheckBox('show line1')
        self._checkbox1.setChecked(True)
        self._checkbox1.clicked.connect(self.enable_line1)

        layout_buttons = QHBoxLayout()
        layout_buttons.addWidget(self._button)
        layout_buttons.addWidget(self._checkbox0)
        layout_buttons.addWidget(self._checkbox1)

        self._plot_canvas = PlotCanvas(self)
        toolbar = NavigationToolbar(self._plot_canvas, self)

        layout = QVBoxLayout()
        layout.addLayout(layout_buttons)
        layout.addWidget(toolbar)
        layout.addWidget(self._plot_canvas)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def start_stop(self, toggled):
        if toggled:
            self._button.setIcon(qta.icon('fa.stop'))
            self._button.setText('stop')
            self._plot_canvas.start()
        else:
            self._button.setIcon(qta.icon('fa.play'))
            self._button.setText('start')
            self._plot_canvas.stop()

    def enable_line0(self, toggled):
        self._plot_canvas.enable_line(0, toggled)

    def enable_line1(self, toggled):
        self._plot_canvas.enable_line(1, toggled)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = MainWindow()
    window.show()
    app.exec_()

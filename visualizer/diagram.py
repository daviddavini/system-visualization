import matplotlib
from visualizer.systems import standard_A

import time
import threading
import warnings
from matplotlib.widgets import Button
from matplotlib import pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import InsetPosition
import numpy as np

#matplotlib.rcParams['text.latex.preamble'] = r'\usepackage{amsmath}'
# matplotlib.rcParams['text.usetex'] = True

class ClassificationDiagram:
  '''The classification diagram for 2D linear systems.'''

  def __init__(self, ax, on_update):
    '''Setup the diagram on the given axes.'''

    self.ax = ax 
    self.fig = self.ax.get_figure()

    self.on_update_callback = on_update

    # Set x and y limits
    self.ax.set(xlim = (-0.5, 1), ylim = (-3, 3))

     # Label the axes
    self.ax.set_ylabel(r'$\tau$ (trace)')
    self.ax.set_xlabel(r'$\Delta$ (determinant)')

    # Get information from axes
    xmin, xmax = self.ax.get_xlim()
    ymin, ymax = self.ax.get_ylim()
    
    # Plot the trace-det parabola
    ys = np.linspace(ymin,ymax,30)
    xs = ys**2 / 4
    self.ax.plot(xs, ys)

    # Plot the x and y axes
    self.ax.hlines(y=0, xmin=xmin, xmax=xmax, color='g')
    self.ax.vlines(x=0, ymin=ymin, ymax=ymax, color='g')

    # Plot mouse point
    self.det = 0
    self.trace = 0
    self.mouse_point, = self.ax.plot(self.det, self.trace,'bo')
    self.update(self.det, self.trace)

    # The auto thread
    self.is_auto_on = False
    self.auto_thread = None
    self.auto_index = 0

    # Create a mouse plotter
    self.cid = self.fig.canvas.mpl_connect('button_press_event', 
      lambda event : self.on_click(event))
  
  def update(self, det, trace):
    self.mouse_point.set_xdata(det)
    self.mouse_point.set_ydata(trace)
    self.trace = trace
    self.det = det
    self.A = standard_A(self.trace, self.det)
    self.f = lambda x : self.A.dot(x)

    self.on_update_callback(self)
  
  def on_click(self, event):
    if event.inaxes == self.ax:
      det, trace = event.xdata.item(), event.ydata.item()
      self.stop_auto()
      self.update(det, trace)
    
  def start_auto(self):
    def auto():
      theta = np.linspace(0, 2*np.pi, 50)
      dets = 0.25 + 0.5 * np.cos(theta)
      traces = 2 * np.sin(theta)

      diagram_path = np.stack((dets, traces)).T

      while self.is_auto_on:
        start_time = time.time()
        det, trace = diagram_path[self.auto_index]
        self.update(det = det, trace = trace)
        plt.show(block=False)

        # Make sure we wait at least T seconds
        sleep_time = 0.1
        delta_time = time.time() - start_time
        time_remaining = sleep_time - delta_time
        if time_remaining > 0:
          time.sleep(time_remaining)

        self.auto_index += 1
        if self.auto_index >= len(diagram_path):
          self.auto_index = 0
    
    self.is_auto_on = True
    self.auto_thread = threading.Thread(target=auto, daemon=True)
    self.auto_thread.start()
  
  def stop_auto(self):
    self.is_auto_on = False
  
  def toggle_auto(self):
    if self.is_auto_on:
      self.stop_auto()
    else:
      self.start_auto()
  

class DiagramInfo:
  '''Manages the plot that displays diagram info.'''
  precision = 2

  def __init__(self, ax, on_auto_clicked):
    self.ax = ax
    self.on_auto_clicked_callback = on_auto_clicked

    kwargs = {
      'horizontalalignment':'center',
      'verticalalignment':'center', 
      'transform':self.ax.transAxes
    }

    self.A_text = self.ax.text(.05, .5, "A =", fontsize = 25, **kwargs)
    self.matrix_text = self.ax.text(.7, .5, "(No Matrix)", fontsize = 25, **kwargs)
    self.trace_text = self.ax.text(.5, .15, "(No Data)", fontsize = 14, **kwargs)
    self.det_text = self.ax.text(.5, .05, "(No Data)", fontsize = 14, **kwargs)

    # AUTO Button setup
    warnings.filterwarnings("ignore", message= "This figure includes Axes that are not compatible with tight_layout, so results might be incorrect.")

    button_axes = plt.axes([0, 0, 1, 1])
    ip = InsetPosition(self.ax, [0.2, 0.88, 0.6, 0.1])
    button_axes.set_axes_locator(ip)
    self.auto_button = Button(button_axes, 'RUN AUTO ELLIPSE', color='gray')
    self.auto_button.on_clicked(lambda event : self.on_auto_clicked(event))

    # Don't draw the axes
    self.ax.axis('off')
  
  def update(self, trace, det, A):
    A_ = np.around(A, self.precision)
    txt = "{}  {} \n{}  {} ".format(A_[0,0], A_[0,1], A_[1,0], A_[1,1])
    #A_txt=r"$ \begin{matrix} a & b \\ d & e \end{matrix} $"
    self.matrix_text.set_text(txt)

    txt = r"$\tau = {0:.2f}$".format(trace)    
    self.trace_text.set_text(txt)

    txt = r"$\Delta = {0:.2f}$".format(det)    
    self.det_text.set_text(txt)
  
  def on_auto_clicked(self, event):
    self.on_auto_clicked_callback()

    
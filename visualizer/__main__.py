####### In class demonstration
####Plot dynamical system

from visualizer.approx import rungenkutta
from visualizer.diagram import ClassificationDiagram, DiagramInfo
from visualizer.portrait import PhasePortrait

import sys
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation

# Change the color palette
plt.style.use('seaborn-pastel')


### Setup figure, with subplots
fig = plt.figure(figsize=(10,6))
fig.suptitle('Visualization of 2D Linear Systems', fontsize = 25, fontweight = 'bold')

diagram_axes = plt.subplot2grid((2, 3), (0, 0))
portrait_axes = plt.subplot2grid((2, 3), (0, 1), rowspan = 2, colspan = 2)
info_axes = plt.subplot2grid((2,3), (1, 0))

### Handle object interaction:
def on_diagram_update(diagram):
    # Update the phase portrait plot
    portrait.set_f(diagram.f)
    # Update text
    info.update(diagram.trace, diagram.det, diagram.A)
    # Redraw to the screen
    plt.draw()

def on_info_auto_button_clicked():
    diagram.toggle_auto()

### Create the objects that manage the separate subplots
portrait = PhasePortrait(portrait_axes)
info = DiagramInfo(info_axes, on_auto_clicked=on_info_auto_button_clicked)
diagram = ClassificationDiagram(diagram_axes, on_update = on_diagram_update)

# Must be called after adding labels, etc
fig.tight_layout(rect=[0, 0, 1, 0.93])

### Make sure pyplot doesn't keep opening more windows
def on_close(event):
    exit()

fig.canvas.mpl_connect('close_event', on_close)

plt.show()
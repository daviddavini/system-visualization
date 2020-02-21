import numpy as np
from matplotlib import pyplot as plt
import warnings

from visualizer.approx import rungenkutta
from visualizer.colors import plot_gradient, Color

class Trajectory:
  '''An individual trajectory on the PhasePortrait.'''
  N = 50
  dt = .1
  # unused
  colors = ['b']
  next_color = 0

  start_color = Color((1,0,0,0)) # Red
  mid_color =   Color((0.3,0.7,0.3,1)) # Green
  end_color =   Color((0,0,1,0)) # Blue

  linewidth = 3

  def __init__(self, ax, x0):
    self.ax = ax

    self.x0 = x0
    self.lines = []
    # unused
    self.color = self.colors[self.next_color % len(self.colors)]
    self.__class__.next_color += 1

  def create(self, f):
    '''Creates new trajectory data and plots it in the axes.'''
    # If we already drew lines, delete them
    if len(self.lines) > 0:
      for line in self.lines:
        line.remove()
      self.lines = []

    # Create and plot data
    front_data = np.array(rungenkutta(self.N,self.x0,lambda x : -f(x),self.dt,True)).T
    back_data = np.array(rungenkutta(self.N,self.x0,f,self.dt,True)).T
    #back_data = np.flip(back_data, axis = 1)

    self.data = np.concatenate((back_data, front_data), axis=1)
    
    plot_kwargs = {'linewidth':self.linewidth}

    front_lines = plot_gradient(self.ax, front_data, 10, self.mid_color, self.start_color, **plot_kwargs)
    back_lines = plot_gradient(self.ax, back_data, 10, self.mid_color, self.end_color, **plot_kwargs)
    self.lines = front_lines + back_lines
    #self.ax.plot(X, Y, color=self.color)

def polar_sampling(xmin, xmax, ymin, ymax, N):
  '''Returns a polar sampling of points in the given box.'''
  bounds = [xmin, xmax, ymin, ymax]
  Rmax = min([abs(x) for x in bounds])
  x0s = []
  R_count = N
  theta_count = N
  for R in np.linspace(0, Rmax, R_count, endpoint=False):
    for theta in np.linspace(0, 2*np.pi, theta_count, endpoint=False):
      x = R*np.cos(theta)
      y = R*np.sin(theta)
      x0s.append([x, y])
  
  return np.array(x0s)

def cartesian_sampling(xmin, xmax, ymin, ymax, N):
  '''Returns an evenly-distributed sampling of points in the given box.'''
  X, Y = np.meshgrid(
    np.linspace(xmin, xmax, N+2)[1:-1],
    np.linspace(ymin, ymax, N+2)[1:-1]
  )
  XY = np.stack((X, Y))
  return XY.reshape(2, -1).T

class PhasePortrait:
  '''Manages the phase portrait plot.'''

  xlim = (-10, 10)
  ylim = (-10, 10)
  field_density = 15

  def __init__(self, ax, f = lambda x : np.array([0,0])):
    self.ax = ax

    # Set the axes limits
    self.ax.set(xlim = self.xlim, ylim = self.ylim)
    xmin, xmax = self.ax.get_xlim()
    ymin, ymax = self.ax.get_ylim()

    # Label the axes
    self.ax.set_ylabel('y')
    self.ax.set_xlabel('x')

    self.quiver = None
    # Ignore quivers complaints (when plotting the zero field)
    warnings.filterwarnings("ignore", category=RuntimeWarning, module='matplotlib')

    # Create the initial points for trajectories
    self.x0s = cartesian_sampling(xmin, xmax, ymin, ymax, 5)

    # List of x0, line objects
    self.trajectories = []
    for x0 in self.x0s:
      self.trajectories.append(Trajectory(self.ax, x0))

    self.set_f(f)

  def set_f(self, f):
    '''Create the vector function f used for the vector field.'''
    self.f = f
    # Plot the trajectories
    self.plot_trajectories()
    # Plot the vector field
    self.plot_vector_field()

  def plot_trajectories(self):

    for trajectory in self.trajectories:
      trajectory.create(self.f)

  def plot_vector_field(self):
    '''Plots the vector field for x' = f(x).'''
    xlim = self.ax.get_xlim()
    ylim = self.ax.get_ylim()
    
    # Create the vector field inputs... (x,y) pairs
    X, Y = np.meshgrid(
        np.linspace(xlim[0], xlim[1], self.field_density),
        np.linspace(ylim[0], ylim[1], self.field_density)
    )

    # Apply the function to the vector field
    XY = np.stack(arrays = (X,Y), axis = 2)
    UV = np.apply_along_axis(func1d = self.f, axis = 2, arr = XY)
    U, V = np.split(ary = UV, indices_or_sections = 2, axis = 2)

    # Get rid of the dummy axis
    U = np.squeeze(U, axis = 2)
    V = np.squeeze(V, axis = 2)

    # Remove the last plotted field
    if self.quiver:
      self.quiver.remove()

    # Plot the new field
    self.quiver = self.ax.quiver(X,Y,U,V, units='x')

    # Get back warnings

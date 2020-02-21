from matplotlib import pyplot as plt
import matplotlib

import numpy as np

def split_overlap_endpoints(arr, section_count, axis):
  '''Similar to np.array_split, but with overlapping endpoints.'''

  # Split the arr normally
  arrs = np.array_split(arr, section_count, axis=axis)

  # Add the end of each previous section to the next section (slow)
  for i in range(len(arrs)-1):
    end = arrs[i].take(-1, axis=axis)
    end = np.expand_dims(end, axis=axis)
    arrs[i+1] = np.concatenate((end, arrs[i+1]), axis=axis)

  return arrs

class Color:
  '''Since matplotlib has no Color class, this serves the essential purposes.'''
  def __init__(self, x):
    if isinstance(x, Color):
      self.rgba = x.rgba
    elif isinstance(x, tuple) and len(x) == 4:
      self.rgba = x
    else:
      self.rgba = matplotlib.colors.to_rgba(x)
  
  def __add__(self, other):
    return Color(tuple(sum(x) for x in zip(self.rgba,other.rgba)))
  
  def __neg__(self):
    return Color(tuple(-x for x in self.rgba))
  
  def __sub__(self, other):
    return self + (-other)
  
  def __mul__(self, scalar):
    if not isinstance(scalar, (int, float, complex)):
      raise Exception("Can only multiply color with number")

    return Color(tuple(x * scalar for x in self.rgba))

  def __str__(self):
    return "Color({})".format(self.rgba)
  
  def get_rgba(self):
    return self.rgba

  def get_rgb(self):
    return self.rgba[:-1]
  
  @classmethod
  def range(cls, C1, C2, section_count):
    colors = []
    for i in range(section_count):
      percent = i / section_count
      colors.append( (C2-C1)*percent + C1 )
    return colors

Color.blue = Color('b')
Color.red = Color('r')
Color.green = Color('g')

def plot_gradient(ax, XY, section_count, c1, c2, **kwargs):
  '''Plots line as a gradient, gradually changing color from c1 to c2.
  (XY is a 2 x N array).'''

  C1 = Color(c1)
  C2 = Color(c2)

  colors = []
  for i in range(section_count):
    # C = (C2 - C1) * percent + C1
    percent = i / section_count
    colors.append( (C2-C1)*percent + C1 )

  # Split XY into segments to be colored
  XY_parts = split_overlap_endpoints(XY, section_count, axis = 1)

  lines = []

  for XY_part, color in zip(XY_parts, colors):
    X = XY_part[0,:]
    Y = XY_part[1,:]
    line, = ax.plot(X, Y, c=color.get_rgba(), **kwargs)
    lines.append(line)
  
  return lines

if __name__ == '__main__':
  
  x = np.linspace(-1, 1, 100)
  y = x ** 2
  xy = np.stack((x,y), axis = 1)

  print(Color.blue)

  plot_gradient(plt, xy, 100, 'r', 'y')

  plt.show()

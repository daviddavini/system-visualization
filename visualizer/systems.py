import numpy as np

def standard_A(trace, det):
  '''Creates the typical A matrix for the linear system
   with trace and determinant.'''

  decider = trace**2 - 4*det

  if decider > 0:
    # Real eigenvalues exist
    return eigenvalued_A(trace, det)
  
  else:
    # Eigenvalues don't exist
    return symmetric_A(trace, det)

  a = trace / 2 
  b = ( det - a**2 )**0.5 
  A = np.array([[a, -b],[b, a]])

  return A

def eigenvalued_A(trace, det):
  '''The unique matrix with trace and determinant,
  given x-axis and y-axis are eigen-directions.'''
  radical = (trace**2 - 4*det) ** 0.5
  ev1 = (trace + radical) / 2
  ev2 = (trace - radical) / 2
  A = np.array([[ev1, 0],[0, ev2]])

  return A

def symmetric_A(trace, det):
  '''The unique matrix with trace and determinant,
  given 90 degree rotational symmetry.'''

  a = trace / 2 
  b = ( det - a**2 )**0.5 
  A = np.array([[a, -b],[b, a]])

  return A
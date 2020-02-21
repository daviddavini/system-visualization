def eulermethod(n,x0,fun,dt,autonomous=False,t0=0):
  ''' Solve system x' = f(t,x) from initial state t0,x0 for n steps of size dt, standard Euler '''
  vals =[x0]
  curx=x0
  curt=t0 #initialize

  #do for n steps
  for j in range(0,n-1):
    nextt = curt+dt #next time
    if (not autonomous):
        nextx = curx+dt*fun(curt,curx) #compute val
    else:
        nextx = curx+dt*fun(curx)

    vals.append(nextx) #add next value

    curx=nextx
    curt=nextt #update vals

  return vals

## Solve system x' = f(t,x) from initial state t0,x0 for n steps of size dt. Update using average of f at x, and potential x
def averageeuler(n,x0,fun,dt,autonomous=False,t0=0):
    vals =[x0]
    curx=x0
    curt=t0 #initialize

    #do for n steps
    for j in range(0,n-1):
        nextt = curt+dt #next time
        if (not autonomous):
            nextx = curx+dt*(fun(curt,curx)+fun(curt+dt,curx+dt*curx))/2 #compute val
        else:
            nextx = curx+dt*(fun(curx)+fun(curx+dt*curx))/2 #compute val

        vals.append(nextx) #add next value

        curx=nextx
        curt=nextt #update vals

    return vals


# Solve using Rungen-kutta
def rungenkutta(n,x0,fun,dt,autonomous=False,t0=0):
    vals =[x0]
    curx=x0
    curt=t0 #initialize

    #do for n steps
    for j in range(0,n-1):
        nextt = curt+dt #next time

        if (not autonomous):
            k1 = dt*fun(curt,curx)
            k2 = dt*fun(curt+dt/2, curx+k1/2)
            k3 = dt*fun(curt + dt/2, curx+k2/2)
            k4 = dt*fun(curt + dt, curx+k3)
        else:
            k1 = dt*fun(curx)
            k2 = dt*fun(curx+k1/2)
            k3 = dt*fun(curx+k2/2)
            k4 = dt*fun(curx+k3)

        nextx = curx+(k1+2*k2+2*k3+k4)/6 #compute val

        vals.append(nextx) #add next value

        curx=nextx
        curt=nextt #update vals

    return vals
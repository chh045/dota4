# -*- coding: utf-8 -*-

from p3_basic_backtracking import *
from collections import deque


def ac3(csp, arcs=None):
    """Executes the AC3 or the MAC (p.218 of the textbook) algorithms.

    If the parameter 'arcs' is None, then this method executes AC3 - that is, it will check the arc consistency
    for all arcs in the CSP.  Otherwise, this method starts with only the arcs present in the 'arcs' parameter
    in the queue.

    Note that the current domain of each variable can be retrieved by 'variable.domains'.

    This method returns True if the arc consistency check succeeds, and False otherwise."""

    queue_arcs = deque(arcs if arcs is not None else csp.constraints.arcs())

    # TODO implement this
    def getNeighbors(csp,xi):
        neighbors = defaultdict(lambda: None)
        for cons in csp.constraints[xi]:
            neighbors[cons.var2] = cons.var2
        neighList = []
        for var in neighbors:
            neighList.append(var)
        return neighList

    while(queue_arcs):
        pair = queue_arcs.pop()
        xi = pair[0]
        xj = pair[1]

        listxj = [xj]                           #create a set containing just the Xj variable
        if revise(csp,xi,xj):                   #If we find values in Xi's domain that don't satisfy (Xi,Xj)
            if len(xi.domain) == 0:
                return False                    #csp has no solution with current configuration
            for xk in list(set(getNeighbors(csp,xi)) - set(listxj)):        #iterate over neighbors of Xi that aren't Xj
                queue_arcs.append((xk, xi))     #Add variables with reduced domain to queue

    return True

def revise(csp, xi, xj):
    # You may additionally want to implement the 'revise' method.
    def no_value_satisfies(csp, x, xi, xj):
        for cons in csp.constraints[xi]:
            if cons.var2 == xj:
                if cons.var2.is_assigned():
                    if cons.is_satisfied(x, cons.var2.value) == True:
                        return False
                else:
                    for y in cons.var2.domain:
                        if cons.is_satisfied(x,y) == True:
                            return False
        return True
        

    revised = False
    for x in xi.domain:
        if no_value_satisfies(csp, x, xi, xj):      #value x doesn't satisfy (Xi,Xj) constraints
            xi.domain.remove(x)
            revised = True

    return revised
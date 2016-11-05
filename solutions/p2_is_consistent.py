# -*- coding: utf-8 -*-

from p1_is_complete import *

def is_consistent(csp, variable, value):
    """Returns True when the variable assignment to value is consistent, i.e. it does not violate any of the constraints
    associated with the given variable for the variables that have values assigned.

    For example, if the current variable is X and its neighbors are Y and Z (there are constraints (X,Y) and (X,Z)
    in csp.constraints), and the current assignment as Y=y, we want to check if the value x we want to assign to X
    violates the constraint c(x,y).  This method does not check c(x,Z), because Z is not yet assigned."""

    # TODO implement this
    for constraint in csp.constraints[variable]:
        if constraint.var2.domain == 1 and constraint.var2.is_assigned() == True:
            if constraint.is_satisfied(value, constraint.var2.value) == False:
                return False
        else:
            counter = 0
            for value2 in constraint.var2.domain:
                if constraint.is_satisfied(value, value2) == False:
                    counter += 1
            if counter >= len(constraint.var2.domain):
               return False
    return True      

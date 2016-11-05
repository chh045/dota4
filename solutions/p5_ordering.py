# -*- coding: utf-8 -*-

from p4_ac3 import *
from Queue import PriorityQueue
from collections import defaultdict

def select_unassigned_variable(csp):
    """Selects the next unassigned variable, or None if there is no more unassigned variables
    (i.e. the assignment is complete).

    This method implements the minimum-remaining-values (MRV) and degree heuristic. That is,
    the variable with the smallest number of values left in its available domain.  If MRV ties,
    then it picks the variable that is involved in the largest number of constraints on other
    unassigned variables.
    """

    # TODO implement this
    global numCons
    numCons = 0

    unassigned_vars = filter(lambda x: not x.is_assigned(),csp.variables)
    mrv_vars = filter(lambda x:len(x.domain) == len(min(unassigned_vars,key=lambda x:len(x.domain)).domain),unassigned_vars)

    gt = -1
    res = None
    for var in mrv_vars:
        x = len(csp.constraints[var])
        for o_var in unassigned_vars:
            if o_var == var: continue
            o_x = len(csp.constraints[var,o_var])
            if x + o_x > gt:
                gt = x+o_x
                res = var
                #print var.domain
    return res 



def order_domain_values(csp, variable):
    """Returns a list of (ordered) domain values for the given variable.

    This method implements the least-constraining-value (LCV) heuristic; that is, the value
    that rules out the fewest choices for the neighboring variables in the constraint graph
    are placed before others.
    """

    # TODO implement this
    var = variable
    q = PriorityQueue()

    for value in var.domain:
        counter = 0
        for cons in csp.constraints[var]:                               #Iterate over neighbors of var
            if cons.var2.is_assigned():
                if cons.is_satisfied(value, cons.var2.value) == True:   #We found another satisfied constraint
                    counter += 1
            else:
                for val2 in cons.var2.domain:
                    if cons.is_satisfied(value, val2) == True:          #We found another satisfied constraint
                        counter += 1
        q.put((counter, value))                                         #Add (# of satisfied cons, value) to queue

    orderedDomain = []
    while(q.empty() == False):
        counter, value = q.get()
        orderedDomain.insert(0,value)                                      #add elements of queue to a list
                                                                         # with correct ordering
    return orderedDomain

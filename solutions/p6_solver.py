from collections import deque
from operator import itemgetter


def inference(csp, variable):
    """Performs an inference procedure for the variable assignment.
    For P6, *you do not need to modify this method.*
    """
    return ac3(csp, csp.constraints[variable].arcs())


def backtracking_search(csp):
    """Entry method for the CSP solver.  This method calls the backtrack method to solve the given CSP.
    If there is a solution, this method returns the successful assignment (a dictionary of variable to value);
    otherwise, it returns None.
    For P6, *you do not need to modify this method.*
    """
    if backtrack(csp):
        return csp.assignment
    else:
        return None


def backtrack(csp):
    """Performs the backtracking search for the given csp.
    If there is a solution, this method returns True; otherwise, it returns False.
    """

    # csp is is complete
    if (is_complete(csp)):
        return csp.assignment;
    else:
        var = select_unassigned_variable(csp);
        # Loop through all possible values for var
        for value in order_domain_values(csp, var):
            # assign if value is consistent with var
            if (is_consistent(csp, var, value)):
                csp.variables.begin_transaction();
                var.assign(value);
                inference(csp, var);
                result = backtrack(csp);
                if (result != False):
                    return result;
                else:
                    # Value didn't work, so backtrack
                    csp.variables.rollback();
        return False;

def is_consistent(csp, variable, value):
    """Returns True when the variable assignment to value is consistent, i.e. it does not violate any of the constraints
    associated with the given variable for the variables that have values assigned.
    For example, if the current variable is X and its neighbors are Y and Z (there are constraints (X,Y) and (X,Z)
    in csp.constraints), and the current assignment as Y=y, we want to check if the value x we want to assign to X
    violates the constraint c(x,y).  This method does not check c(x,Z), because Z is not yet assigned."""

    # Looks through all the constraints linked to the variable
    for c in csp.constraints[variable]:
        # Loop through all the variable
        for v2 in csp.variables:
            # Check if is assigned and is set
            if(v2 == c.var2 and v2.is_assigned()):
                # Check if satisfied
                if not c.is_satisfied(value, v2.value):
                    return False

    return True

def is_complete(csp):
    """Returns True when the CSP assignment is complete, i.e. all of the variables in the CSP have values assigned."""
    for x in csp.variables:
        if (not x.is_assigned()):
            return False;

    return True;


def select_unassigned_variable(csp):
    """Selects the next unassigned variable, or None if there is no more unassigned variables
    (i.e. the assignment is complete).
    This method implements the minimum-remaining-values (MRV) and degree heuristic. That is,
    the variable with the smallest number of values left in its available domain.  If MRV ties,
    then it picks the variable that is involved in the largest number of constraints on other
    unassigned variables.
    """

    smallestDomain = float("infinity");
    unassignedVars = deque();

    for variable in csp.variables:
        currentDomain = len(variable.domain);
        # length of domain of variable is less than the previous smallest domain, but
        # variable is unassigned
        if (currentDomain < smallestDomain and currentDomain != 1):
            # variable is the new MRV variable
            unassignedVars.clear();
            unassignedVars.append(variable);
            # currentDomain is the new smallestDomain
            smallestDomain = currentDomain;
        # length of domain of variable is equal to smallest domain, so add variable to 
        # queue of variables with the minimum remaining values
        elif (currentDomain == smallestDomain):
            unassignedVars.append(variable);
        # if length of domain is greater than previous smallest domain, skip this variable

    largestConstraints = float("-infinity");
    # unassignedVars holds the variables with MRV ties
    for var in unassignedVars:
        if (len(csp.constraints[var]) > largestConstraints):
            nextVar = var;
    return nextVar;


def order_domain_values(csp, variable):
    """Returns a list of (ordered) domain values for the given variable.
    This method implements the least-constraining-value (LCV) heuristic; that is, the value
    that rules out the fewest choices for the neighboring variables in the constraint graph
    are placed before others.
    """

    # used to sort domain by number of conflicts created
    valueToConflicts = [];
    for value in variable.domain:
        conflicts = 0;
        # check all neighbors for conflicts
        for arc in csp.constraints[variable].arcs():
            conflicts += arc[0].domain.count(value);
            conflicts += arc[1].domain.count(value);
        valueToConflicts.append([value, conflicts]);
        
    # sort by increasing order of conflicts created
    valueToConflicts = sorted(valueToConflicts, key=itemgetter(1));
    newDomain = [];
    for value in valueToConflicts:
        newDomain.append(value[0]);

    return newDomain

def ac3(csp, arcs=None):
    """Executes the AC3 or the MAC (p.218 of the textbook) algorithms.
    If the parameter 'arcs' is None, then this method executes AC3 - that is, it will check the arc consistency
    for all arcs in the CSP.  Otherwise, this method starts with only the arcs present in the 'arcs' parameter
    in the queue.
    Note that the current domain of each variable can be retrieved by 'variable.domains'.
    This method returns True if the arc consistency check succeeds, and False otherwise."""

    queue_arcs = deque(arcs if arcs is not None else csp.constraints.arcs())

    # loop through the arcs
    while (queue_arcs):
        arc = queue_arcs.popleft();
        # check if arc needs to be revised
        if (revise(csp, arc[0], arc[1])):
            # if no more in domain, arc consistency fails
            if (len(arc[0].domain) == 0 or len(arc[1].domain) == 0):
                return False;
            else :
                # loop through all arcs with arc[0]
                for neighbor in csp.constraints[arc[0]].arcs():
                    # skip if neighbor is the same arc
                    if (neighbor[0] == arc[1] or neighbor[1] == arc[1]):
                        continue;
                    # add arc to queue if current arc has been revised
                    queue_arcs.append(neighbor);
    return True;

def revise(csp, xi, xj):
    revised = False;
    # loop through domain of xi
    for xVal in xi.domain:
        found = False;
        # loop through domain of xj
        for yVal in xj.domain:
            # check if domain for xj satisfies constraints
            satisfied = True;
            for constraint in csp.constraints[xi, xj]:
                if (not constraint.is_satisfied(xVal, yVal)):
                    # satisfied is false if value of xj doesn't satisfy any of the constraints
                    satisfied = False;
                    break;
            # if any value of domain for xj is consistent, don't have to check any other values
            if (satisfied):
                found = True;
                break;
        # none of the domain of xj satisfies constraint with xi
        if (not found):
            xi.domain.remove(xVal);
            revised = True;
    return revised;
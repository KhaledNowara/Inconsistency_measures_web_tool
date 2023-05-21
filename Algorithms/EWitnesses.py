from z3 import *
from Algorithms.FOL import *
def FalseEWitness (Gamma):
    for i in Gamma:
        for j in Gamma: 
            clause1 = i.Factor()
            clause2 = j.Factor()

            if len(clause1.paramList) != 1 :
                break
            if len(clause2.paramList) != 1: 
                continue
             
            if clause1.paramList[0].GetPredicate().Unify(clause2.paramList[0].GetPredicate()):
                if (type(clause1.paramList[0]) != type(clause2.paramList[0])) : 
                    return True
    return False



def DecidableFragmentEwitness (Gamma):
        s = Solver()
        predecessor = True
        antecedent = True
        for clause in Gamma:
            predecessor = And (predecessor,clause.GetZ3clause())

        s.add(predecessor)

        return(s.check() == unsat)


def belongsEwitness (Gamma):
        
        for clause in Gamma: 
                # print(clause)
                if len(clause.paramList) == 1 and isinstance(clause.paramList[0],false):
                        return True
        return False

max_depth = 100000
def change_depth( n):
    global max_depth 
    max_depth = n
def print_depth():
    print(max_depth)
def resolutionTreeEwitness(clauses):
    tree = []
    queue = [(clause, None) for clause in clauses]  # each item in the queue is a tuple containing a clause and its parent node
    global max_depth
    while queue:
        clause1, parent = queue.pop(0)
        for clause2 in tree:
            resolvents = resolution(clause1, clause2)

            for resolvent in resolvents:
                if(resolvent == []):
                    return True
                if resolvent not in tree:
                    # add new clause to the proof tree and the queue
                    if len(tree) >= max_depth:
                        return False
                    tree.append(resolvent)
                    queue.append((resolvent, len(tree)-1))
        if clause1 not in tree:
            # add new clause to the proof tree
            tree.append(clause1)
            if parent is not None:
                # add edge from parent to new clause
                tree[parent]['children'].append(len(tree)-1)
                # mark parent as resolved
                tree[parent]['resolved'] = True
            # add new clause to the queue
            queue += [(clause1, len(tree)-1)]
    # no contradiction found: proof is incomplete
    return False

def resolution(clause1, clause2):
    resolvents = []
    clause1 = clause1.Factor()
    clause2 = clause2.Factor()

    for literal1 in clause1.paramList :
        for literal2 in clause2.paramList:
            if literal1.GetPredicate().name == literal2.GetPredicate().name and type(literal1) != type (literal2):
               if  literal1.GetPredicate().Unify(literal2.GetPredicate()) :
                    resolvent = clause1.paramList + clause2.paramList 
                    resolvent.remove(literal1)
                    resolvent.remove(literal2)
                    if(len(resolvent) > 0 ):
                        resolvents.append(Disjunction(resolvent).Factor())
                    else :
                        resolvents.append([])
    return resolvents

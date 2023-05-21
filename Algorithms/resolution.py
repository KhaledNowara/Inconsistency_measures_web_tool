from Algorithms.FOL import *

def resolutionTreeEwitness(clauses, max_depth = 100):
    tree = []
    queue = [(clause, None) for clause in clauses]  # each item in the queue is a tuple containing a clause and its parent node
   
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


# clauses = [Disjunction([Predicate('works',[Variable('x')]),Predicate('wo',[Variable('x')])]),Disjunction([  Negation ([ Predicate('works',[Variable('x'), ])]) ]), Disjunction([Negation ([ Predicate('wo',[Variable('x')]) ])])]

# x = Variable('x')
# y = Variable('y')
# z = Variable('z')

# nono = Constant('Nono')
# m1 = Constant('M1')
# west = Constant('West')
# america = Constant('America ')

# p1 = Predicate('American',[x])
# p2 =  Predicate('Weapon',[y])
# p3 = Predicate('Sells',[x,y,z])
# p4 = Predicate('Hostile',[z])
# p5 = Predicate('Criminal',[x])

# l1 = Negation([p1])
# l2 = Negation([p2])
# l3 = Negation([p3])
# l4 = Negation([p4])
# l5 = Negation([p5])

# c1 = Disjunction([l1,l2,l3,l4,l5])

# p6 = Predicate('Missile',[x])
# p7 = Predicate('Owns',[nono,x])
# p8 = Predicate('Sells',[west,x,nono])


# l6 =  Negation([p6])
# l7 = Negation([p7])

# c2 = Disjunction([l6,l7,p8]) 

# p9 = Predicate('Enemy',[x,america])
# p10 = Predicate('Hostile',[x])

# l8  = Negation([p9])

# c3 = Disjunction([l8,p10])


# p11 =  Predicate('Weapon',[x])
# p12 = Predicate('Missile',[x])
# l9 = Negation([p12])

# c4 = Disjunction([l9,p11])



# p13 = Predicate('Owns',[nono,m1])

# p14 = Predicate('American',[west])

# p15 = Predicate('Missile',[m1])

# p16 = Predicate('Enemy',[nono,america])

# p17 = Predicate('Criminal',[west])

# l10 = Negation([p17])


# exampleProof = [c1,Disjunction([l10]),Disjunction([p14]),c4,c2,c3,Disjunction([p13]),Disjunction([p15]),Disjunction([p16])]







# tree = resolution_proof_tree(exampleProof)
# print(tree[0].__str__())

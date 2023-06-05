from z3 import *
from Algorithms.FOL import *
from Algorithms.Marko import parser

class Complementary :
     
    
    def check (Gamma, phi = false ()):
        if not isinstance (phi, false):
             return false
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



class Mpc :
    def check (Gamma , phi = false ()):
            s = Solver()
            predecessor = True
            antecedent = True
            for clause in Gamma:
                predecessor = And (predecessor,clause.GetZ3clause())

        
            s.add(predecessor)
            s.add (Negation([phi]).PushNegation().GetZ3clause())

            return(s.check() == unsat)


class Membership :
    def check (Gamma, phi = false ()):
            clause2 = phi.GetDisjunction()[0]
            for clause1 in Gamma: 
                for literal1 in clause1.paramList :
                    for literal2 in clause2.paramList:
                        if literal1.GetPredicate().name == literal2.GetPredicate().name and type(literal1) == type (literal2):
                           if  literal1.GetPredicate().Unify(literal2.GetPredicate()) :
                               return True
            return False

class Resolution :
    max_depth = 100000
    def change_depth( n): 
       Resolution.max_depth = n
    def check(clauses, phi = false()):
        # print (phi)
        clauses = clauses.copy()
        negation_resolvent = (Negation([phi]).PushNegation()).GetDisjunction()
        clauses.update(negation_resolvent)
        tree = []
        queue = [(clause, None) for clause in clauses]  # each item in the queue is a tuple containing a clause and its parent node
        while queue:
            clause1, parent = queue.pop(0)
            for clause2 in tree:
                resolvents = Resolution.resolution(clause1, clause2)

                for resolvent in resolvents:
                    if(resolvent == []):
                        return True
                    if resolvent not in tree:
                        # add new clause to the proof tree and the queue
                        if len(tree)  >= Resolution.max_depth:
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

class Deduction_Theorem :
    

    def __init__(self,witness) :
        self.witness = witness
    def check ( self, Delta,phi = false()):

        for psi in Delta:
                # not psi of phi
                # print (psi)
                if self.witness ( Delta - {psi} ,Disjunction ([Negation([psi]).PushNegation(),phi])):
                    return True
                if self.witness ( Delta, Disjunction ([Negation([psi]).PushNegation(),phi])):
                    return True


        return False 
    
class Cut1 :

    def __init__(self,witness1,witness2, f) :
        self.witness1 = witness1
        self.witness2 = witness2
        self.f = f.splitlines()

    def check (self, Gamma, phi = false() ):
        found = False
        for Delta in self.f:
                Delta_adjusted = parser (Delta)  
                if self.witness1(Delta_adjusted,phi): 
                    found = True
                    for delta in Delta:
                            if not (self.witness2(Gamma,delta)):
                                found = False
                    if found :
                        return True

        return False

class Cut2 :

    def __init__(self,witness1,witness2, f) :
        self.witness1 = witness1
        self.witness2 = witness2
        self.f = f.splitlines()

    def check(self,Gamma,phi = false ()):
        for psi in self.f:
                if self.witness2(Gamma,psi):
                    if self.witness2(Gamma + psi,phi):
                        return True
        return False    
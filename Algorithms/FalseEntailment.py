from  Algorithms.FOL import *

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



# jenny = [Disjunction([Predicate('Works',[Variable('x')])]),Disjunction([Predicate('Works',[Variable('')])])]         
# clauses = [Disjunction([Predicate('works',[Variable('x')]),Predicate('wo',[Variable('x')])]),Disjunction([  Negation ([ Predicate('works',[Variable('x'), ])]) ]), Disjunction([Negation ([ Predicate('wo',[Variable('x')]) ])])]

# print(FalseWitness(clauses))
from z3 import *
from Algorithms.FOL import *
def DecidableFragmentEwitness (Gamma):
        s = Solver()
        predecessor = True
        antecedent = True
        for clause in Gamma:
            predecessor = And (predecessor,clause.GetZ3clause())

        s.add(predecessor)

        return(s.check() == unsat)


# clauses = [Disjunction([Predicate('works',[Variable('x')]),Predicate('wo',[Variable('x')])]),Disjunction([ Negation ([ Predicate('works',[Variable('x'), ])]) ]), Disjunction([Negation ([ Predicate('woo',[Variable('x')]) ])])]

# print(DecidableFragmentEwitness(clauses))
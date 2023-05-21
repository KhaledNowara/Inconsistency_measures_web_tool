from Algorithms.FOL import false
def belongsEwitness (Gamma):
        for clause in Gamma: 
                if isinstance(clause,false):
                        return True
        return False
# Gamma = {frozenset([1,2,3]),frozenset([-1,2]),frozenset([4,2,-2]),frozenset([5,3,2])}
# sigma = {frozenset([1,2,3]),frozenset([1,3])}

# print(belongsEwitness(Gamma,sigma))
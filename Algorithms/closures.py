#  how to do the formatting of inputs and outputs 

import itertools

def algorithm1 (e1, Delta, phi):

    for psi in Delta:
            # not psi of phi
            if e1 ( Delta - psi ,phi):
                return True
            if e1 ( Delta, phi):
                return True


    return False 

# how to create F belongs to F in L 
def algorithm2(e1,e2,Gamma,phi,f ):
    found = False
    for Delta in f: 
            if e1(Delta,phi): 
                found = True
                for j in range(len(Delta) + 1):
                    for delta in itertools.combinations(Delta,j):
                        if not (e2(Gamma,delta)):
                            found = False
                if found :
                    return True

    return False
# hot to create PHi belongs to F in LN
def algorithm3(e1,e2,Gamma,phi,Phi):
    for psi in Phi:
            if e2(Gamma,psi):
                if e1(Gamma + psi,phi):
                    return True
    return False    
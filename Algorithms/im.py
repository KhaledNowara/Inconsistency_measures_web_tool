import subprocess
import time
from Algorithms.SC import *
from Algorithms.Marko import *
from Algorithms.EWitnesses import *
# from Algorithms.decidableFOL import DecidableFragmentEwitness

def Drastic (filename,Ewitness):

    return (get_Drastic(filename,Ewitness)) 
 


def MI (filename,Ewitness):

    return len( Marco(filename,Ewitness)[1])
 


def MIC(filename,Ewitness):
    mus = Marco(filename,Ewitness)[1]

    Sum = sum(1/(len(x.data)) for x in mus)

    return Sum

def MC (filename,Ewitness):
    mss = Marco(filename,Ewitness)[0]
    sc = get_SC(filename,Ewitness)
    return len (mss) + len(sc) - 1



def problematic(filename,Ewitness):
    mus = Marco(filename,Ewitness)[1]
    inconsistent_sets_members = set().union(*[set(x.data) for x in mus])
    return len(inconsistent_sets_members)


# print(MIC("Algorithms/test/t.txt",DecidableFragmentEwitness))
# Marko.Marco("tests/test5.cnf")

witness_map = {
    'Complementary': Complementary.check,
    'Mpc': Mpc.check,
    'Membership': Membership.check,
    'Resolution' : Resolution.check,

}

measure_map = {
    'drastic': Drastic,
    'mi': MI,
    'mic': MIC,
    'mc': MC,
    'prob' : problematic,

    
}
def run_measures(kb, measures, witnesses,res_depth):
 

    results = []
    times = []
    Resolution.change_depth(int(res_depth))
    for witness in witnesses:
        result = [witness]
        t = [witness]
        for measure in measures:
       

            start_time = time.time()
            value = measure_map.get(measure)(kb,witness_map.get(witness))
            end_time = time.time()
            elapsed_time_ms = (end_time - start_time) * 1000
            result.append(value)
            t.append(elapsed_time_ms)
        
        results.append(result)
        times.append(t)
    return [results,times]
   

def ohoy (): 
    pass
    # try:
    #    print(run_measures("P  ) \n Q fe asd( x ) \n  ( Not P ( x ) ) \n F ( x ) ",["mi"],["resolution"],0 ))
    # except Exception as e:
    #     print (e)
    # print ("ohoy")



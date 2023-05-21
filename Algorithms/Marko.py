import itertools
from z3 import *
from Algorithms.FOL import *
# from FalseEntailment import resolutionTreeEwitness
# from Algorithms.decidableFOL import DecidableFragmentEwitness
# from Algorithms.resolution import resolutionTreeEwitness
class Node:
    def __init__(self,data,parents):
        self.data = data
        self.parents = parents
        self.children = []

    def __str__(self):
        return self.data.__str__()
    

def parser (filename):
     my_set = set()
     _id  = 0
     lines = filename.splitlines()
     
    #  with open(filename, "r") as f:
    #     try : 
    #         lines = f.readlines()
     for line in lines:
         folClause = interpreter(line,_id )
         folClause = folClause.Eliminate().PushNegation().Standardize().Distribute().Flatten().GetDisjunction()
         my_set.update(folClause)
         _id  += 1

        # except ValueError:
        #     print(f"Error parsing line: {line}")    
     return my_set 


# my_set = {frozenset([1]),frozenset([-1]),frozenset([2]),frozenset([-2]),frozenset([1,2])}

# for clause in my_set:
#     for c in clause:
#         print(clause.__le__)

# Loop through all subsets of the set
# for i in range(len(my_set)+1):
#     for subset in itertools.combinations(my_set, i):
#         print(subset)




# nextNodes = [lastNode]
# while (nextNodes != []):
#     loopNode = nextNodes.pop(0)
#     print(loopNode.data)
#     for parent in loopNode.parents:
#         if not parent in nextNodes:
#             nextNodes.append(parent)

def check(clauses,witness):
    return not  witness(clauses)


def shrink(node,allNodes,witness):
    while not check(node.data,witness):
        newNode = False
        for parent in node.parents:
            if not check(parent.data,witness):
                if parent in allNodes:
                    allNodes.remove(parent)
                node = parent
                newNode = True
                break
        if not newNode : 
            break
        
    
    return node 


def Marco(filename,witness):
    previousLevel= []
    currentLevel = []
    allNodes = []
    initialNode = None
    my_set =  parser(filename)
    for i in range(len(my_set)+1):
        for subset in itertools.combinations(my_set,i):
            if i == 0 :
                initialNode = Node(set(subset),[])
                currentLevel.append(initialNode)
                allNodes.append(initialNode)
            else:
                parents = []
                for node in previousLevel:
                    if node.data.issubset(set(subset)) or not node.data:
                        parents.append(node)
                currentNode = Node (set(subset),parents)
                for node in parents:
                    node.children.append(currentNode)
                currentLevel.append(currentNode)
                allNodes.append(currentNode)

        previousLevel = currentLevel
        currentLevel = []


    mss = set()
    mus = set()
    while allNodes:
        seed = allNodes.pop()
        # check satifiability
        if check(seed.data,witness) :
            mss.add(seed)
            blockDown = [seed]
            
            while blockDown:
                currentNode = blockDown.pop()
                for parent in currentNode.parents: 
                    if parent in allNodes:
                        allNodes.remove(parent)
                    blockDown.append(parent)
        else:
            mus.add(shrink(seed,allNodes,witness))

    # for node in mss:
    #     unique_clauses = {}
    #     for clause in node.data:
    #         unique_clauses[clause._id ] = clause
    #     node.data = set(unique_clauses.values())

    # for node in mus:
    #     unique_clauses = {}
    #     for clause in node.data:
    #         unique_clauses[clause._id ] = clause
    #     node.data = set(unique_clauses.values())

    return(mss,mus)

def get_SC(filename,witness):
    sc = []
    lines = filename.splitlines()
    for line in lines:
        folClause = interpreter(line,0 )
        folClause = folClause.Eliminate().PushNegation().Standardize().Distribute().Flatten().GetDisjunction()
        if (witness(folClause)):
            sc.append(folClause)
    return sc

def get_Drastic (filename,witness):
     my_set =  parser(filename)
     if  not check(set(my_set),witness):
         return 1
     else:
         return 0
     

# Marco("test/t.txt",DecidableFragmentEwitness)

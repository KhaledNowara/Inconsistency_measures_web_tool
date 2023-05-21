import abc
from z3 import *

ReplacementCode = -1

class Sentence :
    variables = []
    replacements = {}

class Universal(Sentence) :
    param = 2
    def __init__(self,  paramList,_id  = -1) -> None:
        self._id  = _id 
        self.sentence = paramList[1]
        self.variable = paramList[0]
    def __str__(self):
        return "Forall " + self.variable + " ( "  + self.sentence.__str__() + " ) "
    def Eliminate(self):
        return Universal([self.variable,self.sentence.Eliminate()],self._id  ) 
    def PushNegation (self):
        return Universal([self.variable,self.sentence.PushNegation()],self._id  )
    def Negate (self):
        return Existential([self.variable,self.PushNegation().sentence.Negate()],self._id  )
    def Standardize(self, replacements = {}):
            global ReplacementCode
            ReplacementCode += 1  
            replacements[self.variable] = 'x' + str(ReplacementCode)

            return  self.sentence.Standardize(replacements)

        


class Existential(Sentence):
    param = 2
    def __init__(self, paramList,_id  = -1) -> None:
        self._id  = _id 
        self.sentence = paramList[1]
        self.variable = paramList[0]
        
    def __str__ (self):
        return  "Exists " + self.variable + "( " +  self.sentence.__str__() + " )"
    def Eliminate(self):
        return Existential([self.variable,self.sentence.Eliminate()],self._id  ) 
    def PushNegation (self):
        return Existential([self.variable,self.sentence.PushNegation()],self._id  )
    def Negate (self):
        return Universal([self.variable,self.sentence.PushNegation().Negate()],self._id  )
    def Standardize(self, replacements = {}):
        global ReplacementCode
        ReplacementCode += 1
        replacements[self.variable] = Function(['F' + str(ReplacementCode),self.variable])
        return  self.sentence.Standardize(replacements)

class Equivalence:
    param = 2 
    def __init__(self, paramList,_id  = -1) -> None:
        self._id  = _id 
        self.sentence1 = paramList[0]
        self.sentence2 = paramList[1]
    def __str__ (self):
        return   "( " + self.sentence1.__str__() + "Equals" +  self.sentence2.__str__() +  " )"
    def Eliminate(self):
        P  = self.sentence1.Eliminate()
        Q = self.sentence2.Eliminate()
        notP = Negation([P])
        notQ = Negation([Q])
        return Disjunction([Conjunction([P,Q]),Conjunction([notP,notQ])],self._id  ) 

class Implication:
     param = 2 
     def __init__(self, paramList,_id  = -1) -> None:
        self._id  = _id 
        self.sentence1 = paramList[0]
        self.sentence2 = paramList[1]
     def __str__ (self):
         return " ( " + self.sentence1.__str__() + " Implies " +  self.sentence2.__str__() + " ) "
     def Eliminate(self):
        return Disjunction([Negation([self.sentence1.Eliminate()]),self.sentence2.Eliminate()],self._id  )

class Disjunction: 
     param = 2
     def __init__(self, paramList,_id  = -1) -> None:
        self._id  = _id 
        self.paramList = paramList
     def __str__ (self):
         output = " ( "
         for i in range ( len(self.paramList) ):
             output += self.paramList[i].__str__()
             if i < len(self.paramList) - 1 :
                 output += " Or "
         output += " ) "

         return output
     def Eliminate(self):
        return Disjunction([self.paramList[0].Eliminate(),self.paramList[1].Eliminate()],self._id  ) 
     def PushNegation(self):
         return Disjunction([self.paramList[0].PushNegation(),self.paramList[1].PushNegation()],self._id  )
     def Negate(self):
        return Conjunction([self.paramList[0].PushNegation().Negate(),self.paramList[1].PushNegation().Negate()],self._id  )
     def Standardize (self,replacements = {}):
         return Disjunction([self.paramList[0].Standardize(replacements),self.paramList[1].Standardize(replacements)],self._id  )
     def Distribute (self, sentence = None):
         return self.paramList[0].Distribute(self.paramList[1])
     def Flatten(self): 

             flatList = []
             for i in range (len(self.paramList)) :
                 if type(self.paramList[i]) == type(self):
                    for param in self.paramList[i].Flatten().paramList:
                        flatList.append(param)
                 else:
                     flatList.append(self.paramList[i].Flatten())

             return Disjunction(flatList,self._id  )
     def GetDisjunction (self):
         return [self] 
    
     def GetZ3clause(self):
         
         c = False
         for literal in self.paramList:
            c = Or(c,literal.GetZ3clause())  
         return c
     
     def Factor (self):

         i = 0 
         while i < len(self.paramList):
             j = i+1
             while j <len(self.paramList):
                 if self.paramList[i].GetPredicate().Unify(self.paramList[j].GetPredicate()):
                     if type(self.paramList[i]) == type(self.paramList[j]) :
                        self.paramList.pop(j)
                 else : 
                     j +=1
             i +=1
         return Disjunction(self.paramList,self._id  )
class Conjunction: 
     
     param = 2
     def __init__(self, paramList,_id  = -1) -> None:
        self._id  = _id 
        self.paramList = paramList

     def __str__ (self):
         output = " ( "
         for i in range ( len(self.paramList) ):
             output += self.paramList[i].__str__()
             if i < len(self.paramList) -1 :
                 output += " And  "
         output += " ) "

         return output
     def Eliminate(self):
        return Conjunction([self.paramList[0].Eliminate(),self.paramList[1].Eliminate()],self._id  )
     def PushNegation(self):
         return Conjunction([self.paramList[0].PushNegation(),self.paramList[1].PushNegation()],self._id  )
     def Negate(self):
        return Disjunction([self.paramList[0].PushNegation().Negate(),self.paramList[1].PushNegation().Negate()],self._id  ) 
     def Standardize (self,replacements = {}):
         return Conjunction([self.paramList[0].Standardize(replacements),self.paramList[1].Standardize(replacements)],self._id  )
     def Distribute(self, sentence = None):
         if sentence == None:
            return Conjunction([self.paramList[0].Distribute(), self.paramList[1].Distribute()],self._id  )
         else:
            
            sent1 = Disjunction([self.paramList[0].Distribute(), sentence.Distribute()],self._id  )
            sent2 =   Disjunction([self.paramList[1].Distribute(), sentence.Distribute()],self._id  )
            return Conjunction([sent1,sent2],self._id  )
         
     def Flatten(self): 

             flatList = []
             for i in range (len(self.paramList)) :
                 if type(self.paramList[i]) == type(self):
                    for param in self.paramList[i].Flatten().paramList:
                        flatList.append(param)
                 else:
                     flatList.append(self.paramList[i].Flatten())

             return Conjunction(flatList,self._id  ) 
     
     def GetDisjunction (self):
         return self.paramList
     
     def GetZ3clause(self):
         
         c = True
         for literal in self.paramList:
            c = And(c,literal.GetZ3clause())  
         return c

class Negation: 
     param = 1
     def __init__(self, paramList,_id  = -1) -> None:
        self._id  = _id 
        self.sentence = paramList[0]
     def __str__ (self):
        return   " Not" + " ( " + self.sentence.__str__()+" ) "
     def Eliminate(self):
        return Negation([self.sentence.Eliminate()],self._id  ) 
     def PushNegation(self):
         return self.sentence.Negate()
     def Negate(self):
         return self.sentence
     def Standardize (self, replacements = {}):
         return Negation([self.sentence.Standardize(replacements)],self._id  )
     def Distribute (self, sentence = None):
        return self
     def Flatten(self):
         return self
     def GetDisjunction (self):
         return [Disjunction([self],self._id  )]
     def GetPredicate (self):
         return self.sentence 
     
     def GetZ3clause(self):
         return Not(self.sentence.GetZ3clause())
class Predicate:

    def __init__(self,   name, subjects,_id  = -1) :
        self._id  = _id 
        # subject is variable , constant or function
        self.name = name
        self.subjects = subjects

    def __str__(self) :
      subs = ''
      for i in self.subjects: 
          subs += i.__str__() + " , "
      return   self.name + " ( " + ' , '.join([subject.__str__() for subject in self.subjects]) + " ) " 
    def Eliminate(self):
        return self
    def PushNegation(self):
        return self
    def Negate(self):
        return Negation([self],self._id)
    def Standardize (self, replacements = {}) :
        for i  in range (len(self.subjects)):
            if self.subjects[i] in replacements:
                self.subjects[i] = replacements[self.subjects[i]]
                
        return Predicate(self.name,self.subjects,self._id  )
        
    def Distribute (self, sentence = None):
        if sentence == None:
            return self
        return Disjunction ([self,sentence],self._id)
    def Flatten(self):
        return self
    
    def GetDisjunction (self):
         return [Disjunction([self],self._id  )]
    
    def GetPredicate (self):
        return self

    def Unify (self, mate):
        if len(self.subjects) != len(mate.subjects) :
            return False
        if self.name != mate.name :
            return False 
        
        unifier = {}
        
        for i in range ( len(self.subjects)): 
            if not self.subjects[i].Unify(mate.subjects[i],unifier):
                return False
            
        for i in range ( len(self.subjects)): 
            while self.subjects[i].__str__() in unifier:
                self.subjects[i] = unifier[self.subjects[i].__str__() ]
            while mate.subjects[i].__str__() in unifier:
                mate.subjects[i] = unifier[mate.subjects[i].__str__() ]
        
        return True
    
    def GetZ3clause(self):
         subjectNames = "" 
         for subject in self.subjects:
             subjectNames += subject.GetZ3clause()
         return Bool(self.name + "_" + subjectNames)

class Variable: 

    def __init__(self, name,_id  = -1) -> None:
        self._id  = _id 
        self.name= name

    def __str__(self) -> str:
        return self.name
    def Unify ( self, mate, unifier  ): 
        real_mate = mate
        while  real_mate.__str__() in unifier :
            
            real_mate = unifier [real_mate.__str__()]
        real_self = self
        while  real_self.__str__() in unifier :
            real_self = unifier [real_self.__str__()]

        if (isinstance(real_self,Constant) and isinstance(real_mate,Constant) and real_self.__str__() != real_mate.__str__()):
            return False
        else: 
            if (real_self.__str__() != real_mate.__str__()):
                unifier[real_self.__str__()] = real_mate
            return True
    def GetZ3clause (self):
        return '**'

class Constant: 

    def __init__(self, name,_id  = -1) -> None:
            self._id  = _id 
            self.name= name

    def __str__(self) -> str:
        return "_" + self.name
    
    def Unify( self,mate,unifier):
        real_mate = mate
        while real_mate.__str__() in unifier :
            real_mate = unifier [real_mate.__str__()]
        real_self = self
        if (isinstance(real_mate,Constant)):
            if real_self.__str__() != real_mate.__str__():
                return False
            else:
                return True
        else : 
            return real_mate.Unify(self, unifier)

    def GetZ3clause (self):
        return self.name

class Function : 
     def __init__(self, params,_id  = -1) -> None:
            self._id  = _id 
            self.name= params[0]
            self.var = params[1]
     def __str__(self) :
      return   self.name + "(" + self.var + ") " 
     
     def Unify (self,mate,unifier):
        real_mate = mate
        while real_mate.__str__() in unifier :
            real_mate = unifier [real_mate.__str__()]
        real_self = self
        while real_self.__str__() in unifier :
            real_self = unifier [real_self.__str__()]

        if (isinstance(real_self,Constant) and isinstance(real_mate,Constant) and real_self.__str__() != real_mate.__str__()):
            return False
        else: 
            unifier[real_self.__str__()] = real_mate
            return True


class false:
    param = 0
    def __init__(self,_id  = -1) :
        self._id  = _id 
        self.name = "False"
        self.subjects = []
        # subject is variable , constant or function


    def __str__(self) :

      return "False"
    def Eliminate(self):
        return self
    def PushNegation(self):
        return self
    def Negate(self):
        return Negation([self],self._id)
    def Standardize (self, replacements = {}) :

                
        return self
        
    def Distribute (self, sentence = None):
        if sentence == None:
            return self
        return sentence
    def Flatten(self):
        return self
    
    def GetDisjunction (self):
         return [Disjunction([self],self._id  )]
    
    def GetPredicate (self):
        return self

    def Unify (self, mate):
       if isinstance(mate,false):
        return True
    
    def GetZ3clause(self):
         return False
    

class true:
    param = 0
    def __init__(self,_id  = -1) :
        self._id  = _id 
        self.name = "True"
        self.subjects = []
        # subject is variable , constant or function

    def __str__(self) :

      return "True"
    def Eliminate(self):
        return self
    def PushNegation(self):
        return self
    def Negate(self):
        return Negation([self],self._id)
    def Standardize (self, replacements = {}) :

                
        return self
        
    def Distribute (self, sentence = None):
        if sentence == None:
            return self
        return self
    def Flatten(self):
        return self
    
    def GetDisjunction (self):
         return [Disjunction([self],self._id  )]
    
    def GetPredicate (self):
        return self

    def Unify (self, mate):
       if isinstance(mate,false):
        return True
    
    def GetZ3clause(self):
         return True
    
function_map = {
    'And': Conjunction,
    'Or': Disjunction,
    'Implies': Implication,
    '=' : Equivalence,
    'Not' : Negation,
    'Forall' : Universal,
    'Exists' : Existential,
    'True' : true,
    'False' : false
    
}

def interpreter (sentence, _id  ):
    operand = []
    operator = []

    for token in sentence.split():
        if (token == '\n') : break
     
        if (token in function_map or token == "(" or token == ","):
            operator.append(token)
        elif (token ==")"):
            predicateSubjects = []
            while operator[len(operator)-1] == ',':
                operator.pop()
                currentSubject = operand.pop()
                if (currentSubject[0].isupper()):
                    predicateSubjects.insert(0,Constant(currentSubject,_id))
                else:
                    predicateSubjects.insert(0,Variable(currentSubject,_id))
            if (operator[len(operator)-1] == '('):
                operator.pop()
                currentSubject = operand.pop()
                if (currentSubject[0].isupper()):
                    predicateSubjects.insert(0,Constant(currentSubject,_id))
                else:
                    predicateSubjects.insert(0,Variable(currentSubject,_id))
                name = operand.pop()
                operand.append(Predicate(name,predicateSubjects,_id ))
            else:
                op = []
                cls = function_map.get(operator.pop())
                for i in range (cls.param):
                    op.insert(0 , operand.pop())
                if cls.param > 0 :
                    operand.append(cls(op,_id ))
                else:
                    operand.append(cls(_id ))
                # remove start bracket
        else :
            operand.append(token)
    return operand.pop()



Allanimals =   " ( Forall y (  Animal ( y )  Implies   Loves ( x  , y )  ) ) "

Somelove =  " ( Exists y  Loves ( y , x )  ) "

hoba = "  ( Forall x ( " + Allanimals + " Implies " + Somelove + " ) ) " 

mshFlat  = " (  And ( P ( x ) And ( P ( x ) And ( P ( x ) And ( P ( x ) And P ( x )  ) ) ) )"
# c = interpreter(mshFlat)


# # k = Universal(["", "world"])
# x = (c.Flatten())
# print(x)



# noone = Predicate("Works", [Constant('y'),Constant('z'),Constant('f'),Constant('x')])

# print(jennies.Factor())
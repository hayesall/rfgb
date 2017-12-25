from random import random
class State(object):
    '''generates a state with boxes and trucks'''

    def __init__(self,number):
        '''constructor'''

        self.action = "unload(s"+str(number)+",t)"

        if random() < 0.5:
            if random() < 0.5:
                self.state = ["bon(s"+str(number)+",b,t)",
                              "tin(s"+str(number)+",t,d1)",
                              "isd(s"+str(number)+",d1)",
                              "dname(s"+str(number)+",d1,c1)"]
            else:
                self.state = ["bon(s"+str(number)+",b,t)",
                              "tin(s"+str(number)+",t,d2)",
                              "isd(s"+str(number)+",d2)",
                              "dname(s"+str(number)+",d2,c2)"]
            self.destination = True
        else:
            self.state = ["bon(s"+str(number)+",b,t)",
                          "tin(s"+str(number)+",t,d3)",
                          "dname(s"+str(number)+",d3,c3)"]
            self.destination = False

def generateStates():
    '''generates N states with boxes and trucks'''
    N = 10
    facts,pos,neg = [],[],[]
    for i in range(N):
        s = State(i)
        if s.destination:
            pos.append(s.action)
        else:
            neg.append(s.action)
        for fact in s.state:
            facts.append(fact)
    with open("train/facts.txt","a") as fp:
        for fact in facts:
            fp.write(fact+"\n")
    with open("train/pos.txt","a") as fp:
        for ex in pos:
            fp.write(ex+"\n")
    with open("train/neg.txt","a") as fp:
        for ex in neg:
            fp.write(ex+"\n")
generateStates()
    
            

#if 3 blocks are stacked then put it down
from random import random

class State(object):
    '''generates states with 3 blocks or 4 blocks'''

    def __init__(self,number):
        '''constructor'''
        self.action = "putdown(s"+str(number)+")"
        if random() < 0.5:
            if random() < 0.5:
                self.state = ["ontable(s"+str(number)+",b1,table)",
                              "on(s"+str(number)+",b2,b1)",
                              "on(s"+str(number)+",b3,b2)"]
            else:
                self.state = ["ontable(s"+str(number)+",b1,table)",
                              "on(s"+str(number)+",b2,b1)",
                              "on(s"+str(number)+",b3,b2)",
                              "on(s"+str(number)+",b4,b3)"]
            self.threeStack = True
        else:
            self.state = ["ontable(s"+str(number)+",b1,table)",
                          "on(s"+str(number)+",b2,b1)"]
            self.threeStack = False

def generateStates():
    '''generates block stacks'''
    facts,pos,neg = [],[],[]
    for i in range(10):
        s = State(i)
        for fact in s.state:
            facts.append(fact)
        if s.threeStack:
            pos.append(s.action)
        else:
            neg.append(s.action)

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





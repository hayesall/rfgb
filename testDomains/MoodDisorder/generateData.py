from random import random
class Person(object):
    '''generates persons with mood disorders'''

    def __init__(self,number):
        '''constructor'''
        self.target = "bipolar(p"+str(number)+")"

        if random() < 0.5: #bipolar person
            self.facts = ["dep(p"+str(number)+")",
                          "agg(p"+str(number)+")",
                          "anxiety(p"+str(number)+")",
                          "abuse(p"+str(number)+")",
                          "heartrate(p"+str(number)+")",
                          "breathing(p"+str(number)+")",
                          "pattern(p"+str(number)+")",
                          "ego(p"+str(number)+")"]
        else: #PTSD person
            self.facts = ["dep(p"+str(number)+")",
                          "agg(p"+str(number)+")",
                          "anxiety(p"+str(number)+")",
                          "abuse(p"+str(number)+")",
                          "heartrate(p"+str(number)+")",
                          "breathing(p"+str(number)+")"]
        if random() < 0.5:
            self.prediction = True
        else:
            self.prediction = False

def generatePersons():
    '''generates N persons with mood disorders'''
    facts,pos,neg = [],[],[]
    N = 10
    for i in range(N):
        person = Person(i)
        if person.prediction:
            pos.append(person.target)
        else:
            neg.append(person.target)
        for fact in person.facts:
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
generatePersons()

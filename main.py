from __future__ import print_function

from Utils import Utils
from Tree import node
from Boosting import Boosting
from sys import argv

def main():
    '''main method'''
    targets = argv[argv.index("-target")+1][1:-1].split(',') #read targets from input
    regression,advice = False,False
    if "-reg" in argv:
        regression = True
    if "-expAdvice" in argv:
        advice = True
    for target in targets:
        data = Utils.readTrainingData(target,regression,advice) #read training data
        numberOfTrees = 2 #number of trees for boosting
        trees = [] #initialize place holder for trees
        for i in range(numberOfTrees): #learn each tree and update gradient
            print('='*20,"learning tree",str(i),'='*20)
            node.setMaxDepth(2)
            node.learnTree(data) #learn RRT
            trees.append(node.learnedDecisionTree)
            Boosting.updateGradients(data,trees)
        for tree in trees:
            print('='*30,"tree",str(trees.index(tree)),'='*30)
            for clause in tree:
                print(clause)
        testData = Utils.readTestData(target,regression) #read testing data
        Boosting.performInference(testData,trees) #get probability of test examples
        
        #print testData.pos #--> uncomment to see test query probabilities (for classification)
        #print testData.neg

        #print testData.examples #--> uncomment to see test example values (for regression)
        
main()

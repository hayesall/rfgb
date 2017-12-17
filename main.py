from Utils import Utils
from Tree import node
from Boosting import Boosting

def main():
    '''main method'''
    data = Utils.readTrainingData() #read training data
    numberOfTrees = 2 #number of trees for boosting
    trees = [] #initialize place holder for trees
    for i in range(numberOfTrees): #learn each tree and update gradient
        print '='*20,"learning tree",str(i),'='*20
        node.setMaxDepth(3)
        node.learnTree(data) #learn RRT
        trees.append(node.learnedDecisionTree)
        Boosting.updateGradients(data,trees)
    for tree in trees:
        print '='*30,"tree",str(trees.index(tree)),'='*30
        for clause in tree:
            print clause
    testData = Utils.readTestData() #read testing data
    Boosting.performInference(testData,trees) #get probability of test examples
    for posEx in testData.pos:
        print testData.pos[posEx]
        break
    for negEx in testData.neg:
        print testData.neg[negEx]
        break
    #print testData.pos --> uncomment to see test query probabilities
    #print testData.neg
main()

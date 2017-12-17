from Utils import Utils
from Tree import node
from Boosting import Boosting

def main():
    '''main method'''
    data = Utils.readTrainingData() #read training data
    numberOfTrees = 1 #number of trees for boosting
    trees = [] #initialize place holder for trees
    for i in range(numberOfTrees): #learn each tree and update gradient
        node.setMaxDepth(4)
        node.learnTree(data) #learn RRT
        trees.append(node.learnedDecisionTree)
        Boosting.updateGradients(data,trees)
    for tree in trees:
        for clause in tree:
            print clause
    testData = Utils.readTestData() #read testing data
    Boosting.performInference(testData,trees) #get probability of test examples
    #print testData.pos --> uncomment to see test query probabilities
    #print testData.neg
main()

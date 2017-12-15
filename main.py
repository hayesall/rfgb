from Utils import Utils
from Tree import node
from Boosting import Boosting

def main():
    '''main method'''
    data = Utils.readTrainingData() #read training data
    numberOfTrees = 2 #number of trees for boosting
    trees = [] #initialize place holder for trees
    for i in range(numberOfTrees): #learn each tree and update gradient
        node.setMaxDepth(4)
        node.learnTree(data) #learn RRT
        trees.append(node.learnedDecisionTree)
        Boosting.updateGradients(data,trees)
        print data.pos
        print data.neg
        exit()
main()

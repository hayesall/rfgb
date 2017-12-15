from Utils import Utils
from Tree import node

def main():
    '''main method'''
    data = Utils.readTrainingData() #read training data
    node.learnTree(data) #learn RRT
    node.setMaxDepth(2)
    print node.learnedDecisionTree
main()

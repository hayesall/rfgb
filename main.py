from Utils import Utils
from Tree import node

def main():
    '''main method'''
    data = Utils.readTrainingData() #read training data
    node.setMaxDepth(3)
    node.learnTree(data) #learn RRT
    print node.learnedDecisionTree
main()

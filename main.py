from Utils import Utils
from Tree import node
from Boosting import Boosting
from sys import argv

def main():
    '''main method'''
    targets = argv[argv.index("-target")+1][1:-1].split(',') #read targets from input
    regression = False
    if "-reg" in argv:
        regression = True
    for target in targets:
        if regression:
            data = Utils.readTrainingData(target,regression = True) #read training data
        else:
            data = Utils.readTrainingData(target)
        numberOfTrees = 2 #number of trees for boosting
        trees = [] #initialize place holder for trees
        for i in range(numberOfTrees): #learn each tree and update gradient
            print '='*20,"learning tree",str(i),'='*20
            print "current values: ",[data.getValue(example) for example in data.examples]
            node.setMaxDepth(2)
            node.learnTree(data) #learn RRT
            trees.append(node.learnedDecisionTree)
            print "tree: ",node.learnedDecisionTree
            print "true values: ",[data.getExampleTrueValue(example) for example in data.examples]
            Boosting.updateGradients(data,trees)
            print "gradients: ",data.examples
            raw_input()
        for tree in trees:
            print '='*30,"tree",str(trees.index(tree)),'='*30
            for clause in tree:
                print clause
        if regression:
            testData = Utils.readTestData(target,regression = True) #read testing data
        else:
            testData = Utils.readTestData(target)
        Boosting.performInference(testData,trees) #get probability of test examples
        
        #print testData.pos #--> uncomment to see test query probabilities (for classification)
        #print testData.neg

        #print testData.examples #--> uncomment to see test example values (for regression)
        
main()

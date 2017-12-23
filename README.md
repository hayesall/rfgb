# RFGB
Developing gradient boosting for relational data


**To run regression:**


1. Copy a regression example from test domains both train and test (ex: Boston Housing) to same directory as the python files or you can write your own.

2. Run command: *python main.py -target <list of target(s)> -reg*

3. For the insurance example: python main.py -target [value] -reg


**To run classification:**


1. Copy a classification example from test domains both train and test (ex: Toy Cancer) to same directory as .py files or you can write your own.

2. Run command: *python main.py -target <list of target(s)>*

3. For the TicTacToe example: python main.py -target [put,dontput]

**To run classification with expert advice:**

1. Copy an expert advice based classification example from test domains both train and test (for now heart attack) to same directory as .py files or you can write your own.

2. Include advice.txt file in train folder

3. The file contains pieces of advice of the form: *advice clause <list of preferred target(s)> <list of non preferred target(s)>*
  
4. Run command: *python main.py -target <list of target(s)> -expAdvice*
  
5. For the HeartAttack example: python main.py -target [ha] -expAdvice


**Still in development, pending -> further testing, commenting, cleaning up code and adding more functionality such as MLN learning, soft margin etc.**

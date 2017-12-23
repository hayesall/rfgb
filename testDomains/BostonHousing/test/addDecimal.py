newExampleLines = []
with open("examples.txt") as fp:
    exampleLines = fp.read().splitlines()
    for line in exampleLines:
        if len(line.split(' ')[1]) > 2:
            newExampleLines.append(line[:-1]+"."+line[-1])
        else:
            newExampleLines.append(line)

with open("modExamples.txt","a") as fp:
    for line in newExampleLines:
        fp.write(line+"\n")
    

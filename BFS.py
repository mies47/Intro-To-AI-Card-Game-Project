import copy
import time
import re
import sys

class Card:
    'class for each card with its color and number'
    def __init__(self , numColor:str):
        self.number , self.color = self.splitNumColor(numColor)
        self.number = int(self.number)

    def splitNumColor(self , numColor:str):
        return tuple(re.split('(\d+)',numColor)[1:])

    def __eq__(self , other):
        if not isinstance(other, Card):
            return False
        return (self.number == other.number and self.color == other.color)

    def __hash__(self):
        return hash((self.number , self.color))

def canBeAdded(listToAdd: list , card: Card):
    'Check to see if "card" can be added to pile "listToAdd"'
    if(len(listToAdd) > 0 and listToAdd[len(listToAdd) - 1].number <= card.number):
        return False
    else:
        return True

def sameColor(listOfCards: list):
    'Check to see if all cards in the list are of the same color'
    for i in range(1 , len(listOfCards)):
        if(listOfCards[i].color != listOfCards[i-1].color):
            return False                    
    return True

def trueOrder(listOfCards: list):
    'Check to see if all cards in the list are in descending order'
    for i in range(len(listOfCards) - 1):
        if(listOfCards[i].number < listOfCards[i+1].number):
            return False                    
    return True

def getTopCard(listOfCards: list):
    'Return the top card of list or if it is empty return False'
    if(len(listOfCards) > 0):
        return listOfCards[len(listOfCards) - 1]
    else:
        return False 


class State:
    'A class to represent each state with its depth parent and action taken to get from parent to this state'
    def __init__(self , listState: list ,parent , action:str = None):
        self.stateList = listState
        self.parent = parent
        self.action = action
        if(parent):
            self.depth = parent.depth + 1
        else:
            self.depth = 0 

    def addAction(self , action):
        'change the action of this state'
        self.action = action           

    def __eq__(self , other):
        if not isinstance(other, State):
            return False
        if(self.stateList != other.stateList):
            return False
        return True         

    def __hash__(self):
        x = []
        for i in self.stateList:
            for j in i:
                x.append(j)    
        return hash(tuple(x))  


def goalTest(state: list):
    for statePart in state:
        if( not (sameColor(statePart) and trueOrder(statePart))):
            return False
    return True   

class BFS:
    def __init__(self , partNum ,colorNum, initialList):
        self.initialState = []
        self.colorNum = colorNum
        self.partNum = partNum
        self.frontier = []
        self.visited = set()
        self.stateAction = {}
        self.currentState = None
        self.expandedNodes = 0
        self.createdNodes = 0
        for i in initialList:
            temp = []
            self.initialState.append(temp)
            for j in i:
                if(j != '#'):
                    temp.append(Card(j))
     
    

    def breadthFirstSearch(self):
        if(self.colorNum > self.partNum or self.partNum != len(self.initialState)):
            return "Failure"
        self.currentState = State(copy.copy(self.initialState) , None)
        if(goalTest(self.currentState.stateList)):
            return self.currentState
        self.frontier.append(copy.copy(self.currentState))

        while True:
            if(len(self.frontier) == 0):
                return 'Failure'
            x = self.frontier.pop(0)
            self.expandedNodes += 1
            self.currentState = x
            lastState = copy.deepcopy(self.currentState)
            self.stateAction.update({lastState : lastState.action})
            self.visited.add(lastState)
            for i in range(len(self.currentState.stateList)):
                for j in range(len(self.currentState.stateList)):
                    if( j != i):
                        topCard = getTopCard(self.currentState.stateList[i])
                        if(topCard and canBeAdded(self.currentState.stateList[j] ,topCard)):
                            self.currentState.stateList[j].append(self.currentState.stateList[i].pop())
                            self.createdNodes += 1
                            if((not self.currentState in self.visited) and (not self.currentState in self.frontier)):
                                self.currentState.addAction("Moved Card %d%s From Pile %d To Pile %d" % ( topCard.number ,topCard.color , i+1 ,j + 1))
                                self.currentState.depth = lastState.depth + 1
                                if(goalTest(self.currentState.stateList)):
                                    self.currentState.parent = lastState    
                                    self.stateAction.update({self.currentState: self.currentState.action})
                                    return self.currentState
                                self.currentState.parent = lastState    
                                self.frontier.append(copy.copy(self.currentState)) 
                            self.currentState = copy.deepcopy(lastState)

def findInFile():
    fo = open('test.txt' , 'r')
    k , m , n = 0 , 0 , 0
    inputList = []
    for i in enumerate(fo.readlines()):
        if(i[0] != 0):
            x = i[1].strip().split(' ')
            inputList.append(x)
        else:
            temp = i[1].strip().split(' ')
            k , m , n = int(temp[0]) , int(temp[1]) , int(temp[2])
    fo.close()        
    return k , m , n , inputList        


k , m , n , inputList = findInFile()
bfs = BFS(k , m , inputList)
startTime = time.time()
state = bfs.breadthFirstSearch()
endTime = time.time()
print("\nElapsed Time is: %s minutes and %s seconds" % (int((endTime - startTime) // 60)  ,float((endTime - startTime) % 60)))
print('\n``````````````````````````````````````````````````````````````````````````````````````````````````')
if(state == "Failure"):
    print("Search Failed!!")
    sys.exit(1)
else:
    print("Final State Is:\n")
    tempState = state
    for j in tempState.stateList:
        if(len(j) == 0):
            print("#" , end="")
        for x in j:
            print("%d%s " % (x.number , x.color) , end=""),
        print('\n')   
    print('``````````````````````````````````````````````````````````````````````````````````````````````````')  
    print('Actions:')
    actions = []  
    while tempState.parent != None:
        actions.append(bfs.stateAction.get(tempState))         
        tempState = tempState.parent
    actions.reverse()
    for ac in actions:     
        print(ac) 
print('\n``````````````````````````````````````````````````````````````````````````````````````````````````')
print("Depth is: %d" % state.depth)
print('\n``````````````````````````````````````````````````````````````````````````````````````````````````')
print("Created Nodes Are: %d" % bfs.createdNodes)
print('\n``````````````````````````````````````````````````````````````````````````````````````````````````')
print("Expanded Nodes Are: %d" % bfs.expandedNodes)
print('\n``````````````````````````````````````````````````````````````````````````````````````````````````')




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

class IDS:
    def __init__(self , partNum ,colorNum, initialList , initialLimit):
        self.initialState = []
        self.colorNum = colorNum
        self.initialLimit = initialLimit
        self.partNum = partNum
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
     
    def recursive_DLS(self , state: State , limit: int):
        if(goalTest(state.stateList)): return state
        elif(limit == 0): return "cutoff"
        else:
            cutoff_occured = False
            alreadyAdded = False
            self.currentState = copy.deepcopy(state)
            for i in range(len(state.stateList)):
                for j in range(len(state.stateList)):
                    if( j != i):
                        topCard = getTopCard(state.stateList[i])
                        if(topCard and canBeAdded(state.stateList[j] ,topCard)):
                            if(not alreadyAdded):
                                self.expandedNodes += 1
                                alreadyAdded = True
                            self.currentState.addAction("Moved Card %d%s From Pile %d To Pile %d" % ( topCard.number ,topCard.color , i+1 ,j + 1))
                            self.currentState.stateList[j].append(self.currentState.stateList[i].pop())
                            self.currentState.parent = state
                            self.currentState.depth += 1
                            self.stateAction.update({self.currentState: self.currentState.action}) 
                            self.createdNodes += 1
                            result = self.recursive_DLS(self.currentState , limit - 1)
                            if result == "cutoff" : cutoff_occured = True
                            elif result != "Failure" : return result
                            self.currentState = copy.deepcopy(state)
            if cutoff_occured : return "cutoff"
            else : return "Failure"                

    
    def depth_limited_search(self, limit: int):
        return self.recursive_DLS(State(self.initialState , None) , limit)

    def iterative_deepening_search(self):
        if(self.colorNum > self.partNum or self.partNum != len(self.initialState)):
            return "Failure"
        limit = self.initialLimit
        while 1:
            result = self.depth_limited_search(limit)
            if result != "cutoff" : return result
            limit += 1
            self.stateAction = {}

    


    
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
initialLimit = int(input())
ids = IDS(k , m , inputList , initialLimit)
startTime = time.time()
state = ids.iterative_deepening_search()
endTime = time.time()
print('``````````````````````````````````````````````````````````````````````````````````````````````````')
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
        actions.append(tempState.action)         
        tempState = tempState.parent
    actions.reverse()
    for ac in actions:     
        print(ac) 
print('\n``````````````````````````````````````````````````````````````````````````````````````````````````')
print("Depth is: %d" % state.depth)
print('\n``````````````````````````````````````````````````````````````````````````````````````````````````')
print("Created Nodes Are: %d" % ids.createdNodes)
print('\n``````````````````````````````````````````````````````````````````````````````````````````````````')
print("Expanded Nodes Are: %d" % ids.expandedNodes)
print('\n``````````````````````````````````````````````````````````````````````````````````````````````````')




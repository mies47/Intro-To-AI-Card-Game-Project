import cards
class Part:
    def __init__(self , maxnum):
        self.stack = []
        self.maxnum = maxnum
    
    def addCard(self ,card , start):
        if(not start and len(self.stack) > 0 and self.stack[len(self.stack) - 1].number <= card.number):
            return False
        else:
            self.stack.append(card)
            return True

    def removeCard(self , card , canBeMoved):
        if(canBeMoved):
            self.stack.pop()
            return True
        else:
            return False

    def sameColor(self):
        for i in range(1 , len(self.stack)):
            if(self.stack[i].color != self.stack[i-1]):
                return False                    
        return True

    def trueOrder(self):
        for i in range(len(self.stack)):
            if(self.stack[i].number != i+1):
                return False                    
        return True

    def __eq__(self , other):
        if not isinstance(other, Part):
            return False
        if(len(other.stack) != len(self.stack)):
            return False
        else:
            for i in range(len(other.stack)):
                if(other.stack[i] != self.stack[i]):
                    return False
            return True               

    def __hash__(self):
        return hash(self.stack)
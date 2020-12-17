import re
class Card:
    'class for each card with its color and number'
    def __init__(self , numColor):
        self.number , self.color = self.splitNumColor(numColor)
        self.number = int(self.number)

    def splitNumColor(self , numColor):
        return tuple(re.split('(\d+)',numColor)[1:])

    def __str__(self):
        return 'Card (%d , %s)' % (self.number, self.color)

    def __eq__(self , other):
        if not isinstance(other, Card):
            return False
        return (self.number == other.number and self.color == other.color)

    def __hash__(self):
        return hash((self.number , self.color))
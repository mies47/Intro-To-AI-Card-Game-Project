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

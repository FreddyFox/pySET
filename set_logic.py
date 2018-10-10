from enum import Enum
import random

class Color(Enum):
	red = 1
	green = 2
	blue = 3

class Shape(Enum):
	circle = 1
	triangle = 2
	square = 3

class Number(Enum):
	one = 1
	two = 2
	three = 3

class Fill(Enum):
	full = 1
	half = 2
	none = 3

class Card(object):
	def __init__(self, _color, _shape, _number, _fill):
		self.color = _color
		self.shape = _shape
		self.number = _number
		self.fill = _fill

	def __str__(self):
		return str(Color(self.color))+','+str(Shape(self.shape))+','+str(Number(self.number))+','+str(Fill(self.fill))

	def getColor(self):
		return self.color

	def getShape(self):
		return self.shape

	def getNumber(self):
		return self.number

	def getFill(self):
		return self.fill

	def getAttributes(self):
		return [self.getColor(), self.getShape(), self.getNumber(), self.getFill()]

class Deck(object):
	def __init__(self, number_of_attributes=4):
		self.attributes = [Color, Shape, Number, Fill]
		attributes = [[self.attributes[i](1)] for i in range(4)]
		for i in range(number_of_attributes):
			attributes[i] = self.attributes[i]
		self.cards = [Card(color, shape, number, fill) 
						for color in attributes[0] 
						for shape in attributes[1]
						for number in attributes[2]
						for fill in attributes[3]]

	def shuffle(self):
		random.shuffle(self.cards)

	def getCards(self):
		return self.cards

	def drawCards(self, num_of_cards):
		cards = self.cards[-num_of_cards:]
		self.cards = self.cards[:-num_of_cards]
		return cards

	def isEmpty(self):
		if len(self.cards) == 0: return True
		else: return False

class Set(object):
	def __init__(self, _card1, _card2, _card3):
		self.card1 = _card1
		self.card2 = _card2
		self.card3 = _card3

		self.attributes = ["color","shape","number","fill"]

	def isAttributeValid(self, attribute):
		if (getattr(self.card1, attribute) == getattr(self.card2, attribute) and getattr(self.card2, attribute) == getattr(self.card3, attribute)) \
		or (getattr(self.card1, attribute) != getattr(self.card2, attribute) and getattr(self.card2, attribute) != getattr(self.card3, attribute) \
		and getattr(self.card1, attribute) != getattr(self.card3, attribute)):
			return True
		return False

	def isSetValid(self):
		for attribute in self.attributes:
			if not self.isAttributeValid(attribute):
				return False
		return True

class Table(object):
	def __init__(self, _cards):
		self.cards = _cards

	def getCards(self):
		return self.cards

	def removeCards(self, slots):
		for slot in sorted(slots, reverse=True): del self.cards[slot]

	def fillTable(self, deck):
		num_of_cards = 12-len(self.cards)
		if num_of_cards: self.cards.extend(deck.drawCards(num_of_cards))
		while not self.hasSet() and not deck.isEmpty():
			self.cards.extend(deck.drawCards(3))

	def hasSet(self):
		for i in range(len(self.cards)):
			for j in range(i+1, len(self.cards)):
				for k in range(j+1, len(self.cards)):
					s = Set(self.cards[i],self.cards[j],self.cards[k])
					if s.isSetValid():
						return True
		return False

class SetGame(object):
	def __init__(self, _deck):
		self.deck = _deck
		self.table = Table(self.deck.drawCards(12))

		self.winner = None

	def getTable(self):
		return self.table

	def getDeck(self):
		return self.deck

	def isActive(self):
		if self.deck.isEmpty() and not self.table.hasSet(): return False
		return True


if __name__ == '__main__':
	print("Start set_game.py to play the game")

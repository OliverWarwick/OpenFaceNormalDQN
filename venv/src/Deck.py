# Deck class which contains an array of Card objects.
import random


class Card:

    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def get_numeric_value(self):

        valueLookUpDict = {"Ace": 14, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "Jack": 11, "Queen": 12, "King": 13}

        if valueLookUpDict.get(self.value) is not None:
            return valueLookUpDict.get(self.value)
        else:
            raise NumericValueNotFoundException()


class Deck:

    def __init__(self):
        self.numberOfCards = 0
        self.cards = []

    def create_new_full_deck(self):
        Suits = ["Diamonds", "Spades", "Hearts", "Clubs"]
        Values = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]

        for s in Suits:
            for v in Values:
                self.cards.append(Card(s, v))
        self.numberOfCards = 52
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self):
        if self.numberOfCards != 0:
            self.numberOfCards -= 1
            return self.cards[0]
        else:
            raise EmptyDeckException()

    def print_deck(self):
        print("Start of deck")
        for card in self.cards:
            print(card.value)
        print("End of deck")


# Exception classes.
class EmptyDeckException(Exception):
    pass


class NumericValueNotFoundException(Exception):
    pass


if __name__ == '__main__':

    # Create new deck

    c = Deck()
    c.create_new_full_deck()
    c.deal_card()
    c.deal_card()
    c.print_deck()

    print(c.numberOfCards)







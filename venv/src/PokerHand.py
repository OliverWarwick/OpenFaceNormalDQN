# 5 card hand for the back and middle rows
# Take from three card hand and increase the functionality.

from Deck import Card, Deck


class ThreeCardHand:

    def __init__(self):

        self.currentHand = []
        self.numberOfCards = 0
        self.totalCardsPossible = 3

        self.high = 1
        self.low = 1
        self.importantCards = []

        self.freq = dict()
        self.finalStyle = None

    def add_card(self, card):

        if self.numberOfCards < self.totalCardsPossible:
            self.currentHand.append(card)
            self.numberOfCards += 1
        else:
            raise ThreeCardHandFullException()


    def remove_card(self, card):

        if self.numberOfCards > 0:
            self.currentHand.remove(card)
            self.numberOfCards -= 1
        else:
            raise EmptyHandException()

    def reset(self):                        # Figure out while we need this.
        self.high = 1
        self.low = 1
        self.freq = dict()
        self.importantCards = []


    def has_high_card(self):

        self.reset()
        self.line_up()

        # If the hand just has a high card then just record all the cards which are present, order then and these
        # are the important cards.

        for key in self.freq:
            for i in range(0, self.freq[key]): # Add the number of times this occurs.
                self.importantCards.append(key)

        self.importantCards.sort(reverse=True)

        return PokerHand("High Card", self.importantCards)


    def hasOnePair(self):

        hasPair = False
        self.reset()
        self.line_up()

        # First check if there is a card which appears twice.

        for val in self.freq:
            if self.freq[val] == 2:
                hasPair = True
                self.importantCards.append(val)
        self.importantCards.sort(reverse=True)

        if hasPair:                                # Then loop through again to find the remaining card.
            extraCards = []
            for val in self.freq:
                if val not in self.importantCards: # So check its not the card we are considering, and then add in.
                    for i in range(0, self.freq[val]):
                        extraCards.append(val) # No need to sort the list now, as pair is given prescidence.
            extraCards.sort(reverse=True)

            return PokerHand("One Pair", self.importantCards + extraCards)
        else:
            return None


    def hasThreeOfKind(self):

        # If just 3 cards then check they are all the same.
        hasThreeOfKind = False
        self.reset()
        self.line_up()

        for val in self.freq: # Can't have two triples.
            if self.freq[val] == 3:
                hasThreeOfKind = True
                self.importantCards.append(val)

        if hasThreeOfKind:  # Then loop through again to find the remaining card.
            extraCards = []
            for val in self.freq:
                if val not in self.importantCards:
                    for i in range(0, self.freq[val]):
                        extraCards.append(val)  # No need to sort the list now, as pair is given prescidence.
            extraCards.sort(reverse = True)
            return PokerHand("Three of a Kind", self.importantCards + extraCards)
        else:
            return None

    def line_up(self):

        for val in list(range(2, 14)):

            occurrences = 0

            for cards in self.currentHand:
                if cards.getNumericValue() == val:
                    occurrences += 1

            self.freq[val] = occurrences


    def findHandType(self):

        best = None

        if self.hasHighCard() is not None:
            best = self.hasHighCard()

        if self.hasOnePair() is not None:
            best = self.hasOnePair()

        if self.hasThreeOfKind() is not None:
            best = self.hasThreeOfKind()

        return best


    def evaluateHand(self, handID = "Front"):

        # First get the details of the hand.
        # Royalities as on the wiki page.

        handType = self.findHandType()
        print(handID + ":  " + handType.style)

        if handType.style == "High Card":
            return 0
        elif handType.style == "One Pair":
            points = handType.importantCards[0] - 5
            if points > 0:
                return points
            else:
                return 0
        elif handType.style == "Three of a Kind":
            points = handType.importantCards[0] + 8
            return points
        else:
            return 0

    def compareRow(self, secondHand):

        # Return 1 is Hand 1 is better, 0 if equal and -1 if hand 2 is better.
        # Possible to uniquely identify every hand just using style / high / low.

        ###
        # However this might not be possible for the 5 card, think about a way to encode card hands.
        # 100000 * style rating  + 1000 * high rating + 10 * low rating. + 0.5 * remaining value. ???
        ###


        handOneType = self.findHandType()
        handTwoType = secondHand.findHandType()

        # Also included the other card types for the 5 card checks.
        handDictionary = {"High Card": 1, "One Pair": 2, "Two Pair": 3, "Three of a Kind": 4, "Straight": 5, "Flush": 6,
                          "Full House": 7, "Four of a Kind": 8, "Straight Flush": 9, "Royal Flush": 10}

        try:
            # First check if there is a clear winner, if not then we have to break it down to the cards themselves.
            if handDictionary[handOneType.style] > handDictionary[handTwoType.style]:
                return 1
            elif handDictionary[handOneType.style] < handDictionary[handTwoType.style]:
                return -1
            else:
                # Now they have the same style, so we can cycle through the cards checking at each stage.
                for i in range(0, min(len(handOneType.importantCards), len(handTwoType.importantCards))):
                    if handOneType.importantCards[i] > handTwoType.importantCards[i]:
                        return 1
                    if handOneType.importantCards[i] < handTwoType.importantCards[i]:
                        return -1

                # Having reached the end of this the hands must be exactly equal, hence return 0
                return 0

        except Exception:
            # To catch some weird error happening with the type of card not being recorded correctly.
            print("Dunno - error with recording of hand.")




if  __name__ == "__main__":

    print("Starting\n")
    c = Deck()
    c.createNewFullDeck()

    # deal = c.dealFiveCards()
    # t = ThreeCardHand()
    # t.currentHand = deal
    # print(t.line_up())
    # #print(t.hasHighCard().high)
    # re = t.hasOnePair()
    # if re is not None:
    #     print(re.high)
    #     print(re.low)

    #print(isinstance(c, Deck))
    t = ThreeCardHand()
    s = ThreeCardHand()

    t.currentHand = [Card("Spade", "8"), Card("Diamond", "7"), Card("Spade", "7")]
    s.currentHand = [Card("Spade", "9"), Card("Diamond", "9"), Card("Diamond", "2")]

    print(t.evaluateHand("Front"))
    print(s.evaluateHand("Front"))
    print(t.compareRow(s))























class FiveCardHand(ThreeCardHand):

    def __init__(self):
        super(FiveCardHand, self).__init__()
        self.totalCardsPossible = 5

    def hasTwoPair(self):

        hasTwoPair = False
        self.reset()
        self.line_up()

        # Find a list of all pairs, and from there easy to do high and low.

        pairsList = []

        for val in self.freq:
            if self.freq[val] == 2:
                pairsList.append(val)

        pairsList.sort(reverse=True) # Rank the pairs high to low.

        if len(pairsList) == 2:
            hasTwoPair = True

        # High represents the high pairs and low the lower of the two.

        if hasTwoPair == True:
            for val in self.freq:
                if self.freq[val] == 1:
                    pairsList.append(val)
            return PokerHand("Two Pair", pairsList) # Should containing the three number, for the 2 pairs and then extra card.
        else:
            return None


    def hasFullHouse(self):

        # First check if it has a triple, and then check if it has a pair.
        # High for the triple and low for the pair.

        self.reset()
        self.line_up()

        threes = self.hasThreeOfKind()
        twos = self.hasOnePair()

        if (threes is not None) and (twos is not None):
            # If both are true, then need the important card from each of them, in the order of the triple first.
            return PokerHand("Full House", [threes.importantCards[0], twos.importantCards[0]])
        else:
            return None

    def hasFourOfKind(self):

        self.reset()
        self.line_up()
        hasFourOfKind = False

        for val in self.freq:
            if self.freq[val] == 4:
                hasFourOfKind = True
                self.importantCards.append(val) #Can't have more than one four of kind.

        if hasFourOfKind:
            # Find the remaining card
            for val in self.freq:
                if self.freq[val] == 1:
                    self.importantCards.append(val)
            return PokerHand("Four of a Kind", self.importantCards)
        else:
            return None

    def checkSuitsSame(self):

        try:
            suitInQuestion = self.currentHand[0].suit
            for card in self.currentHand:
                if suitInQuestion is not card.suit:
                    return False
            return True

        except Exception:
            return False

    def checkValuesInOrder(self):

        # Set up an array to store the numbers of the cards
        values = []

        # Get the numeric values of the cards.
        for card in self.currentHand:
            values.append(card.getNumericValue())

        if len(values) == 0 or len(values) == 1:
            return True
        else:
            values.sort()
            for i in range(0,len(values)-1):
                if values[i+1] - values[i] != 1:
                    return False
            return True


    def hasFlush(self):

        self.reset()
        self.line_up()

        if self.checkSuitsSame() and self.numberOfCards == 5:
            # Then need to find the highest, and then the second highest.

            for val in self.freq:
                if self.freq[val] == 1:
                    self.importantCards.append(val)
            self.importantCards.sort(reverse=True)

            #Once finished, remove then call the remaining routine.

            return PokerHand("Flush", self.importantCards)
        else:
            return None


    def hasStraight(self):

        self.reset()
        self.line_up()

        valuesOfCards = set()

        for card in self.currentHand:
            valuesOfCards.add(card.getNumericValue())

        if len(valuesOfCards) == 5:

            valuesOfCards = list(valuesOfCards)

            #Auto orders these so can just check each diff by one.
            for i in range(0,4):
                if valuesOfCards[i] + 1 != valuesOfCards[i+1]:
                    return None

            # If not then this is true, and can return the highest card.
            return PokerHand("Straight", [valuesOfCards[4]])

        return None



    def hasStraightFlush(self):

        self.reset()
        self.line_up()

        st = self.hasStraight()
        fl = self.hasFlush()

        if st is not None and fl is not None:
            # Find high value
            return PokerHand("Straight Flush", [st.importantCards[0]])
        else:
            return None

    def hasRoyalFlush(self):

        self.reset()
        self.line_up()

        stfl = self.hasStraightFlush()

        if (stfl is not None) and (stfl.importantCards[0] == 14):
            return PokerHand("Royal Flush", [14])
        else:
            return None


    def findHandType(self):

        # Find the best poker hand which is contained in this hand.

        best = None

        if self.hasHighCard() is not None:
            best = self.hasHighCard()
        if self.hasOnePair() is not None:
            best = self.hasOnePair()
        if self.hasTwoPair() is not None:
            best = self.hasTwoPair()
        if self.hasThreeOfKind() is not None:
            best = self.hasThreeOfKind()
        if self.hasStraight() is not None:
            best = self.hasStraight()
        if self.hasFlush() is not None:
            best = self.hasFlush()
        if self.hasFullHouse() is not None:
            best = self.hasFullHouse()
        if self.hasFourOfKind() is not None:
            best = self.hasFourOfKind()
        if self.hasStraightFlush() is not None:
            best = self.hasStraightFlush()
        if self.hasRoyalFlush() is not None:
            best = self.hasRoyalFlush()

        return best


    def evaluateHand(self, handID):

        # Find the hand style, and recover the details.
        backDictOfPoints = {("Straight", 2), ("Flush", 4), ("Full House", 6), ("Four of a Kind", 10), ("Straight Flush", 15), ("Royal Flush", 25)}
        middleDictOfPoints = {("Three of a Kind", 2), ("Straight", 4), ("Flush", 8), ("Full House", 12), ("Four of a Kind", 20), ("Straight Flush", 30), ("Royal Flush", 50)}

        handType = self.findHandType()
        print(handID + ":  " + handType.style)

        if handID == "Back":
            try:
                return backDictOfPoints[handType.style]
            except Exception:
                return 0
        else:
            try:
                return middleDictOfPoints[handType.style]
            except Exception:
                return 0


class ThreeCardHandFullException(Exception):
    pass

class EmptyHandException(Exception):
    pass









if  __name__ == "__main__":

    print("He;;p")
    f = FiveCardHand()
    f.currentHand = [Card("Spade", "10"), Card("Spade", "Jack"), Card("Spade", "Queen"), Card("Spade", "King"),
                         Card("Spade", "Ace")]



    # r = f.hasFourOfKind()
    # print(r.high)
    # print(r.low)
    # print(f.hasFlush())
    r = f.hasTwoPair()
    #print(r)
    print(f.scoreRoyalitiesPoints("back"))
    # print(r.low)






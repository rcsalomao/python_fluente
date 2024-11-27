from __future__ import annotations

import collections
import math
from pprint import pp
from random import choice

Card = collections.namedtuple("Card", ["rank", "suit"])


class FrenchDeck:
    ranks = [str(n) for n in range(2, 11)] + list("JQKA")
    suits = "spades diamonds clubs hearts".split()

    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self.suits for rank in self.ranks]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]


suit_values = dict(spades=3, hearts=2, diamonds=1, clubs=0)


def spades_high(card):
    rank_value = FrenchDeck.ranks.index(card.rank)
    return rank_value * len(suit_values) + suit_values[card.suit]


class Vector:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Vector({self.x!r}, {self.y!r})"

    def __abs__(self):
        return math.hypot(self.x, self.y)

    def __bool__(self):
        return bool(abs(self))

    def __add__(self, other: Vector):
        return Vector(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar: float):
        return Vector(self.x * scalar, self.y * scalar)


def exemplo_1():
    deck = FrenchDeck()
    pp(len(deck))
    pp(deck[0])
    pp(deck[-1])
    pp(deck[0:10])
    pp(deck[0:10:2])
    pp((choice(deck), choice(deck), choice(deck)))
    for card in deck:
        pp(card)
    pp(Card("Q", "hearts") in deck)
    pp(Card("Q", "beasts") in deck)
    for card in sorted(deck, key=spades_high):
        pp(card)


def exemplo_2():
    v1 = Vector(2, 4)
    v2 = Vector(2, 1)
    v3 = Vector()
    pp(v1)
    pp(v1 + v2)
    pp(abs(v1))
    pp(bool(v1))
    pp(bool(v3))
    pp(v2 * 8)


if __name__ == "__main__":
    # exemplo_1()
    exemplo_2()

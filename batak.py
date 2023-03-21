import random


class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __repr__(self):
        return f"{self.rank}{self.suit}"


class Deck:
    ranks = "23456789TJQKA"
    suits = "♠♡♢♣"

    def __init__(self):
        self.cards = [Card(rank, suit) for rank in self.ranks for suit in self.suits]
        random.shuffle(self.cards)

    def deal(self, n):
        return [self.cards[i::n] for i in range(n)]


def play_trick(leader, hands, trump_suit, trump_played):
    played_cards = []
    led_suit = None
    for i, hand in enumerate(hands):
        player = (leader + i) % len(hands)
        if led_suit is None:
            led_card = next(
                (card for card in hand if (card.suit != trump_suit) or trump_played),
                hand[0],
            )
            hand.remove(led_card)
            played_cards.append((player, led_card))
            print(f"Player {player + 1} leads {led_card}")
            led_suit = led_card.suit
            if led_card.suit == trump_suit:
                trump_played = True
        else:
            follow_card = next((card for card in hand if card.suit == led_suit), None)
            if follow_card:
                higher_cards = [
                    card
                    for card in hand
                    if card.suit == led_suit
                    and Deck.ranks.index(card.rank) > Deck.ranks.index(follow_card.rank)
                ]
                if higher_cards:
                    follow_card = max(
                        higher_cards, key=lambda c: Deck.ranks.index(c.rank)
                    )
                hand.remove(follow_card)
                played_cards.append((player, follow_card))
                print(f"Player {player + 1} plays {follow_card}")
            else:
                trump_card = next(
                    (card for card in hand if card.suit == trump_suit), None
                )
                if trump_card and trump_played:
                    hand.remove(trump_card)
                    played_cards.append((player, trump_card))
                    print(f"Player {player + 1} plays {trump_card}")
                else:
                    non_trump_card = hand.pop()
                    played_cards.append((player, non_trump_card))
                    print(f"Player {player + 1} plays {non_trump_card}")

    return played_cards


def find_trick_winner(played_cards, trump_suit):
    winning_card = played_cards[0][1]
    winner = played_cards[0][0]
    for player, card in played_cards[1:]:
        if card.suit == trump_suit and winning_card.suit != trump_suit:
            winning_card = card
            winner = player
        elif card.suit == winning_card.suit and Deck.ranks.index(
            card.rank
        ) > Deck.ranks.index(winning_card.rank):
            winning_card = card
            winner = player

    return winner


def play_game(num_players=4):
    deck = Deck()
    hands = deck.deal(num_players)
    tricks_won = [0] * num_players
    leader = 0
    trump_suit = random.choice(Deck.suits)
    trump_played = False
    print(f"Trump suit is {trump_suit}\n")

    for i in range(len(deck.cards) // num_players):
        print(f"Trick {i + 1}:")
        played_cards = play_trick(leader, hands, trump_suit, trump_played)
        winner = find_trick_winner(played_cards, trump_suit)
        tricks_won[winner] += 1
        leader = winner
        if not trump_played:
            trump_played = any(card.suit == trump_suit for _, card in played_cards)
        print(f"Player {winner + 1} wins trick {i + 1}\n")

    for i, tricks in enumerate(tricks_won):
        print(f"Player {i + 1} won {tricks} tricks")


if __name__ == "__main__":
    play_game()

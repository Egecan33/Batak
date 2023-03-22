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


class AIPersonality:
    def lead_card(self, hand, trump_suit, trump_played):
        raise NotImplementedError()

    def follow_card(self, hand, led_suit, trump_suit, trump_played):
        raise NotImplementedError()


class ConservativePlayer(AIPersonality):
    def lead_card(self, hand, trump_suit, trump_played):
        sorted_hand = sorted(
            hand,
            key=lambda c: (Deck.suits.index(c.suit), Deck.ranks.index(c.rank)),
        )
        return sorted_hand[0]

    def follow_card(self, hand, led_suit, trump_suit, trump_played):
        follow_card = next((card for card in hand if card.suit == led_suit), None)
        if follow_card:
            return follow_card
        return next((card for card in hand if card.suit != trump_suit), hand[0])


class AggressivePlayer(AIPersonality):
    def lead_card(self, hand, trump_suit, trump_played):
        sorted_hand = sorted(
            hand,
            key=lambda c: (Deck.suits.index(c.suit), Deck.ranks.index(c.rank)),
            reverse=True,
        )
        return sorted_hand[0]

    def follow_card(self, hand, led_suit, trump_suit, trump_played):
        follow_card = next((card for card in hand if card.suit == led_suit), None)
        if follow_card:
            higher_cards = [
                card
                for card in hand
                if card.suit == led_suit
                and Deck.ranks.index(card.rank) > Deck.ranks.index(follow_card.rank)
            ]
            if higher_cards:
                follow_card = max(higher_cards, key=lambda c: Deck.ranks.index(c.rank))
            return follow_card
        return hand[0]


class BalancedPlayer(AIPersonality):
    def lead_card(self, hand, trump_suit, trump_played):
        non_trump_cards = [card for card in hand if card.suit != trump_suit]
        if non_trump_cards:
            sorted_hand = sorted(
                non_trump_cards,
                key=lambda c: (Deck.suits.index(c.suit), Deck.ranks.index(c.rank)),
            )
            return sorted_hand[0]
        return hand[0]

    def follow_card(self, hand, led_suit, trump_suit, trump_played):
        follow_card = next((card for card in hand if card.suit == led_suit), None)
        if follow_card:
            return follow_card
        return next((card for card in hand if card.suit == trump_suit), hand[0])


class OpportunisticPlayer(AIPersonality):
    def lead_card(self, hand, trump_suit, trump_played):
        if not trump_played:
            non_trump_cards = [card for card in hand if card.suit != trump_suit]
            if non_trump_cards:
                sorted_hand = sorted(
                    non_trump_cards,
                    key=lambda c: (Deck.suits.index(c.suit), Deck.ranks.index(c.rank)),
                    reverse=True,
                )
                return sorted_hand[0]
        return hand[0]

    def follow_card(self, hand, led_suit, trump_suit, trump_played):
        follow_card = next((card for card in hand if card.suit == led_suit), None)
        if follow_card:
            return follow_card
        return next((card for card in hand if card.suit != trump_suit), hand[0])


def create_personalities(num_players):
    personalities = [
        ConservativePlayer(),
        AggressivePlayer(),
        BalancedPlayer(),
        OpportunisticPlayer(),
    ]
    return personalities[:num_players]


def play_trick(leader, hands, trump_suit, trump_played, personalities):
    played_cards = []
    led_suit = None
    for i, hand in enumerate(hands):
        player = (leader + i) % len(hands)
        personality = personalities[player]

        if led_suit is None:
            led_card = personality.lead_card(hand, trump_suit, trump_played)
            hand.remove(led_card)
            played_cards.append((player, led_card))
            print(f"Player {player + 1} leads {led_card}")
            led_suit = led_card.suit
            if led_card.suit == trump_suit:
                trump_played = True
        else:
            follow_card = personality.follow_card(
                hand, led_suit, trump_suit, trump_played
            )
            hand.remove(follow_card)
            played_cards.append((player, follow_card))
            print(f"Player {player + 1} plays {follow_card}")

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


def save_results_to_file(results):
    with open("results.txt", "a") as f:
        f.write(", ".join(str(points) for points in results) + "\n")


def bidding_phase(hands):
    bids = [0] * len(hands)
    tied_players = list(range(len(hands)))

    while len(tied_players) > 1:
        new_bids = []
        for i in tied_players:
            print(
                f"Player {i + 1}, your hand: {sorted(hands[i], key=lambda c: (Deck.suits.index(c.suit), Deck.ranks.index(c.rank)))}"
            )
            bid = int(input(f"Enter your bid (must be at least {bids[i]}): "))
            while bid < bids[i]:
                bid = int(
                    input(f"Invalid bid. Enter your bid (must be at least {bids[i]}): ")
                )
            new_bids.append((i, bid))

        highest_bid = max(new_bids, key=lambda x: x[1])
        tied_players = [i for i, bid in new_bids if bid == highest_bid[1]]
        for i, bid in new_bids:
            bids[i] = bid

    highest_bidder = tied_players[0]

    print(
        f"Player {highest_bidder + 1}, you have the highest bid. Choose the trump suit:"
    )
    for i, suit in enumerate(Deck.suits):
        print(f"{i + 1}: {suit}")
    trump_suit = Deck.suits[
        int(input("Enter the number corresponding to your chosen trump suit: ")) - 1
    ]

    return highest_bidder, bids[highest_bidder], trump_suit


def play_game(num_players=4):
    deck = Deck()
    hands = deck.deal(num_players)
    tricks_won = [0] * num_players
    scores = [0] * num_players
    trump_played = False
    personalities = create_personalities(num_players)

    highest_bidder, highest_bid, trump_suit = bidding_phase(hands)
    print(
        f"\nPlayer {highest_bidder + 1} has the highest bid of {highest_bid} and leads the first trick"
    )
    print(f"Trump suit is {trump_suit}\n")

    leader = highest_bidder
    for i in range(len(deck.cards) // num_players):
        print(f"Trick {i + 1}:")
        played_cards = play_trick(
            leader, hands, trump_suit, trump_played, personalities
        )
        winner = find_trick_winner(played_cards, trump_suit)
        tricks_won[winner] += 1
        if winner != leader:
            leader = winner
        if not trump_played:
            trump_played = any(card.suit == trump_suit for _, card in played_cards)
        print(f"Player {winner + 1} wins trick {i + 1}\n")

    scores = tricks_won.copy()
    if tricks_won[highest_bidder] < highest_bid:
        scores[highest_bidder] = -highest_bid
        print(
            f"Player {highest_bidder + 1} did not win {highest_bid} tricks, their score is set to {-highest_bid}"
        )

    # Update scores for players who didn't win any tricks
    for i, tricks in enumerate(tricks_won):
        if tricks == 0:
            scores[i] = -10
            print(f"Player {i + 1} did not win any tricks, their score is set to -10")

    print("Results:")
    print("--------")
    total_tricks_won = 0
    for i, (score, tricks) in enumerate(zip(scores, tricks_won)):
        print(f"Player {i + 1}:")
        print(f"  Score: {score}")
        print(f"  Tricks won: {tricks}")
        total_tricks_won += tricks

    print(f"\nTotal tricks won: {total_tricks_won}")

    save_results_to_file(scores)


if __name__ == "__main__":
    play_game()

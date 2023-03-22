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

    def bid(self, hand, current_bids):
        raise NotImplementedError()

    def choose_trump_suit(self, hand):
        raise NotImplementedError()


class ConservativePlayer(AIPersonality):
    def lead_card(self, hand, trump_suit, trump_played):
        sorted_hand = sorted(
            hand,
            key=lambda c: (Deck.suits.index(c.suit), Deck.ranks.index(c.rank)),
        )
        if not trump_played:
            sorted_hand = [card for card in sorted_hand if card.suit != trump_suit]
        return sorted_hand[0]

    def follow_card(self, hand, led_suit, trump_suit, trump_played):
        valid_cards = [card for card in hand if card.suit == led_suit]
        if not valid_cards:
            valid_cards = [card for card in hand if card.suit == trump_suit]

        if not valid_cards:
            valid_cards = hand

        return min(valid_cards, key=lambda c: Deck.ranks.index(c.rank))

    def bid(self, hand, current_bids):
        num_high_cards = sum(1 for card in hand if card.rank in "JQKA")
        bid_value = max(1, num_high_cards // 2)
        return max(current_bids + [0]) + bid_value

    def choose_trump_suit(self, hand):
        suit_counts = {suit: 0 for suit in Deck.suits}
        for card in hand:
            suit_counts[card.suit] += 1
        return max(suit_counts, key=suit_counts.get)


class AggressivePlayer(AIPersonality):
    def lead_card(self, hand, trump_suit, trump_played):
        if not trump_played:
            non_trump_cards = [card for card in hand if card.suit != trump_suit]
            if non_trump_cards:
                return max(non_trump_cards, key=lambda c: Deck.ranks.index(c.rank))
        return max(hand, key=lambda c: Deck.ranks.index(c.rank))

    def follow_card(self, hand, led_suit, trump_suit, trump_played):
        valid_cards = [card for card in hand if card.suit == led_suit]
        if not valid_cards:
            valid_cards = [card for card in hand if card.suit == trump_suit]

        if not valid_cards:
            valid_cards = hand

        high_cards = [card for card in valid_cards if card.rank in "JQKA"]
        if high_cards:
            if trump_played:
                return min(high_cards, key=lambda c: Deck.ranks.index(c.rank))
            else:
                return max(high_cards, key=lambda c: Deck.ranks.index(c.rank))
        else:
            if trump_played:
                return min(valid_cards, key=lambda c: Deck.ranks.index(c.rank))
            else:
                return max(valid_cards, key=lambda c: Deck.ranks.index(c.rank))

    def bid(self, hand, current_bids):
        num_high_cards = sum(1 for card in hand if card.rank in "JQKA")
        bid_value = num_high_cards
        return max(current_bids + [0]) + bid_value

    def choose_trump_suit(self, hand):
        suit_counts = {suit: 0 for suit in Deck.suits}
        for card in hand:
            suit_counts[card.suit] += 1
        return max(suit_counts, key=suit_counts.get)


class BalancedPlayer(AIPersonality):
    def lead_card(self, hand, trump_suit, trump_played):
        if not trump_played:
            non_trump_cards = [card for card in hand if card.suit != trump_suit]
            if non_trump_cards:
                return random.choice(non_trump_cards)
        return random.choice(hand)

    def follow_card(self, hand, led_suit, trump_suit, trump_played):
        valid_cards = [card for card in hand if card.suit == led_suit]
        if not valid_cards:
            valid_cards = [card for card in hand if card.suit == trump_suit]

        if not valid_cards:
            valid_cards = hand

        if trump_played:
            return min(valid_cards, key=lambda c: Deck.ranks.index(c.rank))
        else:
            return max(valid_cards, key=lambda c: Deck.ranks.index(c.rank))

    def bid(self, hand, current_bids):
        num_high_cards = sum(1 for card in hand if card.rank in "JQKA")
        bid_value = max(1, num_high_cards // 3)
        return max(current_bids + [0]) + bid_value

    def choose_trump_suit(self, hand):
        suit_counts = {suit: 0 for suit in Deck.suits}
        for card in hand:
            suit_counts[card.suit] += 1
        return max(suit_counts, key=suit_counts.get)


class OpportunisticPlayer(AIPersonality):
    def lead_card(self, hand, trump_suit, trump_played):
        high_cards = [card for card in hand if card.rank in "JQKA"]
        if not trump_played:
            high_cards = [card for card in high_cards if card.suit != trump_suit]
        if high_cards:
            return min(high_cards, key=lambda c: Deck.ranks.index(c.rank))
        return min(hand, key=lambda c: Deck.ranks.index(c.rank))

    def follow_card(self, hand, led_suit, trump_suit, trump_played):
        valid_cards = [card for card in hand if card.suit == led_suit]
        if not valid_cards:
            valid_cards = [card for card in hand if card.suit == trump_suit]

        if not valid_cards:
            valid_cards = hand

        if trump_played:
            return min(valid_cards, key=lambda c: Deck.ranks.index(c.rank))
        else:
            high_cards = [card for card in valid_cards if card.rank in "JQKA"]
            if high_cards:
                return max(high_cards, key=lambda c: Deck.ranks.index(c.rank))
            else:
                return min(valid_cards, key=lambda c: Deck.ranks.index(c.rank))

    def bid(self, hand, current_bids):
        num_high_cards = sum(1 for card in hand if card.rank in "JQKA")
        bid_value = max(1, num_high_cards // 4)
        return max(current_bids + [0]) + bid_value

    def choose_trump_suit(self, hand):
        suit_counts = {suit: 0 for suit in Deck.suits}
        for card in hand:
            suit_counts[card.suit] += 1
        return max(suit_counts, key=suit_counts.get)


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


def bidding_phase(hands, personalities):
    bids = [0] * len(hands)
    tied_players = list(range(len(hands)))
    tie_counter = 0

    while len(tied_players) > 1:
        new_bids = []

        for i in tied_players:
            print(
                f"Player {i + 1}, your hand: {sorted(hands[i], key=lambda c: (Deck.suits.index(c.suit), Deck.ranks.index(c.rank)))}"
            )
            bid = personalities[i].bid(
                hands[i], [bids[j] for j in tied_players if j != i]
            )
            new_bids.append((i, bid))
            print(f"Player {i + 1} bids {bid}")

        highest_bid = max(new_bids, key=lambda x: x[1])
        new_tied_players = [i for i, bid in new_bids if bid == highest_bid[1]]

        if len(new_tied_players) > 1:
            tie_counter += 1
        else:
            tie_counter = 0

        if tie_counter >= 3:
            forced_bidder = random.choice(new_tied_players)
            bids[forced_bidder] += 1
            tied_players = [forced_bidder]
            break
        else:
            tied_players = new_tied_players

        for i, bid in new_bids:
            bids[i] = bid

    highest_bidder = tied_players[0]
    trump_suit = personalities[highest_bidder].choose_trump_suit(hands[highest_bidder])

    return highest_bidder, bids[highest_bidder], trump_suit


def play_game(num_players=4):
    deck = Deck()
    hands = deck.deal(num_players)
    tricks_won = [0] * num_players
    scores = [0] * num_players
    trump_played = False
    personalities = create_personalities(num_players)

    highest_bidder, highest_bid, trump_suit = bidding_phase(hands, personalities)
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

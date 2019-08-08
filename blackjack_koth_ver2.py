# * Menší pozitivní rozdíl do 21 vyhrává (negativní rozdíl má nejvyšší možnou penalizaci)
# Při stejném rozdílu vyhrává dealer
# Dealer - nemůže hrát přes 17
# Bettor - nemůže hrát přes 21
# První hraje Bettor

import random


class Player():

    def __init__(self, log, name,
                 bettor_strategy_handler,
                 dealer_strategy_handler,
                 bet_size_handler,
                 call_strategy_handler,
                 ):
        self.log = log
        self.name = name
        self.wallet = 1000
        self.total_value = 0
        self.bettor_strategy_handler = bettor_strategy_handler
        self.dealer_strategy_handler = dealer_strategy_handler
        self.bet_size_handler = bet_size_handler
        self.call_strategy_handler = call_strategy_handler

    def roll_dice(self):
        return random.randint(1, 6)

    def get_penalty(self):
        penalty = 21 - self.total_value
        return 100 if penalty < 0 else penalty

    def new_round(self):
        self.total_value = 0

    def bettor_play(self):
        still_playing = True
        while still_playing:
            self.total_value += self.roll_dice()
            still_playing = self.bettor_strategy_handler(self.total_value, self.log)
            if self.total_value >= 21:
                still_playing = False

    def dealer_play(self):
        still_playing = True
        while still_playing:
            self.total_value += self.roll_dice()
            still_playing = self.dealer_strategy_handler(self.total_value, self.log)
            if self.total_value >= 17:
                still_playing = False

    def bet(self):
        return self.bet_size_handler(self.total_value, self.log)

    def call(self, bet):
        return self.call_strategy_handler(self.total_value, self.log, bet)


def dummy_bettor_handler(value, log):
    return True


def dummy_dealer_handler(value, log):
    return True


def dummy_bet_handler(value, log):
    return 5


def dummy_check_handler(value, log, bet):
    return True




def better_bettor_handler(value, log):
    if value <= 18:
        return True
    else:
        return False


def better_dealer_handler(value, log):
    return True


def better_bet_handler(value, log):
    bet_size = 0
    if value <= 21:
        bet_size = value - 21 + 5
    else:
        bet_size = 0
    return bet_size


def better_check_handler(value, log, bet):
    if value <= 21:
        return True






def explo1_bettor_handler(value, log):
    if value <= 18:
        return True
    else:
        return False


def explo1_dealer_handler(value, log):
    return True


def explo1_bet_handler(value, log):
    bet_size = 0
    if value <= 21:
        bet_size = value - 21 + 5
    else:
        if random.randint(1, 100) <= 0:
            bet_size = 1
    return bet_size


def explo1_check_handler(value, log, bet):
    if value <= 21:
        return True



def explo2_bettor_handler(value, log):
    if value <= 18:
        return True
    else:
        return False


def explo2_dealer_handler(value, log):
    return True


def explo2_bet_handler(value, log):
    bet_size = 0
    if value <= 21:
        bet_size = value - 21 + 5
    else:
        if random.randint(1, 100) <= 0:
            bet_size = 1
    return bet_size


def explo2_check_handler(value, log, bet):
    if value <= 21:
        if bet <= value - 21 + 5:
            return True






def game_round(dealer, bettor, log):
    bettor.new_round()
    dealer.new_round()
    bettor.bettor_play()
    bet_size = bettor.bet()
    dealer.dealer_play()
    if dealer.call(bet_size):
        if bettor.get_penalty() < dealer.get_penalty():
            bettor.wallet += bet_size
            dealer.wallet -= bet_size
            log.append((bettor.name, dealer.name, bettor.name, dealer.name, bet_size, 1, bettor.total_value, dealer.total_value))
        else:
            bettor.wallet -= bet_size
            dealer.wallet += bet_size
            log.append((bettor.name, dealer.name, dealer.name, bettor.name, bet_size, 1, bettor.total_value, dealer.total_value))
    else:
        bettor.wallet += 1
        dealer.wallet -= 1
        log.append((bettor.name, dealer.name, bettor.name, dealer.name, bet_size, 0, bettor.total_value, dealer.total_value))




def simulation(players, n, log):
    for k in range(n):
        game_round(players[0], players[1], log)
        players = players[::-1]
    for p in players:
        print("{}\t{}".format(p.name, p.wallet))
    output = "bettor_name, dealer_name, winner, loser, bet_size, call, bettor_value, dealer_value\n"
    output += "\n".join([",".join(map(str, line)) for line in log])
    with open("data/output.csv", "w") as f:
        f.write(output)

log = []
p1 = Player(log, "Better player", better_bettor_handler, better_dealer_handler,
            better_bet_handler, better_check_handler)
p2 = Player(log, "Explo2 player", explo2_bettor_handler, explo2_dealer_handler,
            explo2_bet_handler, explo2_check_handler)

simulation([p1, p2], 1000, log)
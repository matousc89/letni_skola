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

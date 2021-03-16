from constants import *
import itertools
from functools import reduce

# various functions to generate combinations for each line


def line_combinations(players, line, use_structure=True):
    """returns combinations of players that fit salary constraints for given [line]

    Args:
        players ([dataframe]): [all players in particular line]
        line ([String]): [line on the field, e.g. forward]
    """
    arrangement = get_line_arrangement(line)
    # separate into locked and unlocked
    locked = tuple(players.loc[players[LOCK] == 1].index)
    unlocked = players.drop(list(locked))
    print(locked)
    onfield_locked = tuple(
        players.loc[(players[LOCK] == 1) & (players[BENCH] == 0)].index)
    onfield_unlocked = unlocked[unlocked[BENCH] == 0]

    # separate into price categories for efficiency
    # unlocked
    premium = unlocked[unlocked[PRICE] > PRICE_PREMIUM]
    mid_range = unlocked[(unlocked[PRICE] <= PRICE_PREMIUM)
                         & (unlocked[PRICE] > PRICE_ROOKIE)]
    rookie = unlocked[(unlocked[PRICE] <= PRICE_ROOKIE)
                      & (unlocked[BENCH] == 0)]
    bench = unlocked[(unlocked[PRICE] <= PRICE_ROOKIE)
                     & (unlocked[BENCH] == 1)]

    # locked
    premium_lock = players.loc[(players[LOCK] == 1) & (
        players[PRICE] > PRICE_PREMIUM)]
    mid_range_lock = players.loc[(players[LOCK] == 1) & (
        players[PRICE] <= PRICE_PREMIUM) & (players[PRICE] > PRICE_ROOKIE)]
    rookie_lock = players.loc[(players[LOCK] == 1) & (
        players[PRICE] <= PRICE_ROOKIE) & (players[BENCH] == 0)]
    bench_lock = players.loc[(players[LOCK] == 1) & (players[BENCH] == 1)]

    # testing
    # if not using structure
    onfield = list(itertools.combinations(onfield_unlocked.index,
                                          arrangement[4] - len(onfield_locked) - arrangement[3]))
    onfield = list(map(lambda x: onfield_locked + x, onfield))

    # add combinations of unlocked mids to list of locked mids
    premium_combs = list(itertools.combinations(
        premium.index, arrangement[0] - len(premium_lock)))
    premium_combs = list(
        map(lambda x: tuple(premium_lock.index) + x, premium_combs))

    mid_range_combs = list(itertools.combinations(
        mid_range.index, arrangement[1] - len(mid_range_lock)))
    mid_range_combs = list(
        map(lambda x: tuple(mid_range_lock.index) + x, mid_range_combs))

    rookie_combs = list(itertools.combinations(
        rookie.index, arrangement[2] - len(rookie_lock)))
    rookie_combs = list(
        map(lambda x: tuple(rookie_lock.index) + x, rookie_combs))

    bench_combs = list(itertools.combinations(
        bench.index, arrangement[3] - len(bench_lock)))
    bench_combs = list(map(lambda x: tuple(bench_lock.index) + x, bench_combs))

    # create all combinations for defenders from price categories
    combinations_array = []

    if use_structure:
        combinations_array = [premium_combs,
                              mid_range_combs, rookie_combs, bench_combs]
    else:
        combinations_array = [onfield, bench_combs]

    combinations = list(itertools.product(*combinations_array))

    # convert to single array for each combination
    formatted_combinations = []
    test = ()
    for comb in combinations:
        formatted_combinations.append(reduce(lambda a, b: a + b, comb))

    return formatted_combinations


def get_line_arrangement(line):
    if line == DEFENDER:
        return [
            DEF_PREMIUM,
            DEF_MID_PRICE,
            DEF_ROOKIE,
            DEF_BENCH,
            DEF_TOTAL
        ]
    elif line == MIDFIELDER:
        return [
            MID_PREMIUM,
            MID_MID_PRICE,
            MID_ROOKIE,
            MID_BENCH,
            MID_TOTAL
        ]
    elif line == RUCK:
        return [
            RUCK_PREMIUM,
            RUCK_MID_PRICE,
            RUCK_ROOKIE,
            RUCK_BENCH,
            RUCK_TOTAL
        ]
    else:
        return [
            FWD_PREMIUM,
            FWD_MID_PRICE,
            FWD_ROOKIE,
            FWD_BENCH,
            FWD_TOTAL
        ]

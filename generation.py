from constants import *
import itertools
from functools import reduce
from helpers import *

# various functions to generate combinations for each line


def line_combinations(players, line, min_salary, max_salary, use_structure=True,):
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

    if use_structure:
        # add combinations of unlocked mids to list of locked mids
        premium_combs = list(itertools.combinations(premium.index, arrangement[0] - len(premium_lock)))
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
    results = []
    
    for comb in combinations:
        formatted_comb = reduce(lambda a, b: a + b, comb)
        salary = get_total_salary(formatted_comb, players)
        if salary >= min_salary and salary <= max_salary:
            results.append((formatted_comb, salary))

    
    return results


def remove_invalid_salary(teams, player_data, min_salary=SALARY_CAP - 30, max_salary=SALARY_CAP):
    """removes all the teams with too low or high salary.

    Args:
        teams (list[tuple]): team combinations list
        min_salary (int, optional): Defaults to SALARY_CAP-200.
        max_salary (int, optional): Defaults to SALARY_CAP.
    """

    filtered_teams = []

    for team in teams:
        salary = team[1]

        if salary >= min_salary and salary <= max_salary:
            # valid salary 29 players
            filtered_teams.append(team)
            # add sum of scores too
            # sums = data.loc[team, ['average', 'projected', 'last3Avg', 'aami']].sum()
            # average.append(sums.average)
            # projected.append(sums.projected)
            # last3Avg.append(sums.last3Avg)
            # aami.append(sums.aami)

    return filtered_teams


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

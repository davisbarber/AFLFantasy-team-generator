import pandas as pd
from constants import *
from formatting import format_player_data
from generation import line_combinations
import time
import itertools

# main execution function to read player list and generate fantasy teams.
def main():
    data = pd.read_csv('data/fav_players.csv')
    print('''--------------------------\n
--------------------------\n
--------------------------\n
          \n\n\n''')
    
    # Format
    data = format_player_data(data)
    # print(data[:5])
    
    # separate into postions
    defenders = pd.concat([data[data[POSITION1] == 'Defender'], data[data[POSITION2] == 'Defender']])

    forwards = pd.concat([data[data[POSITION1] == 'Forward'], data[data[POSITION2] == 'Forward']])

    midfielders = pd.concat([data[data[POSITION1] == 'Midfielder'], data[data[POSITION2] == 'Midfielder']])

    rucks = pd.concat([data[data[POSITION1] == 'Ruck'], data[data[POSITION2] == 'Ruck']])
    # print(rucks)
    
    
    # generate defender combinations
    defs = line_combinations(defenders, DEFENDER, use_structure = False)
    mid = line_combinations(midfielders, MIDFIELDER, use_structure = False)
    ruck = line_combinations(rucks, RUCK, use_structure = False)
    fwd = line_combinations(forwards, FORWARD, use_structure = False)
    print(len(defs))
    print(len(mid))
    print(len(ruck))
    print(len(fwd))

    print(ruck)
    t = time.time()
    
    full_team = list(itertools.product(*[defs, mid, ruck, fwd]))
    print(time.time() - t)
    
    print(len(full_team))
    
    # combine arrays
    full_team_combined = []
    for comb in full_team:
        full_team_combined.append(comb[0] + comb[1] + comb[2] + comb[3])
    
    # teams_df = pd.DataFrame()
    team_salaries = []
    teams = []
    projected = []
    average = []
    last3Avg = []
    aami = []

    print(data.loc[full_team_combined[0], ['average', 'projected', 'last3Avg']].sum().average)
    print(full_team_combined[0])

    # for team in full_team:
    #     salary = data.loc[team, 'price'].sum()

    #     if salary <= 12830 and salary >= 12790:
    #         # valid salary 29 players
    #         teams.append(team)
    #         team_salaries.append(salary)
    #         # add sum of scores too
    #         sums = data.loc[team, ['average', 'projected', 'last3Avg', 'aami']].sum()
    #         average.append(sums.average)
    #         projected.append(sums.projected)
    #         last3Avg.append(sums.last3Avg)
    #         aami.append(sums.aami)

    print(len(teams))

if __name__ == "__main__":
    main()
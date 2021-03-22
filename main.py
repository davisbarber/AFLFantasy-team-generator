import pandas as pd
import generation
from constants import *
from formatting import format_player_data
import time
import itertools
from functools import reduce
from helpers import *

# main execution function to read player list and generate fantasy teams.
def main():
    data = pd.read_csv('data/last_list.csv')
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
    print("Generating combinations...")
    start_time = time.time()
    t = time.time()
    # generate defender combinations
    defs = generation.line_combinations(defenders, DEFENDER, SALARY_DEF_MIN, SALARY_DEF_MAX, use_structure = False)
    mid = generation.line_combinations(midfielders, MIDFIELDER, SALARY_MID_MIN, SALARY_MID_MAX, use_structure = False)
    ruck = generation.line_combinations(rucks, RUCK, SALARY_RUCK_MIN, SALARY_RUCK_MAX, use_structure = False)
    fwd = generation.line_combinations(forwards, FORWARD, SALARY_FWD_MIN, SALARY_FWD_MAX, use_structure = False)
    print(len(defs))
    print(len(mid))
    print(len(ruck))
    print(len(fwd))

    
    full_team = list(itertools.product(*[defs, mid, ruck, fwd]))
    
    print(time.time() - t)
    
    print(len(full_team))
    print('\n')
    # combine arrays
    full_team_combined = []
    
    print("Estimated time is...")
    time_per_comb = 64.84898209571838 / 3144000
    print((time_per_comb * len(full_team)) / 60)
    print('\n')
    print("Combining lines for each team combination...")
    t = time.time()
    
        
    for comb in full_team:
        team = comb[0][0] + comb[1][0] + comb[2][0] + comb[3][0]
        salary = comb[0][1] + comb[1][1] + comb[2][1] + comb[3][1]
        full_team_combined.append((team, salary))
        
    print(time.time() - t)
    print('\n')
    # remove duplicates
    final_teams = []
    print("Removing duplicates...")
    t = time.time()
    for comb in full_team_combined:
        if not contains_duplicates(comb[0]):
            final_teams.append(comb)
    
    print(time.time() - t)
    print(len(final_teams))
    print('\n')
    print("Removing invalid salary...")
    t = time.time()
    results = generation.remove_invalid_salary(final_teams, data)
    
    print(len(results))
    print(time.time() - t)
    
    # get relevant values for teams
    team_salaries = []
    teams = []
    projected = []
    average = []
    last3Avg = []
    aami = []
    combined = []

    for team in results:
        # valid salary 29 players
        teams.append(team[0])
        team_salaries.append(team[1])
        # add sum of scores too
        sums = data.loc[team[0], [AVERAGE, PROJECTED, LAST3AVG, AAMI, COMBINED]].sum()
        average.append(sums.average)
        projected.append(sums.projected)
        last3Avg.append(sums.last3Avg)
        aami.append(sums.aami)
        combined.append(sums.combined)
        
    # data frame with results
    results_data = {
        'salary' : team_salaries,
        'average' : average,
        'projected' : projected,
        'last3Avg' : last3Avg,
        'aami' : aami,
        'combined' : combined,
        'team' : teams
    }

    results_df = pd.DataFrame(results_data, columns=['salary', 'average', 'projected', 'last3Avg', 'aami', 'combined', 'team'])
    
    sort_by_projected = results_df.sort_values('projected', ascending=False)
    sort_by_average = results_df.sort_values('average', ascending=False)
    sort_by_last3Avg = results_df.sort_values('last3Avg', ascending=False)
    sort_by_aami = results_df.sort_values('aami', ascending=False)
    sort_by_combined = results_df.sort_values('combined', ascending=False)
    
    # create an array of dataframes for each team
    best_projected = []
    best_average = []
    best_last3Avg = []
    best_aami = []
    best_combined = []
    
    print(data.loc[list(sort_by_projected.iloc[0].team)])
    # gets top ten for each category
    for i in range(10):
        best_projected.append(data.loc[list(sort_by_projected.iloc[i].team)])
        best_average.append(data.loc[list(sort_by_average.iloc[i].team)])
        best_last3Avg.append(data.loc[list(sort_by_last3Avg.iloc[i].team)])
        best_aami.append(data.loc[list(sort_by_aami.iloc[i].team)])
        best_combined.append(data.loc[list(sort_by_combined.iloc[i].team)])
        
    

    print(sort_by_aami.head())
    
    writer = pd.ExcelWriter('best_teams.xlsx',engine='xlsxwriter')
    # workbook=writer.book
    # worksheet= workbook.add_worksheet('Result')
    # writer.sheets['Result'] = worksheet
    # worksheet.write_string(0, 0, df1.name)

    
    for i in range(10):
        best_aami[i].to_excel(writer, sheet_name = 'aami', startrow = 1 + i*32, startcol = 0)
        best_combined[i].to_excel(writer, sheet_name = 'combined', startrow = 1 + i*32, startcol = 0)
        best_average[i].to_excel(writer, sheet_name = 'average', startrow = 1 + i*32, startcol = 0)
        best_last3Avg[i].to_excel(writer, sheet_name = 'last3Avg', startrow = 1 + i*32, startcol = 0)
        best_projected[i].to_excel(writer, sheet_name = 'projected', startrow = 1 + i*32, startcol = 0)
        
    writer.save()
    
    total_time = time.time() - start_time
    print(total_time)
    print('time per initial combination:')
    print(total_time / len(full_team))

if __name__ == "__main__":
    main()
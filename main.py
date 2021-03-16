import pandas as pd
from constants import *
from formatting import format_player_data

# main execution function to read player list and generate fantasy teams.
def main():
    data = pd.read_csv('data/fav_players.csv')

    
    # Format
    data = format_player_data(data)
    print(data[:5])
    
    # separate into postions
    defenders = pd.concat([data[data[POSITION1] == 'Defender'], data[data[POSITION2] == 'Defender']])

    forwards = pd.concat([data[data[POSITION1] == 'Forward'], data[data[POSITION2] == 'Forward']])

    midfielders = pd.concat([data[data[POSITION1] == 'Midfielder'], data[data[POSITION2] == 'Midfielder']])

    rucks = pd.concat([data[data[POSITION1] == 'Ruck'], data[data[POSITION2] == 'Ruck']])
    print(rucks)
    

if __name__ == "__main__":
    main()
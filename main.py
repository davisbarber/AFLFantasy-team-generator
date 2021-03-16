import pandas as pd
from constants import *
from Player import Player

# main execution function to read player list and generate fantasy teams.
def main():
    data = pd.read_csv('data/fav_players.csv')
    print(data.shape[0])
    print(data.loc[0,].firstName)
    
    # create players list
    players = []
    
    for i in range(data.shape[0]):
        players.append(Player(data.loc[i,]))
        
    # separate players into positional lists
    
    players[0].print_to_csv()
    

if __name__ == "__main__":
    main()
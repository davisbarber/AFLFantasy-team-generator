class Player:
    """Player class to store info """
    def __init__(self, playerData):
        self.firstName = playerData.firstName
        self.lastName = playerData.lastName
        # can have up to two positions
        self.position = [playerData.pos1]
        if playerData.pos2 != None:
            self.position.append(playerData.pos2)
        else:
            self.position.append('')
            
        self.price = int(playerData.price.strip('$k')) # price in thousands of dollars
        self.average = playerData.average # 2020 average points per game
        self.lastThree = playerData.last3Avg # average ppg for last 3 games of 2020
        self.projected = playerData.projected
        
    def print_to_csv(self):
        print(f'{self.firstName},{self.lastName},{self.position[0]},{self.position[1]},{self.price},{self.average},{self.lastThree},{self.projected}')

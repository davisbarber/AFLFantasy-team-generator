from enum import Enum

# team size constraints


class Defenders(Enum):
    """Team Structure for Defenders """
    TOTAL = 8
    PREMIUM = 3
    MID_PRICE = 3
    ROOKIE = 0
    BENCH = 2


class Mids(Enum):
    """ Team Structure for Mids """
    TOTAL = 10
    PREMIUM = 3
    MID_PRICE = 3
    ROOKIE = 2
    BENCH = 2


class Rucks(Enum):
    """Team Structure for Rucks """
    TOTAL = 3
    PREMIUM = 1
    MID_PRICE = 0
    ROOKIE = 1
    BENCH = 1


class Forwards(Enum):
    """Team Structure for Forwards """
    TOTAL = 8
    PREMIUM = 1
    MID_PRICE = 3
    ROOKIE = 2
    BENCH = 2


# fantasy salary constraints
class Salary(Enum):

    CAP = 13000  # thousands of dollars
    DEF_MIN = 3000
    DEF_MAX = 4000
    MID_MIN = 3000
    MID_MAX = 6000
    RUCK_MIN = 1000
    RUCK_MAX = 1850
    FWD_MIN = 3000
    FWD_MAX = 4000


class Col(Enum):
    """Column names for input data"""
    FIRSTNAME = 'firstName'
    LASTNAME = 'LASTNAME'
    POSITION1 = 'pos1'
    POSITION2 = 'pos2'
    INCLUDE = 'include'
    LOCK = 'lock'
    BENCH = 'bench'
    PRICE = 'price'
    AVERAGE = 'average'
    LAST3AVG = 'last3Avg'
    PROJECTED = 'projected'
    AAMI = 'aami'

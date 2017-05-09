import random

all_cities = pd.read_csv('data/cities.csv', delimiter='|')
all_cities.loc[:,'city_lowercase'] = all_cities['City'].str.lower()
all_cities.loc[:,'state_lowercase'] = all_cities['State short'].str.lower()
unique_lowercase_states = all_cities.state_lowercase.unique()

# MUST DO: remove states not in the main 50

def get_location(loc):
    """
    Should return the proper abbreviation of a state
    """
    loc_pieces = loc.split(' ')
    loc_pieces = [l.strip(',').lower() for l in loc_pieces]

    for lp in loc_pieces:
        if len(lp)==2:
            state = lp
            if state in unique_lowercase_states:
                return state.upper()


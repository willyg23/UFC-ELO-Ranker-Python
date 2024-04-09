import json
from eloCalculations import EloCalculator
from fight import FightEntity
from fighter import FighterEntity
from datetime import datetime

def create_fighter_entry(fighter_name, fight_entity, data_entry, side):
    """Creates a new fighter entry or returns an existing one.

    Args:
        fighter_name (str):  The name of the fighter.
        fight_entity (FightEntity): The current FightEntity object.
        data_entry (dict):  A single entry from your JSON data.
        side (str): 'R' for red corner fighter, 'B' for blue corner fighter.

    Returns:
        FighterEntity:  The created or updated FighterEntity.
    """

    new_entry = {
        "name": fighter_name,
        "weight_classes": [fight_entity.weight_class],
        "gender": data_entry["gender"],

        "current_win_streak": data_entry[f"{side}_current_win_streak"],  # Dynamic 'R' or 'B'
        "current_loss_streak": data_entry[f"{side}_current_lose_streak"], 

        "avg_SIG_STR_landed": data_entry[f"{side}_avg_SIG_STR_landed"], 
        "avg_SIG_STR_pct": data_entry[f"{side}_avg_SIG_STR_pct"], 
        "avg_SUB_ATT": data_entry[f"{side}_avg_SUB_ATT"], 
        "avg_TD_landed": data_entry[f"{side}_avg_TD_landed"],  
        "avg_TD_pct": data_entry[f"{side}_avg_TD_pct"],  

        "total_rounds_fought": data_entry[f"{side}_total_rounds_fought"],
        "total_title_bouts": data_entry[f"{side}_total_title_bouts"],
        "wins_by_Decision_Majority": data_entry[f"{side}_win_by_Decision_Majority"],
        "wins_by_Decision_Split": data_entry[f"{side}_win_by_Decision_Split"],
        "wins_by_Decision_Unanimous": data_entry[f"{side}_win_by_Decision_Unanimous"],
        "wins_by_KO": data_entry[f"{side}_win_by_KO/TKO"], 
        "wins_by_Submission": data_entry[f"{side}_win_by_Submission"],
        "wins_by_TKO_Doctor_Stoppage": data_entry[f"{side}_win_by_TKO_Doctor_Stoppage"],
        "height_cms": data_entry[f"{side}_Height_cms"],  
        "reach_cms": data_entry[f"{side}_Reach_cms"],  

        "elo": [1200],  
        "fight_history": [fight_entity],  
        "stance": data_entry[f"{side}_Stance"],
        "wins": 0,
        "losses": 0   
    }

    # You need to determine 'R' or 'B' for age more definitively
    if data_entry.get('R_fighter') == fighter_name:
        new_entry['age'] = fight_entity.r_age 
    else:
        new_entry['age'] = fight_entity.b_age

    return FighterEntity(**new_entry)


with open('ufc_data.json', 'r') as f:
    load = json.load(f)

    data = load['items']
# Initialize the eloCalculator object
elo_calculator_object = EloCalculator()  # Assuming you have the EloCalculator class defined

# Python dictionary for the 'eloHashMap' concept
elo_hash_map = {}  # Key: FighterFirstName FighterLastName-month-day-year, Value: ELO

# Dictionaries for Fighters and Fights
_fighters = {}  # Mapping fighter names to FighterEntity objects
_fights = []  # List to hold FightEntity objects



for i in range(len(data) - 1, -1, -1):
    fight_entity = FightEntity()  # Assuming you have a FightEntity class

    # Access the fighter data from the JSON
    fight_entity.r_fighter_string = data[i]['R_fighter']
    fight_entity.b_fighter_string = data[i]['B_fighter']

    # Check if fighters exist in the '_fighters' dictionary
    if fight_entity.b_fighter_string in _fighters:
        fight_entity.b_fighter_entity = _fighters[fight_entity.b_fighter_string]
    if fight_entity.r_fighter_string in _fighters:
        fight_entity.r_fighter_entity = _fighters[fight_entity.r_fighter_string]

    fight_entity.winner = data[i]['Winner']


    fight_entity.r_odds = data[i]['R_odds']
    fight_entity.r_odds = data[i]['B_odds']

    fight_entity.weight_class = data[i]['weight_class']
    fight_entity.finish = data[i]['finish']
    fight_entity.r_age = data[i]['R_age']
    fight_entity.b_age = data[i]['B_age']
    fight_entity.fight_id = data[i]['fight_id'] 
    

    date_to_parse = data[i]['date']  # Assuming format like "MM/DD/YYYY"
    date_format = "%m/%d/%Y"  # Match your date format

    parsed_date = datetime.strptime(date_to_parse, date_format)

    fight_entity.year = parsed_date.year
    fight_entity.month = parsed_date.month
    fight_entity.day = parsed_date.day

    _fights.append(fight_entity)  # Add the entity to the fights list



create_fighter_entry(data[i]['R_fighter'], fight_entity, data, 'R')
fight_entity.r_fighter_entity = _fighters[fight_entity.r_fighter_string]

create_fighter_entry(data[i]['B_fighter'], fight_entity, data, 'B')
fight_entity.b_fighter_entity = _fighters[fight_entity.b_fighter_string]

print('Creation of _fighters hasmap and _fights list has been completed! ')
print('Length of the _fighters hashmap:', len(_fighters))  # Using len() for dictionary length
print('Length of the _fights list:', len(_fights))        # Using len() for list length


_modifiers = []  # Create an empty list
sub_win_input = None  # Assign None directly 
ko_tko_input = None
_modifiers.append(sub_win_input)  # Use append() to add items to a list
_modifiers.append(ko_tko_input)

# elo_hash_map_r = ""  redundant I believe
# elo_hash_map_b = ""  redundant I believe

# current_fighter = None  redundant I believe
date_of_fight = ""  # Empty string for now


for fight in _fights:
    if fight.winner is not None and fight.r_fighter_string is not None and fight.b_fighter_string is not None:
        date_of_fight = f"{fight.month}-{fight.day}-{fight.year}"  # Using an f-string
        elo_calculator_object.set_new_rating(fight.winner, fight.r_fighter_string, fight.b_fighter_string, _fighters, _modifiers, date_of_fight)



# 1. Sorting Fighters
sorted_fighters = sorted(_fighters.items(), key=lambda item: item[1].elo[-1], reverse=True) 

# 2. Iteration and Ranking
rank = 1  # Start rank at 1
for fighter_name, fighter_entity in sorted_fighters:
    print(f'Fighter: {fighter_name} Elo: {fighter_entity.elo[-1]} Win/Loss ratio: W{fighter_entity.wins} L{fighter_entity.losses} Rank: {rank}')
    rank += 1  # Increment rank

print("eloHashMap Test") 
print("fighterEloHashMap test:")
print(_fighters["Jon Jones"].fighter_elo_hash_map["Jon Jones-4-23-2016"])  # 1313
print(_fighters["Jon Jones"].fighter_elo_hash_map["Jon Jones-7-6-2019"])  # 1343
print(_fighters["Alexander Gustafsson"].fighter_elo_hash_map["Alexander Gustafsson-5-28-2017"])  # 1247
print(_fighters["Drew Dober"].fighter_elo_hash_map["Drew Dober-12-13-2014"])  # 1191

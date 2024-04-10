import json
from eloCalculations import EloCalculator
from fight import FightEntity
from fighter import FighterEntity
from datetime import datetime
import seaborn as sns 
import matplotlib.pyplot as plt
import pandas as pd 

with open('ufc_data.json', 'r') as f:
    load = json.load(f)

    data = load['items']

# Initialize the eloCalculator object
elo_calculator_object = EloCalculator()  

# Python dictionary for the 'eloHashMap' concept
elo_hash_map = {}  # Key: FighterFirstName FighterLastName-month-day-year, Value: ELO

# Dictionaries for Fighters and Fights
fighters = {}  # Mapping fighter names to FighterEntity objects. Key = a string of the fighter's name  value = that fighter's fighterEntity
#^note that this could get messed up if there's ever fighters with duplicate names, which our dataset fortunately doesn't have.
#Dealing with duplicate names would be a good feature to introduce in the future.

fights = []  # List to hold FightEntity objects



for i in range(len(data) - 1, -1, -1):
    
    fight_entity = FightEntity()  

   
    fight_entity.r_fighter_string = data[i]['R_fighter']
    fight_entity.b_fighter_string = data[i]['B_fighter']

    # Check if fighters exist in the 'fighters' dictionary
    if fight_entity.b_fighter_string in fighters:
        fight_entity.b_fighter_entity = fighters[fight_entity.b_fighter_string]
    if fight_entity.r_fighter_string in fighters:
        fight_entity.r_fighter_entity = fighters[fight_entity.r_fighter_string]

    fight_entity.winner = data[i]['Winner']


    fight_entity.r_odds = data[i]['R_odds']
    fight_entity.r_odds = data[i]['B_odds']

    fight_entity.weight_class = data[i]['weight_class']
    fight_entity.finish = data[i]['finish']
    fight_entity.r_age = data[i]['R_age']
    fight_entity.b_age = data[i]['B_age']
    fight_entity.fight_id = data[i]['fight_id'] 
    

    date_to_parse = data[i]['date']  # Assuming format like "MM/DD/YYYY"
    date_format = "%m/%d/%Y"  # Match date format

    parsed_date = datetime.strptime(date_to_parse, date_format)

    fight_entity.year = parsed_date.year
    fight_entity.month = parsed_date.month
    fight_entity.day = parsed_date.day

    fights.append(fight_entity)  # Add the entity to the fights list


    if fighters.get(fight_entity.r_fighter_string) is None:  # Check if fighter exists
        new_entry = {
            "name": fight_entity.r_fighter_string,
            "weight_classes": [fight_entity.weight_class],   
            "gender": data[i]["gender"],
            "current_win_streak": data[i]["R_current_win_streak"],
            "current_loss_streak": data[i]["R_current_lose_streak"],
            "avg_SIG_STR_landed": data[i]["R_avg_SIG_STR_landed"],  
            "avg_SIG_STR_pct": data[i]["R_avg_SIG_STR_pct"], 
            "avg_SUB_ATT": data[i]["R_avg_SUB_ATT"], 
            "avg_TD_landed": data[i]["R_avg_TD_landed"],  
            "avg_TD_pct": data[i]["R_avg_TD_pct"],  
            "total_rounds_fought": data[i]["R_total_rounds_fought"],
            "total_title_bouts": data[i]["R_total_title_bouts"],
            "wins_by_Decision_Majority": data[i]["R_win_by_Decision_Majority"],
            "wins_by_Decision_Split": data[i]["R_win_by_Decision_Split"],
            "wins_by_Decision_Unanimous": data[i]["R_win_by_Decision_Unanimous"],
            "wins_by_KO": data[i]["R_win_by_KO/TKO"],
            "wins_by_Submission": data[i]["R_win_by_Submission"],
            "wins_by_TKO_Doctor_Stoppage": data[i]["R_win_by_TKO_Doctor_Stoppage"],
            "height_cms": data[i]["R_Height_cms"],  
            "reach_cms": data[i]["R_Reach_cms"],  
            "elo": [1200],  
            "fight_history": [fight_entity],  
            "stance": data[i]["R_Stance"],
            "wins": 0,
            "age": fight_entity.r_age,
            "losses": 0   
        }
        fighters[fight_entity.r_fighter_string] = FighterEntity(**new_entry)

    # Link the entity to the fight
    fight_entity.r_fighter_entity = fighters[fight_entity.r_fighter_string]


    if fighters.get(fight_entity.b_fighter_string) is None: 
        new_entry = {
            "name": fight_entity.b_fighter_string,
            "weight_classes": [fight_entity.weight_class],   
            "gender": data[i]["gender"],
            "current_win_streak": data[i]["B_current_win_streak"],
            "current_loss_streak": data[i]["B_current_lose_streak"],
            "avg_SIG_STR_landed": data[i]["B_avg_SIG_STR_landed"], 
            "avg_SIG_STR_pct": data[i]["B_avg_SIG_STR_pct"], 
            "avg_SUB_ATT": data[i]["B_avg_SUB_ATT"], 
            "avg_TD_landed": data[i]["B_avg_TD_landed"],  
            "avg_TD_pct": data[i]["B_avg_TD_pct"],  
            "total_rounds_fought": data[i]["B_total_rounds_fought"],
            "total_title_bouts": data[i]["B_total_title_bouts"],
            "wins_by_Decision_Majority": data[i]["B_win_by_Decision_Majority"],
            "wins_by_Decision_Split": data[i]["B_win_by_Decision_Split"],
            "wins_by_Decision_Unanimous": data[i]["B_win_by_Decision_Unanimous"],
            "wins_by_KO": data[i]["B_win_by_KO/TKO"],
            "wins_by_Submission": data[i]["B_win_by_Submission"],
            "wins_by_TKO_Doctor_Stoppage": data[i]["B_win_by_TKO_Doctor_Stoppage"],
            "height_cms": data[i]["B_Height_cms"],  
            "reach_cms": data[i]["B_Reach_cms"],  
            "elo": [1200],  
            "fight_history": [fight_entity],  
            "stance": data[i]["B_Stance"],
            "wins": 0,
            "age": fight_entity.b_age,  
            "losses": 0   
        }
        fighters[fight_entity.b_fighter_string] = FighterEntity(**new_entry)

    # Link the entity to the fight
    fight_entity.b_fighter_entity = fighters[fight_entity.b_fighter_string] 

#------------------------------------------end of the for loop that creates the fight list and fighters hashmap


print('Creation of fighters hasmap and fights list has been completed! ')
print('Length of the fighters hashmap:', len(fighters))  # Using len() for dictionary length
print('Length of the fights list:', len(fights))        # Using len() for list length


_modifiers = []  # Create an empty list
sub_win_input = None  # Assign None directly 
ko_tko_input = None
_modifiers.append(sub_win_input)  # Use append() to add items to a list
_modifiers.append(ko_tko_input)




date_offight = ""  # Empty string for now


for fight in fights:
    if fight.winner is not None and fight.r_fighter_string is not None and fight.b_fighter_string is not None:
        date_offight = f"{fight.month}-{fight.day}-{fight.year}"  # Using an f-string
        elo_calculator_object.setNewRating(fight.winner, fight.r_fighter_string, fight.b_fighter_string, fighters, _modifiers, date_offight)

# 1. Sorting Fighters
sortedfighters = sorted(fighters.items(), key=lambda item: item[1].elo[-1], reverse=True) 

# 2. Iteration and Ranking
# have the highest ranked fighter print last, so in the terminal, you'll see the highest ranked fighters first.
rank = 1749  # Start rank at 1749 (amount of fighters)
for fighter_name, fighter_entity in sorted(sortedfighters, key=lambda item: item[1].elo[-1]): # No reverse=True needed
    print(f'Fighter: {fighter_name} Elo: {fighter_entity.elo[-1]} Win/Loss ratio: W{fighter_entity.wins} L{fighter_entity.losses} Rank: {rank}')
    rank -= 1  # decrement rank

print("eloHashMap Test") 
print("fighterEloHashMap test:")
print(fighters["Jon Jones"].fighterEloHashMap["Jon Jones-4-23-2016"])  # 1313
print(fighters["Jon Jones"].fighterEloHashMap["Jon Jones-7-6-2019"])  # 1343
print(fighters["Alexander Gustafsson"].fighterEloHashMap["Alexander Gustafsson-5-28-2017"])  # 1247
print(fighters["Drew Dober"].fighterEloHashMap["Drew Dober-12-13-2014"])  # 1191


def reformat_date(date_str):
    """Reformats dates from 'Name-MM-DD-YYYY' to 'MM-DD-YYYY' """
    if '-' in date_str: 
        parts = date_str.split('-')
        return '-'.join(parts[1:])  # Re-assemble as MM-DD-YYYY
    else:
        return date_str  # No change needed



data = []  # Will collect data for the graph



for fighter_name, fighter in fighters.items():
    for fight_date, elo in fighter.fighterEloHashMap.items():
        print(fight_date)
        data.append({
            'Fighter': fighter_name,
            'Date': reformat_date(fight_date),  # Apply reformatting
            'Elo': elo
        })

# Create the DataFrame
df = pd.DataFrame(data)
df['Date'] = pd.to_datetime(df['Date'], format='%m-%d-%Y') 

# # Create the Seaborn Line Plot
# sns.lineplot(data=df, x='Date', y='Elo', hue='Fighter') 
# plt.xticks(rotation=45) 
# plt.title("Fighter Elo over Time") 
# plt.show()


# ---SEARCH FUNCTIONALITY---
fighterSearchVar = "Drew Dober"  

# Filter the DataFrame based on the search term
filtered_df = df[df['Fighter'] == fighterSearchVar] 

# Create the new line plot with filtered data
sns.lineplot(data=filtered_df, x='Date', y='Elo')  # No need for 'hue' with a single fighter
plt.xticks(rotation=45) 
plt.title(f"Fighter Elo over Time: {fighterSearchVar}") 
plt.show()
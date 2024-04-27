#frontend code is very bad and was meant to quickly produce a UI. Improvements will be made in the future! 

import json
from createFighterEntityFunction import create_fighter
from eloCalculations import EloCalculator
from fight import FightEntity
from fighter import FighterEntity
from datetime import datetime
import seaborn as sns 
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
import sys
# st.write("Running Python version:", sys.version)

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


#loop where we populate the 'fights' list and 'fighters' hashmap
#we start from the bottom of the JSON file, as that's the chroniclogical order of fights
for i in range(len(data) - 1, -1, -1):
    
    #create a fight entity for each fight we parse form the JSON
    fight_entity = FightEntity()

#it is useful to have both the fighter entity and the fighter string, since the key to the _fighters hashmap is a string, the string version is needed.
#though maybe we could parse the name of the fighterEntity to a string or something. Will think about that optimization later.
    fight_entity.r_fighter_string = data[i]['R_fighter']
    fight_entity.b_fighter_string = data[i]['B_fighter']

    # Check if fighters exist in the 'fighters' dictionary
    
    # if _fightEntity.b_fighter is in the _fighters hashmap, add b_fighter's fighterEntity (accessed via the _fighters hashmap) to 
    # _fightEntity's b_fighter_entity value (_fightEntity.b_fighter_entity)
    
    if fight_entity.b_fighter_string in fighters:
        fight_entity.b_fighter_entity = fighters[fight_entity.b_fighter_string]
    #same thing but for r 
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


#optimize this to be just one constructor in the future. make it into a function?

    if fighters.get(fight_entity.r_fighter_string) is None:  # Check if fighter exists
        # add the fighter  entry to the fighters hash map
        fighters[fight_entity.r_fighter_string] = FighterEntity(**create_fighter(fight_entity, data, "R", i))

    # Set the fight entity's r_fighter_entity field, with the fighterEntity of the Red corner fighter
    fight_entity.r_fighter_entity = fighters[fight_entity.r_fighter_string]


    if fighters.get(fight_entity.b_fighter_string) is None:  # Check if fighter exists
        # add the fighter  entry to the fighters hash map
        fighters[fight_entity.b_fighter_string] = FighterEntity(**create_fighter(fight_entity, data, "B", i))
        

    # Set the fight entity's b_fighter_entity field, with the fighterEntity of the Blue corner fighter
    fight_entity.b_fighter_entity = fighters[fight_entity.b_fighter_string] 

#------------------------------------------end of the for loop that creates the fight list and fighters hashmap


print('Creation of fighters hasmap and fights list has been completed! ')
print('Length of the fighters hashmap:', len(fighters))  # fighters hashmap length
print('Length of the fights list:', len(fights))        # fight list length

#modifiers, future implementation
_modifiers = []  
sub_win_input = None  
ko_tko_input = None
_modifiers.append(sub_win_input) 
_modifiers.append(ko_tko_input)




date_of_fight = ""  # Empty string for now


for fight in fights:
    if fight.winner is not None and fight.r_fighter_string is not None and fight.b_fighter_string is not None:
        date_of_fight = f"{fight.month}-{fight.day}-{fight.year}"  # Using an f-string
        elo_calculator_object.setNewRating(fight.winner, fight.r_fighter_string, fight.b_fighter_string, fighters, _modifiers, date_of_fight)

# 1. Sorting Fighters
sortedfighters = sorted(fighters.items(), key=lambda item: item[1].elo[-1], reverse=True) 

# 2. Iteration and Ranking
# have the highest ranked fighter print last, so in the terminal, you'll see the highest ranked fighters first.
rank = len(fighters)  # initialize rank to the length of the fighters hashmap, which is currently 1749
for fighter_name, fighter_entity in sorted(sortedfighters, key=lambda item: item[1].elo[-1]): # No reverse=True needed
    print(f'Fighter: {fighter_name} Elo: {fighter_entity.elo[-1]} Win/Loss ratio: W{fighter_entity.wins} L{fighter_entity.losses} Rank: {rank}')
    rank -= 1  # decrement rank

print("eloHashMap Test") 
print("fighterEloHashMap test:")
print(fighters["Jon Jones"].fighterEloHashMap["Jon Jones-4-23-2016"])  # should be 1313
print(fighters["Jon Jones"].fighterEloHashMap["Jon Jones-7-6-2019"])  # should be 1343
print(fighters["Alexander Gustafsson"].fighterEloHashMap["Alexander Gustafsson-5-28-2017"])  # should be 1247
print(fighters["Drew Dober"].fighterEloHashMap["Drew Dober-12-13-2014"])  # should be 1191

# Reformats dates from 'Name-MM-DD-YYYY' to 'MM-DD-YYYY'
def reformat_date(date_str):
    if '-' in date_str: 
        parts = date_str.split('-')
        return '-'.join(parts[1:])  # Re-assemble as MM-DD-YYYY
    else:
        return date_str  # No change needed



data = []  # Will collect data for the graph

# Populate the 'data' with the necessary data for our graph
for fighter_name, fighter in fighters.items():
    formatted_fighter_name = fighter_name.replace(" ", "").lower()  # Remove spaces and convert to lowercase
    for fight_date, elo in fighter.fighterEloHashMap.items():
        # print(fight_date) # for testing fight_date formatting
        data.append({
            'Fighter': formatted_fighter_name,
            'Date': reformat_date(fight_date),  # Apply reformatting
            'Elo': elo,
            'weight_class': fighter.weight_classes[0] 
        })

df = pd.DataFrame(data) # Create the dataframe
df['Date'] = pd.to_datetime(df['Date'], format='%m-%d-%Y')  #parse date columns into datetime objects


#first graph impl

# sns.lineplot(data=df, x='Date', y='Elo', hue='Fighter') 
# plt.xticks(rotation=45) 
# plt.title("Fighter Elo over Time") 
# plt.show()


# Streamlit Section
st.title("UFC ELO Ranker by William Griner")

# URL of your LinkedIn profile
linkedin_url = "https://www.linkedin.com/in/william-griner/"
github_url = "https://github.com/willyg23"

# Markdown badge for LinkedIn
linkedin_badge = f"[![LinkedIn](https://img.shields.io/badge/LinkedIn-%230077B5.svg?logo=linkedin&logoColor=white)]({linkedin_url})"
github_badge = f"[![GitHub](https://img.shields.io/badge/GitHub-%23181717.svg?logo=github&logoColor=white)]({github_url})"


# Display badges side by side using Markdown in Streamlit, allowing HTML
badges = f"{linkedin_badge} {github_badge}"
st.markdown(badges, unsafe_allow_html=True)

''' After a heated debate with my friend over who the GOAT of the UFC is, I set out to prove him wrong mathematically. I also love to play online chess. Seeing that chess is a 1v1 sport with a algorithimic ranking system (ELO), we can apply the ELO system to the ranking UFC fighters. Thus allowing us to determine who the best UFC fighter is, mathematically. '''
'''How to use:'''
''' 'Elo Range' to see all fighters' Elos over time'''
''' 'Elo Range' and 'weight_class' to see fighters' Elos in a certain weight class over time '''
''' 'Search By Fighter Name' to see a specific fighter's elo over time. i.e. 'Anderson Silva' '''


# ----- Filtering Features Menu Section Start-----

features = ["Elo Range", "weight_class", "Search By Fighter Name"] # Add "weight_class" to features
selected_features = st.multiselect("Select Filtering Features:", features, default=["Elo Range"]) #default makes 'Elo Range' be selected by default

# ----- Filtering Features Menu Section End -----


# ----- filtering features section Start----- 
    # ------ Conditional Display of Filtering Components Section Start -----
elo_mode = None  
elo_lower_bound = None
elo_upper_bound = None
filtered_df = df.copy() # so we can maintain the orignal df for whenever we need it.

        # ----- Search By Fighter Name section Start -----
if "Search By Fighter Name" in selected_features:
    selected_features = ["Search By Fighter Name"] # clears the other options that are selected. havnig Search by fighter name and other featues selected at the same time breaks the app.
    fighterSearchInput = st.text_input("Search for a Fighter:", "Conor Mcgregor")
    fighterSearchVar = fighterSearchInput.replace(" ", "").lower()  # Process input to remove spaces and convert to lowercase

    filtered_df = df[df['Fighter'] == fighterSearchVar]

    # --- Create plot for searched fighter ---
    plt.figure(figsize=(10, 6))  # Create a new figure
    sns.lineplot(data=filtered_df, x='Date', y='Elo', hue='Fighter', legend=False)
    plt.xticks(rotation=45)
    plt.title(f"Fighter Elo over Time: {fighterSearchInput}")  # Dynamic title using the original input for display

    legend_container = st.empty()  # Placeholder for the legend

    # ... (Update `update_display` function to only handle legend if needed)

    st.pyplot(plt)  # Display using Streamlit
        # ----- Search By Fighter Name section End -----    

            # ----- Elo filtering mode section Start -----
else: # 'if Search Fighter By Name' isn't selected
            # ----- Elo filtering mode section Start -----
    # this is supposed to check if "Elo Range" is within features, not if features is ONLY "Elo Range".
    if "Elo Range" in selected_features:
        st.subheader("Elo Filtering") 
        elo_mode = st.selectbox("Elo Filtering Mode:", ["above", "below", "within"])

        if elo_mode in ["above", "below"]:  # Combine cases for 'above' and 'below'
            elo_threshold = st.number_input(f"Elo Threshold ({elo_mode}):", value=1100 if elo_mode == "above" else 1100, step=25)

        else:  # 'within' mode
            col1, col2 = st.columns(2)  
            with col1:
                elo_lower_bound = st.number_input("Elo Lower Bound:", value=1300, step=25)
            with col2:
                elo_upper_bound = st.number_input("Elo Upper Bound:", value=1400, step=25)

    # Data Filtering 

    # this if statement applies the filtering logic to the dataframe based on the selected options.
    if elo_mode == "above":
        filtered_df = filtered_df[filtered_df['Elo'] > elo_threshold]
    elif elo_mode == "below":
        filtered_df = filtered_df[filtered_df['Elo'] < elo_threshold]
    else:  # 'within' mode
        filtered_df = filtered_df[(filtered_df['Elo'] >= elo_lower_bound) & (filtered_df['Elo'] <= elo_upper_bound)] 

            # ----- Elo filtering mode section End -----
            # ----- weight_classes filtering mode section Start -----

    if "weight_class" in selected_features:
        weight_classes = df['weight_class'].unique().tolist()  # Get unique weight_classes
        selected_weight_class = st.selectbox("Select weight_class:", weight_classes)
        filtered_df = filtered_df[filtered_df['weight_class'] == selected_weight_class]

    # print(df.columns)
            # ----- weight_classes filtering mode section End -----




        # ------ Conditional Display of Filtering Components Section End -----
    # ----- filtering features section End ----- 


    # Figure Size
    plt.figure(figsize=(10, 6))  

    # Pagination Logic
    current_page = 0  
    fighters_per_page = 15 

    # *** Text on Hover Implementation ***
    hover_label = st.empty()  
    fig = plt.gcf()

    def annotate(x, y):
        print("Hover at:", x, y) 
        closest_fighter = filtered_df[filtered_df['Elo'].abs().sub(y).abs().argmin()]['Fighter'].iloc[0]
        hover_label.text(x, y, closest_fighter)  
        fig.canvas.draw_idle()

    fig.canvas.mpl_connect('motion_notify_event', annotate)  

    # --- Create initial plot --- 
    sns.lineplot(data=filtered_df, x='Date', y='Elo', hue='Fighter', legend=False) 
    plt.xticks(rotation=45) 
    plt.title("Fighter Elo over Time")

    legend_container = st.empty() # Placeholder for the legend
    # fighters_label = st.empty()   # Placeholder for fighter names # displays fighter names outside of graph

    # --- Function to update displayed fighters and legend ---
    def update_display():
        start_index = current_page * fighters_per_page
        end_index = start_index + fighters_per_page
        fighters_to_display = filtered_df['Fighter'].iloc[start_index:end_index].unique()

        # Update the legend
        legend = plt.legend(labels=fighters_to_display)  
        # legend_container.pyplot(legend)  
        legend_container.empty()  # Clear the previous legend
        legend_container.pyplot(fig) # Display the figure with updated legend

        # Update the fighter names label  
        # fighters_label.text("\n".join(fighters_to_display)) # displays fighter names outside of graph

    update_display()  # Initial display

    if st.button("Previous Page"):
        if current_page > 0:  
            current_page -= 1
            update_display()  # Update graph when page changes 
    if st.button("Next Page"):
        current_page += 1
        update_display()  

    fig.canvas.mpl_connect('motion_notify_event', annotate)

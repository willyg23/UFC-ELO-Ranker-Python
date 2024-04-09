import json

# Load the JSON data from the file
with open('test.json', 'r') as f:
    data = json.load(f)

# Access the 'items' list 
items = data['items']

# Iterate through each fight item
for fight in items:
    print("R_fighter:", fight['R_fighter'])
    print("B_fighter:", fight['B_fighter'])
    print("R_odds:", fight['R_odds'])
    print("B_odds:", fight['B_odds'])
    print("-----------------")  # Add a separator between fights 

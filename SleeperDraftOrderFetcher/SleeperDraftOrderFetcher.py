#!python3
"""The purpose of this script is going to be determine the current draft order in a Sleeper Fantasy
Football League utilizing the Sleeper API. It will also take that information and visualize it."""

#Imported packages

#This package has functions used to query the Sleeper API to get all the data needed to get the draft order
import requests

#Get the users Sleeper League ID. This is found in the URL of the individual league on sleeper.app or in the settings of the sleeper mobile app
league_id = input('Enter your league ID: ')

#Get league info using the league ID above
response = requests.get(f'https://api.sleeper.app/v1/league/{league_id}')
league_info = response.json() 

#Get all of the users in the league
response = requests.get(f'https://api.sleeper.app/v1/league/{league_id}/users')
league_users = response.json()

#Get all of the traded picks, this will be used to figure out who has what pick
response = requests.get(f'https://api.sleeper.app/v1/league/{league_id}/traded_picks')
league_traded_picks = response.json()

#Get all rosters in the league, this is where max points for is stored (seems like it gets rid of the max points for value when the season is restarted)
response = requests.get(f'https://api.sleeper.app/v1/league/{league_id}/rosters')
league_rosters = response.json()

#This block will create a new list with only the owners that includes their user ID
users_list = []
owners_only = []

#iterate through each dictionary in the list of users and get rid of the users who are co-owners
for x, y in enumerate(league_users):
    if league_users[x]['is_owner'] == False:
        del league_users[x]

#creates a new list of dictionaries that gives each user their own index with display name and user_id
for i in range(len(league_users)):
    users_list += [{'display_name':league_users[i]['display_name'], 'user_id': league_users[i]['user_id']}]
    
#this adds the roster ID and max_pf to the dictionaries for each owner. Need the roster ID to correlate picks to users and need max_pf to determine draft order.
for i in range(len(league_rosters)):
    for n in range(len(users_list)):
        if league_rosters[i]['owner_id'] == users_list[n]['user_id']:
            users_list[n]['roster_id'] = league_rosters[i]['roster_id']
            users_list[n]['max_pf'] = league_rosters[i]['settings']['ppts']

#The league_traded_picks variable will contain a list of all traded picks, regardless of year. This will get picks that were traded for the upcoming year that will be necessary to see the draft order. If I haven't updated it you could always change it to the year you're looking for the picks for. 
twentythreepicks = []

#appends traded picks to twentythreepicks.
for i in range(len(league_traded_picks)):
    if league_traded_picks[i]['season'] == '2023':
        twentythreepicks.append(league_traded_picks[i])
        
#This adds the picks each user starts with (if you have more or less rounds you'll need to edit this accordingly. Just copy paste and increment the number for more rounds or delete any extra rounds.
for i, j in enumerate(users_list):
    users_list[i]['draft_picks'] = [{'season': '2023', 'round': 1, 'roster_id': users_list[i]['roster_id'], 'owner_id': users_list[i]['roster_id'], 'original_pick': True},
                                         {'season': '2023', 'round': 2, 'roster_id': users_list[i]['roster_id'], 'owner_id': users_list[i]['roster_id'], 'original_pick': True},
                                         {'season': '2023', 'round': 3, 'roster_id': users_list[i]['roster_id'], 'owner_id': users_list[i]['roster_id'], 'original_pick': True},
                                         {'season': '2023', 'round': 4, 'roster_id': users_list[i]['roster_id'], 'owner_id': users_list[i]['roster_id'], 'original_pick': True}]
    


#this block will remove picks that have been traded away by teams by looking at what picks have been traded and comparing them to the list of picks each user currently has.
for i, j in enumerate(twentythreepicks):
    for m, n in enumerate(users_list):
        if twentythreepicks[i]['roster_id'] == users_list[m]['roster_id']:
                
            for o, p in enumerate(users_list[m]['draft_picks']):
                if (users_list[m]['draft_picks'][o]['owner_id'] and users_list[m]['draft_picks'][o]['round']) == (twentythreepicks[i]['roster_id'] and twentythreepicks[i]['round']) and users_list[m]['draft_picks'][o]['original_pick']:
                    del users_list[m]['draft_picks'][o]
                    
#this block will add picks to users that have traded for them
for i, j in enumerate(twentythreepicks):
    for k, l in enumerate(users_list):
        if twentythreepicks[i]['owner_id'] == users_list[k]['roster_id']:
            users_list[k]['draft_picks'].append(twentythreepicks[i])     
            
#this is going to separate the picks into their own lists, going to be used later to print each round
first_round_picks = []
second_round_picks = []
third_round_picks = []
fourth_round_picks = []

for i in range(len(users_list)):
    for j, k in enumerate(users_list[i]['draft_picks']):
        if users_list[i]['draft_picks'][j]['round'] == 1:
            first_round_picks.append(users_list[i]['draft_picks'][j])
        
        elif users_list[i]['draft_picks'][j]['round'] == 2:
            second_round_picks.append(users_list[i]['draft_picks'][j])
            
        elif users_list[i]['draft_picks'][j]['round'] == 3:
            third_round_picks.append(users_list[i]['draft_picks'][j])
            
        elif users_list[i]['draft_picks'][j]['round'] == 4:
            fourth_round_picks.append(users_list[i]['draft_picks'][j])
            
#add max pf and original owner and current owner of each pick to the dictionary
for i in range(len(first_round_picks)):
    for j in range(len(users_list)):
        if first_round_picks[i]['roster_id'] == users_list[j]['roster_id']:
            first_round_picks[i]['owner_max_pf'] = users_list[j]['max_pf']
            first_round_picks[i]['original_owner'] = users_list[j]['display_name']

for i in range(len(first_round_picks)):
    for j in range(len(users_list)):        
        if first_round_picks[i]['owner_id'] == users_list[j]['roster_id']:
            first_round_picks[i]['current_owner'] = users_list[j]['display_name']

for i in range(len(second_round_picks)):
    for j in range(len(users_list)):
        if second_round_picks[i]['roster_id'] == users_list[j]['roster_id']:
            second_round_picks[i]['owner_max_pf'] = users_list[j]['max_pf']
            second_round_picks[i]['original_owner'] = users_list[j]['display_name']

for i in range(len(second_round_picks)):
    for j in range(len(users_list)):        
        if second_round_picks[i]['owner_id'] == users_list[j]['roster_id']:
            second_round_picks[i]['current_owner'] = users_list[j]['display_name']
            
for i in range(len(third_round_picks)):
    for j in range(len(users_list)):
        if third_round_picks[i]['roster_id'] == users_list[j]['roster_id']:
            third_round_picks[i]['owner_max_pf'] = users_list[j]['max_pf']
            third_round_picks[i]['original_owner'] = users_list[j]['display_name']

for i in range(len(third_round_picks)):
    for j in range(len(users_list)):        
        if third_round_picks[i]['owner_id'] == users_list[j]['roster_id']:
            third_round_picks[i]['current_owner'] = users_list[j]['display_name']
            
for i in range(len(fourth_round_picks)):
    for j in range(len(users_list)):
        if fourth_round_picks[i]['roster_id'] == users_list[j]['roster_id']:
            fourth_round_picks[i]['owner_max_pf'] = users_list[j]['max_pf']
            fourth_round_picks[i]['original_owner'] = users_list[j]['display_name']

for i in range(len(fourth_round_picks)):
    for j in range(len(users_list)):        
        if fourth_round_picks[i]['owner_id'] == users_list[j]['roster_id']:
            fourth_round_picks[i]['current_owner'] = users_list[j]['display_name']

#sorts the list of picks by max pf and assigns the lists to a new variable.
draft_order1 = sorted(first_round_picks, key=lambda x: x['owner_max_pf'])
draft_order2 = sorted(second_round_picks, key=lambda x: x['owner_max_pf'])
draft_order3 = sorted(third_round_picks, key=lambda x: x['owner_max_pf'])
draft_order4 = sorted(fourth_round_picks, key=lambda x: x['owner_max_pf'])

#prints column headers
print(f'{"Pick":<5}\t{"Current Owner":<19}\t{"Original Owner":<10}\t\t{"Max PF":>14}')

#these variables will be used to show what pick number each pick is
pick1 = 1.00
pick2 = 2.00
pick3 = 3.00
pick4 = 4.00

#This will print the pick number, the current owner, the original owner, and the original owner's max_pf
for i in range(12):
    print(f"{pick1 + .01 :>4.2f}\t{draft_order1[i]['current_owner']:<20}\t{draft_order1[i]['original_owner']:<20}\t\t{draft_order1[i]['owner_max_pf']:<20}")
    pick1 += .01
    
for i in range(12):
    print(f"{pick2 + .01:>4.2f}\t{draft_order2[i]['current_owner']:<20}\t{draft_order2[i]['original_owner']:<20}\t\t{draft_order2[i]['owner_max_pf']:<20}")
    pick2 += .01
    
for i in range(12):
    print(f"{pick3 + .01:>4.2f}\t{draft_order3[i]['current_owner']:<20}\t{draft_order3[i]['original_owner']:<20}\t\t{draft_order3[i]['owner_max_pf']:<20}")
    pick3 += .01
    
for i in range(12):
    print(f"{pick4 + .01:>4.2f}\t{draft_order4[i]['current_owner']:<20}\t{draft_order4[i]['original_owner']:<20}\t\t{draft_order4[i]['owner_max_pf']:<20}")
    pick4 += .01

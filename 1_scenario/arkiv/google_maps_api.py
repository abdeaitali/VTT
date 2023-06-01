

valid_platssignatur = ["Bål", "Bro", "Kän", "Khä", "Jkb", "Bkb", "Spå", "Sub", "Ke", "Cst", "Sst", "Åbe", "Äs", "Fas", \
                       "Tåd", "Skg", "Hnd", "Jbo", "Vhn", "Kda", "Ts", "Hfa", "Ssä", "Öso", "Ngd", "Gdv", "Nyh"]

import requests


import requests

# Define the API endpoint and parameters
endpoint = 'https://api.trafiklab.se/sl/hallplatser.json'
params = {
    'key': 'd3dfe2aa25d9472898d67b4cfe7fe643',
    'searchstring': 'Barkarby'
}

# Make a request to the API
response = requests.get(endpoint, params=params)
data = response.json()

# Extract the ID of the first stop in the response
stop_id = data['ResponseData'][0]['SiteId']

# Display the stop ID
print(f'The ID of the stop is {stop_id}.')




params = {
    'key': 'd3dfe2aa25d9472898d67b4cfe7fe643',
    'searchstring': 'Gnesta'
}

# Make a request to the API
response = requests.get(endpoint, params=params)
data = response.json()

# Extract the ID of the first location in the response
location_id_2 = data['StopLocation'][0]['id']

# Display the location ID
print(f'The ID of the location is {location_id_2}.')


endpoint = 'https://api.trafiklab.se/sl/reseplanerare.json'
params = {
    'key': 'd3dfe2aa25d9472898d67b4cfe7fe643',
    'originId': location_id_2,
    'destId': location_id_2,
    'searchForArrival': '0',
    'format': 'json'
}

# Make a request to the API
response = requests.get(endpoint, params=params)
data = response.json()

# Extract the travel time for the second best option
travel_time = data['Trip'][1]['dur']

# Display the travel time
print(f'The travel time is {travel_time} minutes.')
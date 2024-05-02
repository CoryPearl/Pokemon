import requests

req = requests.get('https://pokeapi.co/api/v2/pokemon/?limit=811')
json_data = req.json()

results = json_data['results']
file = open("pokemon.txt", "a")

for item in results:
    file.write(f"{item['name']}\n")

file.close()

import requests

URL = "https://pokeapi.co/api/v2/pokemon/"


pokemon = input("Ingrese el nombre del pokemon: ")
respuesta = requests.get(URL + pokemon)
datos = respuesta.json()

print(f"Movimientos de {pokemon}:")
for move in (datos["moves"]):
    print(move["move"]["name"])

print(f"Tipos de {pokemon}:")
for type in (datos["types"]):
    print(type["type"]["name"])

# print(datos["moves"])
import sys
from itertools import combinations

def createFile(ingr):
    with open("A_solution", "w") as f:
        f.write(str(len(ingr))+" ")
        for i in ingr:
            f.write(i+" ")
            print("FINI")


try:
    instance_file = sys.argv[1]
except:
    raise Exception("Erreur à la lecture des arguments")

data = []
try:
    with open(instance_file, "r") as f:
        data = f.readlines()
    data = [l.strip().split() for l in data]
except:
    raise Exception("Erreur lors de la lecture de l'instance")

Nclients = int(data[0][0]) # Nombre total de clients
data.pop(0)

ingredients = dict() # nom d'un ingrédient (str) -> identifiant (entier allant de 0 à N-1)
noms_ingredients = [] # identifiant (entier allant de 0 à N-1, indice dans la liste) -> nom de l'ingrédient (str) qui a cet identifiant

Ningredients = 0

L = [set() for _ in range(Nclients)] # L[i] est la liste des ingrédients que le client i aime (Like)
D = [set() for _ in range(Nclients)] # D[i] est la liste des ingrédients que le client i n'aime pas (Dislike)

for client in range(Nclients):
    Lc,Dc = data[2*client][1:], data[2*client+1][1:] # préférences du client
    for nom_ingr in Lc + Dc:
        if nom_ingr not in ingredients: # nom_ingr n'est pas dans les clés du dictionnaire -> c'est un ingrédient que l'on a pas encore rencontré
            ingredients[nom_ingr] = Ningredients # on lui attribue un numéro unique dans [0;N-1]
            noms_ingredients.append(nom_ingr)
            Ningredients += 1 # incrémenter le compteur d'ingrédients

for i in range(1,Ningredients):
    for j in combinations(ingredients,i):
        createFile(j)
        



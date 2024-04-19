import sys
import subprocess
import random
import math
try:
    instance_file = sys.argv[1]
except:
    raise Exception("Erreur à la lecture des arguments")

iterations = 100
data = []

try:
    with open(instance_file, "r") as f:
        data = f.readlines()
    data = [l.strip().split() for l in data]
except:
    raise Exception("Erreur lors de la lecture de l'instance")

Nclients = int(data[0][0])  # Nombre total de clients
data.pop(0)

noms_ingredients = []  # tableau des ingrédients présents

Ningredients = 0

for client in range(Nclients):
    Lc, Dc = data[2 * client][1:], data[2 * client + 1][1:]  # préférences du client
    for nom_ingr in Lc + Dc:
        if nom_ingr not in noms_ingredients:
            noms_ingredients.append(nom_ingr)
            Ningredients += 1

def generer_pizza():
    pizza = [random.randint(0, 1) for _ in range(Ningredients)] #recette sous forme de liste de bits (0 si ingrédient absent, 1 si présent)
    return pizza


def creer_fichier(ingr):
    with open("solution.txt", "w") as f:
        f.write(str(sum(ingr)) + " ") 
        for i in range(Ningredients):       #création du fichier de solution 
            if ingr[i] == 1:
                f.write(noms_ingredients[i] + " ")

def modification(pizza):
    nouvelle_pizza = pizza
    index = random.randint(0, Ningredients - 1) #on effectue un bit flip: on prend un ingrédient aléatoire on le rajoute si il était absent(0->1), on le retire si il était présent(1 ->0)
    nouvelle_pizza[index] = 1 - nouvelle_pizza[index]
    return nouvelle_pizza   

def calculer_score(pizza):
    creer_fichier(pizza)
    res = subprocess.getoutput("python3 evaluation.py " + str(instance_file) + " solution.txt")
    score = int(res.split()[-1])
    return score

def recuit_simule(T_max,T_min,diminution):
    pizza_actuelle = generer_pizza()
    meilleure_pizza = pizza_actuelle
    score_actuel = calculer_score(pizza_actuelle)
    score_max = score_actuel
    nouvelle_pizza = pizza_actuelle
    while T_max > T_min: #on itère tant qu'on a pas atteint la temperature minimale
        nouvelle_pizza = modification(pizza_actuelle)
        nouveau_score = calculer_score(nouvelle_pizza)
        delta_score = score_max - nouveau_score
        if delta_score <= 0 or random.random() < math.exp(-delta_score/T_max):
            if nouveau_score > score_max: #on affiche le nouveau max s'il change
                score_max = nouveau_score
                meilleure_pizza = nouvelle_pizza
                print("Nouvelle meilleure pizza trouvée: [")
                for i in range(Ningredients):       
                    if meilleure_pizza[i] == 1:
                        print(noms_ingredients[i]+" ")
                print("]")
                print("Score obtenu:", score_max)
            pizza_actuelle = nouvelle_pizza #si la modif est acceptée on change la pizza actuelle
        T_max*=diminution
    return meilleure_pizza,score_max
meilleure_pizza, score_max = recuit_simule(T_max=100, T_min=0.1, diminution=0.9)
print("Meilleure pizza trouvée: [")
for i in range(Ningredients):       
    if meilleure_pizza[i] == 1:
        print(noms_ingredients[i]+" ")
print("]")
print("Score obtenu:", score_max)
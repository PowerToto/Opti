import sys
import subprocess
import random

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

ingredients = dict()  # nom d'un ingrédient (str) -> identifiant (entier allant de 0 à N-1)
noms_ingredients = []  # identifiant (entier allant de 0 à N-1, indice dans la liste) -> nom de l'ingrédient (str) qui a cet identifiant

Ningredients = 0

for client in range(Nclients):
    Lc, Dc = data[2 * client][1:], data[2 * client + 1][1:]  # préférences du client
    for nom_ingr in Lc + Dc:
        if nom_ingr not in ingredients:
            ingredients[nom_ingr] = Ningredients
            noms_ingredients.append(nom_ingr)
            Ningredients += 1

def generer_pizza():
    recette = [random.randint(0, 1) for _ in range(Ningredients)]
    return recette

def croisement(pizza1, pizza2):
    point = random.randint(1, Ningredients - 2)
    new_pizza1 = pizza1[:point] + pizza2[point:]
    new_pizza2 = pizza2[:point] + pizza1[point:]
    return new_pizza1, new_pizza2

def mutation(pizza):
    nouvelle_pizza = pizza[:]
    index = random.randint(0, Ningredients - 1)
    nouvelle_pizza[index] = 1 - nouvelle_pizza[index]
    return nouvelle_pizza

def createFile(ingr):
    with open("solution.txt", "w") as f:
        f.write(str(sum(ingr)) + " ") 
        for i in range(Ningredients):
            if ingr[i] == 1:
                f.write(noms_ingredients[i] + " ")

def algorithme_genetique(taille_population, prob_mut, max_iterations):
    population = [generer_pizza() for _ in range(taille_population)]
    max_score = 0
    meilleure_pizza = None
    
    while max_iterations > 0:
        scores = []
        for pizza in population:
            createFile(pizza)
            res = subprocess.getoutput("python3 evaluation.py " + str(instance_file) + " solution.txt")
            score = int(res.split()[-1])
            scores.append(score)
            if score > max_score:
                max_score = score
                meilleure_pizza = pizza
                print("Nouvelle meilleure pizza trouvée:", meilleure_pizza)
                print("Score obtenu:", max_score)

        # Sélection des parents pour le croisement
        parents = [pizza for _, pizza in sorted(zip(scores, population), key=lambda x: x[0], reverse=True)]

        # Croisement et mutation
        nouvelle_population = []
        while len(nouvelle_population) < taille_population:
            parent1, parent2 = random.sample(parents[taille_population//2:], 2)
            enfant1, enfant2 = croisement(parent1, parent2)
            if random.random() < prob_mut:
                enfant1 = mutation(enfant1)
            if random.random() < prob_mut:
                enfant2 = mutation(enfant2)
            nouvelle_population.extend([enfant1, enfant2])

        population = nouvelle_population
        max_iterations -= 1

    return meilleure_pizza, max_score

meilleure_pizza, meilleur_score = algorithme_genetique(taille_population=100, prob_mut=0.03, max_iterations=iterations)
print("Meilleure pizza trouvée:", meilleure_pizza)
print("Score obtenu:", meilleur_score)

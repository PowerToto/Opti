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

noms_ingredients = []  # identifiant (entier allant de 0 à N-1, indice dans la liste) -> nom de l'ingrédient (str) qui a cet identifiant

Ningredients = 0

for client in range(Nclients):
    Lc, Dc = data[2 * client][1:], data[2 * client + 1][1:]  # préférences du client
    for nom_ingr in Lc + Dc:
        if nom_ingr not in noms_ingredients:
            noms_ingredients.append(nom_ingr)
            Ningredients += 1

def generer_pizza():
    recette = [random.randint(0, 1) for _ in range(Ningredients)] #recette sous forme de liste de bits (0 si ingrédient absent, 1 si présent)
    return recette

def croisement(pizza1, pizza2):
    point = random.randint(1, Ningredients - 2)
    new_pizza1 = pizza1[:point] + pizza2[point:] #on coupe aléatoirement
    new_pizza2 = pizza2[:point] + pizza1[point:]
    return new_pizza1, new_pizza2

def mutation(pizza):
    nouvelle_pizza = pizza
    index = random.randint(0, Ningredients - 1) #on effectue un bit flip on altère: on prend un ingrédient aléatoire on le rajoute si il était absent, on le retire si il était présent
    nouvelle_pizza[index] = 1 - nouvelle_pizza[index]
    return nouvelle_pizza

def createFile(ingr):
    with open("solution.txt", "w") as f:
        f.write(str(sum(ingr)) + " ") 
        for i in range(Ningredients):       #création du fichier de solution 
            if ingr[i] == 1:
                f.write(noms_ingredients[i] + " ")

def algorithme_genetique(taille_population, prob_mut, max_iterations):
    population = [generer_pizza() for _ in range(taille_population)] #génération de la population de base
    max_score = 0
    meilleure_pizza = None
    
    while max_iterations > 0:
        scores = []
        for pizza in population:
            createFile(pizza) #pour chaque pizza on crée un fichier
            res = subprocess.getoutput("python3 evaluation.py " + str(instance_file) + " solution.txt") #on évalue le fichier
            score = int(res.split()[-1]) #on récupère le score (dernière case de l'output)
            scores.append(score)
            if score > max_score: #on affiche le nouveau max
                max_score = score
                meilleure_pizza = pizza
                print("Nouvelle meilleure pizza trouvée: [")
                for i in range(Ningredients):       
                    if meilleure_pizza[i] == 1:
                        print(noms_ingredients[i]+" ")
                print("]")
                print("Score obtenu:", max_score)
            else:
                max_iterations -= 1

    
        parents = [pizza for _, pizza in sorted(zip(scores, population), key=lambda x: x[0])]   # sélection des parents pour le croisement (on forme des couples score,population (même index))
        nouvelle_population = []
        while len(nouvelle_population) < taille_population: 
            parent1, parent2 = random.sample(parents[taille_population//2:], 2) #on prend la deuxième moitié de la population (meilleurs scores)
            enfant1, enfant2 = croisement(parent1, parent2) 
            if random.random() < prob_mut:
                enfant1 = mutation(enfant1)                 #on effectue les croisements et les mutations
            if random.random() < prob_mut:
                enfant2 = mutation(enfant2)
            nouvelle_population.extend([enfant1, enfant2]) #on rajoute les enfants a la population

        population = nouvelle_population

    return meilleure_pizza, max_score

meilleure_pizza, meilleur_score = algorithme_genetique(taille_population=100, prob_mut=0.05, max_iterations=iterations)
print("Meilleure pizza trouvée: [")
for i in range(Ningredients):       
    if meilleure_pizza[i] == 1:
        print(noms_ingredients[i]+" ")
print("]")
print("Score obtenu:", meilleur_score)

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

Nclients = int(data[0][0]) # Nombre total de clients
data.pop(0)

ingredients = dict() # nom d'un ingrédient (str) -> identifiant (entier allant de 0 à N-1)
noms_ingredients = [] # identifiant (entier allant de 0 à N-1, indice dans la liste) -> nom de l'ingrédient (str) qui a cet identifiant

Ningredients = 0

for client in range(Nclients):
    Lc,Dc = data[2*client][1:], data[2*client+1][1:] # préférences du client
    for nom_ingr in Lc + Dc:
        if nom_ingr not in ingredients: # nom_ingr n'est pas dans les clés du dictionnaire -> c'est un ingrédient que l'on a pas encore rencontré
            ingredients[nom_ingr] = Ningredients # on lui attribue un numéro unique dans [0;N-1]
            noms_ingredients.append(nom_ingr)
            Ningredients += 1 
def generer_pizza():
    L = []
    #plutot prendre dans nom_ingredients ?
    L.append(random.choice(list(ingredients.keys())))
    return L

def croisement (pizza1,pizza2):
    point = random.randint(1, len(ingredients) - 2)
    new_pizza1 = pizza1[:point]+pizza2[point:]
    new_pizza2 = pizza2[:point]+pizza1[point:]
    return set(new_pizza1),set(new_pizza2)

def mutation(pizza):
    nouvelle_pizza = pizza
    new_ing = random.choice(list(ingredients.keys()))
    while new_ing in nouvelle_pizza:
        new_ing = random.choice(list(ingredients.keys()))
    nouvelle_pizza.add(new_ing)
    return set(nouvelle_pizza)

def createFile(ingr):
    with open("solution.txt", "w") as f:
        f.write(str(len(ingr))+" ")
        for i in ingr:
            f.write(i+" ")

def algorithme_genetique(taille_population, prob_mut, max_iterations):
    population = []
    scores = []
    for _ in range(taille_population):
        pizz = generer_pizza()
        while pizz in population:
            pizz = generer_pizza()
        population.append(pizz)
    max_score = 0
    while max_iterations != 0:
        # Évaluation de la population
        for pizza in population:
            createFile(pizza)
            res = subprocess.getoutput("python3 evaluation.py " + str(instance_file) + " solution.txt")
            score = int(res.split()[-1])
            scores.append(score)
            if score > max_score:
                max_iterations = iterations
                meilleure_pizza, max_score = pizza, score
                print(str(pizza) + " " + str(score))
            else:
                max_iterations = max_iterations - 1

        # Sélection des parents pour le croisement
        parents = [pizza for _, pizza in sorted(zip(scores, population), key=lambda x: x[0])]
        # Croisement et mutation)
        nouvelle_population = []
        while len(nouvelle_population) < taille_population:
            parent1, parent2 = random.sample(parents[taille_population//2:], 2)
            enfant1, enfant2 = croisement(list(parent1), list(parent2))
            if random.random() < prob_mut:
                enfant1 = mutation(enfant1)
            if random.random() < prob_mut:
                enfant2 = mutation(enfant2)
            #on retire les doublons et on retrie a chaque fois pour verifier les doublons potentiels
            if enfant1 not in nouvelle_population:  
                nouvelle_population.append(enfant1)
            if enfant2 not in nouvelle_population:  
                nouvelle_population.append(enfant2)
            population = nouvelle_population
    return meilleure_pizza, max_score

meilleure_pizza, meilleur_score = algorithme_genetique(taille_population=100, prob_mut=0.03, max_iterations=iterations)
print("Meilleure pizza trouvée:", meilleure_pizza)
print("Score obtenu:", meilleur_score)
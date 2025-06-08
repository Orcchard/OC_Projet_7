"""
Recherche par Brute Force de la combinaison d'actions maximisant le profit
sans dépasser un budget donné.
Ce script charge un jeu de données contenant une liste d'actions avec leur coût et
leur pourcentage de profit. Il utilise une approche récursive par force brute
pour trouver la combinaison d'actions qui maximise le profit sans dépasser un
budget donné.

Étapes :
1. Chargement et nettoyage des données depuis un fichier CSV(Dataframe)
2. Filtrage des actions ayant un coût ou un profit nul ou négatif.

    Devrait Retourner :
    - total_profit (float) : profit total de la meilleure combinaison.
    - meilleure_combinaison:
    Brute Force O(2^n) où n nombre d'actions = 1000 
    La complexité temporelle de la méthode force brute = 2^1000
    ≈ 10^301 "combinaisons possibles"  donc irréalisable.
    """

import time
import pandas as pd


# Chargement du dataset
dataset = pd.read_csv("dataset1.csv")

# Affiche toutes les lignes et colonnes
pd.set_option("display.max_rows", None)      # pour voir toutes les lignes
pd.set_option("display.max_columns", None)   # pour voir toutes les colonnes

# Affichage de la description du dataset
dataset = dataset[(dataset["price"] > 0) & (dataset["profit"] > 0)]
print(dataset.describe())
# print(dataset)


def recursive_force_brute(capacity, dataset, current_selection=None):
    """
    Methode brute force On travaille sur un sous-problème à chaque appel récursif.
    À chaque appel récursif : Elle se trouve face à un choix :

    Ne pas prendre l'objet courant :Elle appelle la même fonction
    sur le reste des objets (sans changer la capacité).

    Ou prendre l'objet courant (si son poids le permet)
    Elle appelle la même fonction sur le reste des objets
    mais en réduisant la capacité du sac par le poids de l'objet courant,
    et en ajoutant l'objet courant à la sélection.
    """
    if current_selection is None:
        current_selection = []
    if dataset.empty:
        total_profit = sum(row[1] * row[2] / 100 for row in current_selection)
        return total_profit, current_selection

    # On récupère la première ligne (action actuelle) avec iloc(integer-location based indexing)
    # actions[0] correspond à l’action en cours de traitement subproblems.
    current_action = dataset.iloc[0]
    name = current_action["name"]
    price = current_action["price"]
    profit = current_action["profit"]

    reste_dataset = dataset.iloc[1:]

    # Cas où l'on n'inclut pas l'action actuelle
    profit_sans, combinaison_sans = recursive_force_brute(
        capacity, reste_dataset, current_selection
    )
    # Cas où l'on inclut l'action actuelle si elle respecte le budget
    if price <= capacity:
        profit_avec, combinaison_avec = recursive_force_brute(
            capacity - price,
            reste_dataset,
            current_selection + [[name, price, profit]]  # Une liste contenant une sous-liste.
        )
        if profit_avec > profit_sans:
            return profit_avec, combinaison_avec

    return profit_sans, combinaison_sans


BUDGET = 50  # Budget maximal en centimes
start_time = time.time()

# Lancement de la recherche
profit, meilleure_selection = recursive_force_brute(BUDGET, dataset)

end_time = time.time()
execution_time = end_time - start_time

# --- Affichage des résultats ---
total_cout = sum([a[1] for a in meilleure_selection])
print(f"\nCoût total : {total_cout:.2f} €")
print(f"Profit total : {profit:.2f} €")

print("Meilleure combinaison d'actions :")
for name, price, profit in meilleure_selection:
    print(f"{name} | Coût : {price:.2f} € | Profit : {profit:.2f} €")
print(f"Temps d'exécution : {execution_time:.4f} secondes")

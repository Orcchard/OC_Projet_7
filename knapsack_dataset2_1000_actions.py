"""
La librairie Panda, permet de créer un data frame.
Importation du fichier  dataset1.csv qui sera lu et transformé en data frame 
à partir de la fonction read_dataset1.csv. 
1000 Actions contenues dans un fichier dataset1.csv , entetes du fichier .csv
Name: Nom de l'action
Price:  Prix de l'action
Profit en %
"""

import time
import pandas as pd


W = 50000  # capacité maximale du sac

# Chargement du dataset
dataset = pd.read_csv("dataset2.csv")
pd.set_option("display.max_rows", None)      # pour voir toutes les lignes
pd.set_option("display.max_columns", None)   # pour voir toutes les colonnes

# Nettoyage : on enlève les lignes avec des valeurs nulles ou négatives
dataset = dataset[(dataset["price"] > 0) & (dataset["profit"] > 0)]
print(dataset.describe())
print(dataset)



# Création des listes à partir des colonnes dans le cas le Knapsack, 
# c’est le plus simple et le plus lisible. .tolist() permet de :
# convertir les objets en list native Python.
names = dataset["name"].tolist()
dataset["price_cent"] = (dataset["price"] * 100).astype(int)
costs = dataset["price_cent"].tolist()
dataset["profit_euros"] = dataset["price"] * dataset["profit"] / 100
profits = dataset["profit_euros"].tolist()


def knapsack_bottom_up(W, item_costs, item_profits):
    """
    Résout le problème du sac à dos (Knapsack) en utilisant la programmation dynamique (bottom-up).
    item_costs (list of float or int): Liste des coûts de chaque action (prix d'achat).
        item_profits (list of float): Liste des profits attendus (en euros) pour chaque action.
        Chaque action peut être soit prise une seule fois, soit pas du tout (0/1).
    """
    n = len(item_costs)
    dp = [[0 for colonne in range(W + 1)] for line in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(W + 1):
            if item_costs[i - 1] <= w:
                dp[i][w] = max(
                    item_profits[i - 1] + dp[i - 1][w - item_costs[i - 1]],
                    dp[i - 1][w]
                )
            else:
                dp[i][w] = dp[i - 1][w]

    # Recherche des actions sélectionnées
    selected_actions = []
    w = W
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            selected_actions.append(i - 1)
            w -= item_costs[i - 1]
    selected_actions.reverse()  # Pour les remettre dans l'ordre initial
    return dp[n][W], selected_actions


# Exécution
start = time.time()
max_profit, selected_actions = knapsack_bottom_up(W, costs, profits)
end = time.time()

# Résultats
total_cost = sum(costs[i] for i in selected_actions)
print(f"\nCoût total investi : {total_cost/100:.2f} €")
print(f"Bénéfice maximal : {max_profit:.2f} €")
print(f"\033[1m{len(selected_actions)} Actions retenues :\033[0m")
for i in selected_actions:
    print(f"{names[i]} | Coût : {costs[i]/100} € | Profit : {profits[i]:.2f} €")
print(f"\n Temps d'exécution : {end - start:.4f} secondes")
# .4 signifie 4 chiffres après la virgule.

"""
Résolution du problème de sélection d'actions par méthode du sac à dos (knapsack)

Approche par programmation dynamique pour sélectionner un portefeuille optimal de 20 actions
avec un budget maximum de 500 €.

Concepts clés :
- Poids (weight) : coût de l'action (en euros)
- Valeur (value) : profit attendu après 2 ans (en euros)
- Capacité maximale (W) : budget total disponible (500 €)

Principe algorithmique :
Pour chaque action :
    Si le coût de l'action est inférieur ou égal à la capacité restante :
        On compare deux options :
        1. Prendre l'action : ajout du profit + optimisation du budget restant
        2. Ne pas prendre l'action : conservation du profit précédent
        On conserve l'option la plus profitable
    Sinon (coût trop élevé) : On conserve la solution précédente

Complexité :
- Temporelle : O(n×W) = 20×500 = 10 000 opérations
- Spatiale : O(n×W) = tableau de 20×500 cases

Retourne :
- Le profit maximal réalisable
- La liste des indices des actions sélectionnées
- Le coût total du portefeuille
"""

import time


W = 500  # capacité maximale du "sac à dos"
# n = nombre total d’actions.
# costs : 	costs : liste des coûts des objets (ici, les actions)
# profits : liste des profits associés à chaque objet

start_time = time.time()


def knapsack_bottom_up(W, item_costs, item_profits):
    """ Optimisation avec la méthode sac à dos"""
    n = len(costs)
    dp = [[0 for colonne in range(W + 1)] for line in range(n + 1)]
    # Dynamic Programme table
    for i in range(1, n + 1):
        for w in range(W + 1):
            if item_costs[i - 1] <= w:
                # dp[i][w] : le bénéfice maximal qu'on peut
                # obtenir avec les i premiers objets et une capacité  de w.
                dp[i][w] = max(
                    item_profits[i - 1] + dp[i - 1][w - costs[i - 1]],
                    dp[i - 1][w])
            else:
                dp[i][w] = dp[i - 1][w]
        # Recherche des actions sélectionnées
        selected_actions = []
        w = W
        for i in range(n, 0, -1):
            if dp[i][w] != dp[i - 1][w]:
                selected_actions.append(i - 1)
                w -= costs[i - 1]
        selected_actions.reverse()  # Pour les remettre dans l'ordre initial
    return dp[n][W], selected_actions


names = [
    "Action-1", "Action-2", "Action-3", "Action-4", "Action-5",
    "Action-6", "Action-7", "Action-8", "Action-9", "Action-10",
    "Action-11", "Action-12", "Action-13", "Action-14", "Action-15",
    "Action-16", "Action-17", "Action-18", "Action-19", "Action-20"
    ]
costs = [
    20, 30, 50, 70, 60, 80, 22, 26, 48, 34, 42,
    110, 38, 14, 18, 8, 4, 10, 24, 114]
profits = [
    1.00, 3.00, 7.50, 14.00, 10.20, 20.00, 1.54, 2.86, 6.24, 9.18,
    7.14, 9.90, 8.74, 0.14, 0.54, 0.64, 0.48, 1.40, 5.04, 20.52
]
start_time = time.time()
max_profit, selected_actions = knapsack_bottom_up(W, costs, profits)
end_time = time.time()
execution_time = end_time - start_time
total_cost = sum(costs[i] for i in selected_actions)

# Affichage des résultats
print(f"\n----Coût total investi---- : {total_cost} €")
print(f"----Bénéfice maximal---- : {max_profit:.2f} €")
# Le f signifie "float".

print("\n Actions retenues :")
for i in selected_actions:
    print(f"{names[i]} | Coût : {costs[i]} € | Profit : {profits[i]:.2f} €")

print(f"\n Temps d'exécution : {execution_time:.4f} secondes")
# .4 signifie 4 chiffres après la virgule.

"""
La librairie Panda, permet de créer un data frame.
Importation du fichier  dataset1.csv et dataset2 qui seront lus et transformés en data frame
à partir de la fonction read_dataset1.csv.
1000 Actions contenues  dans les fichiers dataset1.csv & dataset2.csv , entetes des fichiers .csv
Name: Nom de l'action
Price:  Prix de l'action
Profit en %
"""

import sys
import time
import pandas as pd

BUDGET_EUROS = 500

# Données des 20 actions.
small_dataset = {
    "names": [
            "Action-1", "Action-2", "Action-3", "Action-4", "Action-5",
            "Action-6", "Action-7", "Action-8", "Action-9", "Action-10",
            "Action-11", "Action-12", "Action-13", "Action-14", "Action-15",
            "Action-16", "Action-17", "Action-18", "Action-19", "Action-20"
            ],
    "costs": [
        20, 30, 50, 70, 60, 80, 22, 26, 48, 34, 42,
        110, 38, 14, 18, 8, 4, 10, 24, 114],
    "profits": [
        1.00, 3.00, 7.50, 14.00, 10.20, 20.00, 1.54, 2.86, 6.24, 9.18,
        7.14, 9.90, 8.74, 0.14, 0.54, 0.64, 0.48, 1.40, 5.04, 20.52
    ],
    "budget": 500
    }


def knapsack_bottom_up(W, item_costs, item_profits):
    """
    Résout le problème du sac à dos (Knapsack) en utilisant la programmation dynamique (bottom-up).
    item_costs : Liste des coûts de chaque action (prix d'achat).
        item_profits : Liste des profits attendus (en euros) pour chaque action.
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


def prepare_data(df):
    """Préparation des datasets csv
    c’est le plus simple et le plus lisible. .tolist() permet de
    convertir les objets en list native Python."""
    df = df.copy()  # Crée une copie explicite
    # pour éviter une modification involontaire du DataFrame original passé en argument.
    df["price_cent"] = (df["price"] * 100).astype(int)
    df["profit_euros"] = df["price"] * df["profit"] / 100
    return (
        df["name"].tolist(),
        df["price_cent"].tolist(),
        df["profit_euros"].tolist()
        )


def run_csv_analysis(file_path, budget_euros):
    """Analyse un fichier CSV contenant des données d'actions
    pour appliquer un algorithme de type sac à dos.
    Cette fonction lit un fichier CSV, nettoie les données
    (suppression des lignes avec des prix ou profits négatifs ou nuls),
    puis applique un algorithme d'optimisation pour sélectionner
    les actions les plus rentables dans la limite du budget spécifié.
    """
    df = pd.read_csv(file_path)
    df = df[(df["price"] > 0) & (df["profit"] > 0)]
    names, costs, profits = prepare_data(df)  # On appelle une fonction (définie ailleurs)
    # nommée prepare_data, à laquelle on passe le DataFrame nettoyé.
    W = int(budget_euros*100)  # conversion en centimes d'euro
    # Exécution
    start = time.time()
    max_profit, selected = knapsack_bottom_up(W, costs, profits)
    # Résultats
    total_cost = sum(costs[i] for i in selected) / 100
    end = time.time()
    print(f"\nCoût total investi : {total_cost:.2f} €")
    print(f"Bénéfice maximal : {max_profit:.2f} €")
    print(f"\033[1m{len(selected)} Actions retenues :\033[0m")
    for i in selected:
        print(f"{names[i]} | Coût : {costs[i]/100:.2f} € | Profit : {profits[i]:.2f} €")
    print(f"\n Temps d'exécution : {end - start:.4f} secondes")
    # .4 signifie 4 chiffres après la virgule.
    # Execution depuis le menu


def main_menu():
    """Mise en page du menu déroulant"""
    print("\n ==== CHOIX POUR L OPTIMISATION DES ACTIONS=====")
    print("0 - Quitter le menu")
    print("1 - Optimisation sur  données de 20 actions ")
    print("2 - Optimisation à partir de dataset1.csv (1000 actions)")
    print("3 - Optimisation à partir de dataset2.csv (1000 actions)")
    choice = input(" Choisissez une option (0,1, 2 ou 3) : ")

    if choice == "0":
        sys.exit()
    if choice == "1":
        W = small_dataset["budget"]
        names = small_dataset["names"]
        costs = small_dataset["costs"]
        profits = small_dataset["profits"]
        start = time.time()
        max_profit, selected = knapsack_bottom_up(W, costs, profits)
        end = time.time()
        total_cost = sum(costs[i] for i in selected)
        print(f"\nCoût total investi : {total_cost} €")
        print(f"Bénéfice maximal : {max_profit:.2f} €")
        print(f"\033[1m{len(selected)} Actions retenues :\033[0m")
        for i in selected:
            print(f"{names[i]} | Coût : {costs[i]} € | Profit : {profits[i]:.2f} €")
        print(f"\n⏱️ Temps d'exécution : {end - start:.4f} secondes")
    elif choice == "2":
        run_csv_analysis("dataset1.csv", BUDGET_EUROS)
    elif choice == "3":
        run_csv_analysis("dataset2.csv", BUDGET_EUROS)

    else:
        print("❌ Option invalide. Veuillez relancer.")

# ========== Lancement ==========


if __name__ == "__main__":
    main_menu()

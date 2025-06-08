"""
    Recherche par force brute de la combinaison d'actions maximisant le profit
    sans dépasser un budget donné.
    La complexité temporelle de la méthode force brute O(2^N) 2^20=1048576

    Paramètres :
    - capacity  : Budget restant
    - actions (list) : liste de tuples (nom, coût, pourcentage de profit).
    - current_selection (list) : liste des actions déjà sélectionnées
    (utilisée pour la récursion interne).

    Retourne :
    - profit_total  : profit total de la meilleure combinaison.
    - meilleure_combinaison (list) : liste des actions (tuples) sélectionnées.
    """
import time

actions = [
    ("Action-1", 20, 0.05),
    ("Action-2", 30, 0.10),
    ("Action-3", 50, 0.15),
    ("Action-4", 70, 0.20),
    ("Action-5", 60, 0.17),
    ("Action-6", 80, 0.25),
    ("Action-7", 22, 0.07),
    ("Action-8", 26, 0.11),
    ("Action-9", 48, 0.13),
    ("Action-10", 34, 0.27),
    ("Action-11", 42, 0.17),
    ("Action-12", 110, 0.09),
    ("Action-13", 38, 0.23),
    ("Action-14", 14, 0.01),
    ("Action-15", 18, 0.03),
    ("Action-16", 8, 0.08),
    ("Action-17", 4, 0.12),
    ("Action-18", 10, 0.14),
    ("Action-19", 24, 0.21),
    ("Action-20", 114, 0.18),
]


def recursive_force_brute(capacity, actions, current_selection=None):
    """
    Methode brute force On travaille sur un sous-problème à chaque appel recursif.
    À chaque appel récursif : Elle se trouve face à un choix :

    Ne pas prendre l'objet courant :Elle appelle la même fonction
    sur le reste des objets (sans changer la capacité).

    Ou prendre l'objet courant (si son poids le permet)
    Elle appelle la même fonction sur le reste des objets,
    mais en réduisant la capacité du sac par le poids de l'objet courant,
    et en ajoutant l'objet courant à la sélection.
    """
    # curent_selection est la sélection actuelle d’actions déjà choisies
    if current_selection is None:
        current_selection = []
    if not actions:
        profit_total = sum(row[1] * row[2] for row in current_selection)
        return profit_total, current_selection

    # Cas où l'on n'inclut pas l'action actuelle
    #  On assigne ces deux valeurs aux variables profit_sans et combinaison_sans."
    profit_sans, combinaison_sans = recursive_force_brute(
        capacity, actions[1:], current_selection  # tout sauf la 1ere action
    )
    current_action = actions[0]
    # actions[0] correspond à l’action en cours de traitement subproblems.
    # Cas où l'on inclut l'action actuelle si elle respecte le budget
    if current_action[1] <= capacity:  # capacity est le budget restant
        profit_avec, combinaison_avec = recursive_force_brute(
            capacity - current_action[1],
            actions[1:],
            # Crée une nouvelle liste sans modifier la liste originale :recusivité
            current_selection + [current_action]
        )
        if profit_avec > profit_sans:
            return profit_avec, combinaison_avec

    return profit_sans, combinaison_sans


BUDGET = 500  # Budget maximal
start_time = time.time()

profit, meilleure_selection = recursive_force_brute(BUDGET, actions)

end_time = time.time()
execution_time = end_time - start_time

# --- Affichage des résultats ---
print("Meilleure combinaison d'actions :")
for nom, cout, pourcentage in meilleure_selection:
    benefice = cout * pourcentage
    print(f"{nom} | Coût : {cout:.2f} € | Bénéfice : {benefice:.2f} €")

total_cout = sum([a[1] for a in meilleure_selection])
print(f"\nCoût total : {total_cout:.2f} €")
print(f"Bénéfice total : {profit:.2f} €")
print(f"Temps d'exécution : {execution_time:.4f} secondes")

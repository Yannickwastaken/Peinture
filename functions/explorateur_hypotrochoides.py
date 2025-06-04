import numpy as np
from math import gcd
import matplotlib.pyplot as plt
from courbe import generate_hypotrochoid_points  # <-- adapte le nom si besoin

def rayon_max(R, r, d):
    return (R - r) + d

def rayon_min(R, r, d):
    return abs((R - r) - d)

def hypotrochoid_is_valid(R, r, d, rayon_max_limite=80, trou_min=15):
    if not float(R).is_integer() or not float(r).is_integer():
        return False
    if gcd(int(R), int(r)) != 1:
        return False
    r_max = rayon_max(R, r, d)
    r_min = rayon_min(R, r, d)
    return r_max <= rayon_max_limite and r_min >= trou_min

def explorer_parametres(r_values, R_values, d_values, show=False):
    solutions = []

    for r in r_values:
        for R in R_values:
            if gcd(int(R), int(r)) != 1:
                continue
            for d in d_values:
                if hypotrochoid_is_valid(R, r, d):
                    turns = 1  # suffisant car R et r entiers et pgcd = 1
                    x, y = generate_hypotrochoid_points(R, r, d, nb_points=1000, center_x=0, center_y=0, turns=turns)
                    solutions.append((R, r, d))

                    print(f"✅ R={R}, r={r}, d={d} → {r} boucles")
                    if show:
                        plt.figure()
                        plt.plot(x, y)
                        plt.title(f"Hypotrochoïde R={R}, r={r}, d={d}")
                        plt.axis('equal')
                        plt.show()
    print(f"\n🧮 {len(solutions)} combinaisons valides trouvées.")
    return solutions

# Exemple d'appel
if __name__ == "__main__":
    r_vals = range(3, 5)            # de 3 à 9 boucles
    R_vals = range(50, 80)           # rayons du cercle principal
    d_vals = range(10, 60, 10)        # longueurs de bras
    explorer_parametres(r_vals, R_vals, d_vals, show=True)

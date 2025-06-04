import numpy as np

def calculer_rayon_min_max(x, y, center_x, center_y):
    # Calcul des distances radiales au centre
    distances = np.sqrt((x - center_x)**2 + (y - center_y)**2)

    Rmin = np.min(distances)
    Rmax = np.max(distances)

    return Rmin, Rmax


def trouver_parametres_optimaux(R_max=80, trou_min=15):
    meilleurs = []
    for R in range(20, R_max + 1):
        for r in range(1, R):
            if np.gcd(R, r) != 1:
                continue  # la courbe ne sera pas fermée

            for d in range(1, r * 2):  # d ≤ 2r est une bonne limite
                rayon_max = (R - r) + d
                rayon_min = abs((R - r) - d)

                if rayon_max <= R_max and rayon_min >= trou_min:
                    nb_boucles = r
                    meilleurs.append((nb_boucles, R, r, d))

    # Trier par nombre de boucles décroissant
    meilleurs.sort(reverse=True)
    return meilleurs

def candidats_optimaux():
    #nulle
    candidats = trouver_parametres_optimaux()
    for boucles, R, r, d in candidats[:5]:
        print(f"✅ R={R}, r={r}, d={d} → {boucles} boucles")

def pause_pour_continuer(texte):
    while True:
        touche = input(f"⏸️{texte}  : ").strip().lower()
        if touche == 'o':
            print("▶️ Reprise de l'exécution...\n")
            break
        else:
            print("❌ Mauvaise touche. Appuyez sur 'o' pour continuer.")
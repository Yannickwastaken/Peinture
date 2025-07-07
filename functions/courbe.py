import numpy as np
import matplotlib.pyplot as plt
import os
import time

from matplotlib.path import Path
import numpy as np


def generer_points_couronneold(center_x, center_y, r_min, r_max, espacement=5.0, marge= 0):
    """
    Génère une grille régulière de points à l’intérieur d'une couronne (disque extérieur - disque intérieur).

    :param center_x: centre de la couronne (X)
    :param center_y: centre de la couronne (Y)
    :param r_min: rayon intérieur (zone vide au centre)
    :param r_max: rayon extérieur (limite de la peinture)
    :param espacement: distance entre deux points
    :return: tableau de points (x, y) à déposer
    """
    points = []

    # Boîte englobante carrée du disque
    xmin = center_x - r_max
    xmax = center_x + r_max
    ymin = center_y - r_max
    ymax = center_y + r_max

    for x in np.arange(xmin, xmax + espacement, espacement):
        for y in np.arange(ymin, ymax + espacement, espacement):
            distance = np.sqrt((x - center_x)**2 + (y - center_y)**2)
            if r_min + marge <= distance <= r_max - marge:
                points.append((x, y))

    return np.array(points)

def generer_points_couronne(center_x, center_y, r_min, r_max, espacement=5.0, marge=0,
                             mode="quadriage", courbe=None, n_cercles=10, tolerance=1.0):
    """
    Mode "cerclage" : extrait les points de la courbe qui sont proches de cercles concentriques
    Mode "quadriage" : quadrillage régulier dans une couronne
    """
    if mode == "quadriage":
        points = []
        n_steps = int(np.ceil(r_max / espacement))
        for i in range(-n_steps, n_steps + 1):
            x = center_x + i * espacement
            for j in range(-n_steps, n_steps + 1):
                y = center_y + j * espacement
                distance = np.sqrt((x - center_x)**2 + (y - center_y)**2)
                if r_min + marge <= distance <= r_max - marge:
                    points.append((x, y))
        return np.array(points)

    elif mode == "cerclage":
        if courbe is None:
            raise ValueError("Le mode 'cerclage' nécessite le paramètre 'courbe=(x, y)'.")

        x, y = courbe
        distances = np.sqrt((x - center_x)**2 + (y - center_y)**2)

        rayons = np.linspace(r_min + marge, r_max - marge, n_cercles)
        result = []

        for rayon in rayons:
            # Indices où la distance au centre ≈ rayon (± tolérance)
            indices = np.where(np.abs(distances - rayon) <= tolerance)[0]
            for idx in indices:
                result.append((x[idx], y[idx]))
        return np.array(result)

    else:
        raise ValueError(f"Mode inconnu : {mode}")


def generate_hypotrochoid_points(R, r, d, nb_points=10000, scale=1.0, center_x=0, center_y=0, turns=1):
    """
    Génère les points d'une hypotrochoïde en s'adaptant automatiquement :
    - Si R et r sont entiers, trace la courbe fermée sur la période exacte.
    - Sinon, utilise un nombre de tours spécifié.

    Paramètres :
    - R, r, d : paramètres géométriques
    - nb_points : nombre de points pour lisser la courbe
    - scale : facteur d’échelle
    - center_x, center_y : translation (décalage)
    - turns : nombre de tours à effectuer si R ou r sont flottants
    """
    is_integer_case = float(R).is_integer() and float(r).is_integer()

    if is_integer_case:
        R_int, r_int = int(R), int(r)
        gcd = np.gcd(R_int, r_int)
        t_max = 2 * np.pi * r_int / gcd * turns
    else:
        t_max = turns * 2 * np.pi    # nombre arbitraire de "tours"

    t = np.linspace(0, t_max, nb_points)

    x = (R - r) * np.cos(t) + d * np.cos((R - r) / r * t)
    y = (R - r) * np.sin(t) - d * np.sin((R - r) / r * t)

    x *= scale
    y *= scale

    return x + center_x, y + center_y


def plot_epicycloid_with_paint_points(x, y, R, r, d, paint_points, center_x, center_y, save_path=None, show=True):
    """
    Affiche 3 sous-graphes :
    1. Courbe hypotrochoïde
    2. Points de peinture dans la couronne
    3. Courbe + points de peinture combinés

    :param x, y: coordonnées de la courbe
    :param R, r, d: paramètres hypotrochoïde
    :param paint_points: tableau Nx2 des points de peinture
    :param center_x, center_y: centre
    :param save_path: chemin pour sauvegarder l'image (facultatif)
    :param show: booléen pour afficher le plot
    """
    fig, axs = plt.subplots(3, 1, figsize=(6, 18))

    # Limites communes à tous les subplots
    all_x = np.concatenate([x, paint_points[:, 0]])
    all_y = np.concatenate([y, paint_points[:, 1]])
    xmin, xmax = np.min(all_x), np.max(all_x)
    ymin, ymax = np.min(all_y), np.max(all_y)
    marge = max((xmax - xmin), (ymax - ymin)) * 0.05  # pour une petite marge visuelle

    # Fonction pour configurer un subplot
    def config_ax(ax, title):
        ax.set_xlim(xmin - marge, xmax + marge)
        ax.set_ylim(ymin - marge, ymax + marge)
        ax.set_aspect('equal')
        ax.grid(True)
        ax.set_title(title)

    # 1. Courbe
    axs[0].plot(x, y, color='blue')
    config_ax(axs[0], "Hypotrochoïde")

    # 2. Points seuls
    axs[1].scatter(paint_points[:, 0], paint_points[:, 1], color='red', s=10)
    config_ax(axs[1], "Points de peinture")

    # 3. Courbe + points
    axs[2].plot(x, y, color='blue', label='Courbe')
    axs[2].scatter(paint_points[:, 0], paint_points[:, 1], color='red', s=10, label='Peinture')
    config_ax(axs[2], "Courbe + Peinture")
    axs[2].legend()

    # Titre global
    fig.suptitle(f"Hypotrochoïde R={R}, r={r}, d={d}", fontsize=14)

    # Sauvegarde
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300)
        print(f"✅ Figure sauvegardée : {save_path}")

    if show:
        plt.show()
    else:
        plt.close()




def trouver_parametres_optimaux(rayon_max=80, rayon_min=15, R_range=range(10, 101), d_step=0.5):
    """
    Recherche les paramètres (R, r, d) d’une hypotrochoïde fermée :
    - Respectant un rayon maximal total ≤ rayon_max
    - Laissant un trou central ≥ rayon_min
    - Fermée (R et r doivent être entiers et premiers entre eux)
    - Maximisant le nombre de boucles (= r si pgcd(R, r) = 1)

    Paramètres :
    - rayon_max : rayon maximum (mm) de l’hypotrochoïde
    - rayon_min : trou vide au centre (mm) minimum
    - R_range : ensemble de valeurs testées pour R (entiers)
    - d_step : pas de variation de d (mm), pour affiner la recherche

    Retour :
    - Liste triée de tuples (nb_boucles, R, r, d)
    """
    meilleurs = []

    for R in R_range:
        for r in range(1, R):
            if np.gcd(R, r) != 1:
                continue  # courbe non fermée

            # Test de plusieurs longueurs de bras d
            d_min = rayon_min - (R - r)
            d_max = rayon_max - (R - r)

            if d_min > d_max:
                continue  # aucune valeur de d possible

            d_values = np.arange(d_min, d_max, d_step)

            for d in d_values:
                rayon_ext = (R - r) + d
                rayon_int = abs((R - r) - d)

                if rayon_ext <= rayon_max and rayon_int >= rayon_min:
                    nb_boucles = r  # comme R et r sont premiers entre eux
                    meilleurs.append((nb_boucles, R, r, round(d, 2)))

    # Tri : plus de boucles d’abord
    meilleurs.sort(reverse=True)

    return meilleurs



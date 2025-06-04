import numpy as np
import matplotlib.pyplot as plt
import os
from functions.calcul import calculer_rayon_min_max
from Sequence import  sequence_complete
import argparse

def main():
    sequence_complete()


def essai():
    from functions.courbe import\
        plot_epicycloid_with_paint_points, generate_hypotrochoid_points, generer_points_couronne
    from config import (
        port, baudrate,
        R, r, d, nb_points, scale, turns,
        espacement_peinture, marge_peinture,
        z_init,
        feedrate_xy, feedrate_z,
        main_gcode_path, dot_gcode_path, figure_path,
        send_main_gcode, send_dot_gcode
    )
    # === FICHIERS ===
    main_gcode_path = f"Gdire/main_epicycloide_Paint_R{R}_r{r}_d{d}.gcode"
    dot_gcode_path = f"Gdire/main_epicycloide_Dot_R{R}_r{r}_d{d}.gcode"
    figure_path = f"figures/epicycloide_R{R}_r{r}_d{d}.png"


    # === Étape 1 : Générer les points de la courbe (hypotrochoïde) ===
    x, y = generate_hypotrochoid_points(
        R, r, d,
        nb_points=nb_points,
        scale=scale,
        center_x=0,
        center_y=0,
        turns=turns
    )

    # === Étape 2 : Calculer les rayons minimum et maximum de la couronne ===
    Rmin, Rmax = calculer_rayon_min_max(x, y, center_x=0, center_y=0)
    if Rmax > 100:
        print(f"❌ Erreur : Rayon max {Rmax:.2f} mm dépasse la limite autorisée.")
    else:print(f"✅ Rayon maximum valide : {Rmax:.2f} mm")

    # === Étape 3 : Générer les points de peinture initiaux (avant recentrage) ===
    paint_points = generer_points_couronne(
        center_x=0, center_y=0,
        r_min=Rmin, r_max=Rmax,
        espacement=espacement_peinture,
        marge=marge_peinture
    )
    # === Étape 4 : Visualisation initiale de la courbe et des points de peinture ===
    plot_epicycloid_with_paint_points(
        x, y, R, r, d, paint_points,
        center_x=0, center_y=0,
        save_path=figure_path,
        show=True
    )

if __name__ == "__main__":
    #essai()
    main()
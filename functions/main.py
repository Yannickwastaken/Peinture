import numpy as np
import matplotlib.pyplot as plt
import os
from Sequence import  sequence_complete
from calcul import calculer_rayon_min_max
from courbe import generate_hypotrochoid_points, plot_epicycloid_with_paint_points, trouver_parametres_optimaux, generer_points_couronne
from PrinterCode import generate_gcode, save_gcode, send_gcode_to_printer, generate_paint_points_gcode

# Paramètres
R = 68      # R/r = 5 -> 5 rota
r = 27
d = 50
nb_points = 10000
scale = 0.8
center_x, center_y = 112, 131.3
turns = 1
Z_init = 2  # Hauteur à laquel le sylo/pinceau doit etre

feedrate = 1500

# Bool
GenerateGcode = True  # ← active ou désactive la generation du gcode
Find_perfect_loop = False  # ← active la recherche de la meilleure valeur finie en fonction des params fixés
send_gcode = False  # ← active ou désactive l’envoi

# Fichiers de sortie
figure_path = f"figures/epicycloide_R{R}_r{r}_d{d}_x{turns}.png"
gcode_path = f"Gdire/epicycloide_R{R}_r{r}_d{d}_x{turns}.gcode"

port = 'COM8'


# Fin Paramètres


def main():
    # Liste triée de tuples (nb_boucles, R, r, d)
    if Find_perfect_loop: Best_loop = trouver_parametres_optimaux(rayon_max=80, rayon_min=15, R_range=range(10, 101),
                                                                  d_step=0.5)
    if Find_perfect_loop: print(Best_loop)
    if Find_perfect_loop: print(len(Best_loop))

    # Générer la courbe
    x, y = generate_hypotrochoid_points(R, r, d, nb_points, scale, center_x, center_y, turns)

    #calcul du rayon max et nim
    Rmin, Rmax = calculer_rayon_min_max(x, y, center_x, center_y)


    if (Rmax) > 100:
        print(f"❌ Erreur de taille attention : R={Rmax}")
    else: print(f"✅ taille  :R= {Rmax} ")

    # Générer le G-code
    if GenerateGcode: gcode_lines = generate_gcode(x, y, feedrate, center_x, center_y, Z_init)

    paint_points = generer_points_couronne(center_x, center_y, Rmin, Rmax, espacement=7.0, marge= 2)

    plot_epicycloid_with_paint_points(
        x, y,
        R, r, d,
        paint_points,
        center_x, center_y,
        save_path=f"figures/epicycloide_R{R}_r{r}_d{d}_x{turns}.png",
        show=True
    )



    # Sauvegarde du G-code
    if GenerateGcode: save_gcode(gcode_lines, gcode_path)

    # Send Code serial
    if GenerateGcode and send_gcode:
        send_gcode_to_printer(gcode_path, port, baudrate=115200)

    gcode_points = generate_paint_points_gcode(paint_points)
    save_gcode(gcode_points, f"Gdire/epicycloide_R{R}_r{r}_d{d}_x{turns}paint.gcode")

if __name__ == "__main__":
    #main()
    sequence_complete()
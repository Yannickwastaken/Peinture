import numpy as np
import os
from courbe import generate_hypotrochoid_points, plot_epicycloid

# -------------------------------
# Paramètres globaux
# -------------------------------
nb_points = 2000
scale = 1.0
center_x = 120
center_y = 120
output_dir = "plots"
output_Gdir = "Gdir"

# Crée le dossier s'il n'existe pas
os.makedirs(output_dir, exist_ok=True)
os.makedirs(output_Gdir, exist_ok=True)


# -------------------------------
# Boucles R, r, d
# -------------------------------
for R in range(5, 50, 1):
    for r in range(5, 50, 1):
        for d in range(5, 40, 1):
            try:
                # Éviter les cas où la génération échoue
                x, y = generate_hypotrochoid_points(R, r, d, nb_points, scale, center_x, center_y)

                # Définir le nom du fichier
                filename = f"R{R}_r{r}_d{d}.png"
                save_path = os.path.join(output_dir, filename)

                # Tracer et sauvegarder la courbe sans l'afficher
                plot_epicycloid(x, y, R, r, d, center_x, center_y, save_path, show=False)
                print(f"✅ Enregistré : {save_path}")

            except Exception as e:
                print(f"⚠️ Erreur avec R={R}, r={r}, d={d} : {e}")

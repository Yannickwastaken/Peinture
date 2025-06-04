# config.py

# Connexion imprimante
port = "COM8"            # Remplace par le port réel (ex : COM3, /dev/ttyUSB0)
baudrate = 115200        # Vitesse de communication série

# Paramètres géométriques pour la courbe hypotrochoïde
R = 68                   # Grand rayon
r = 12                   # Petit rayon
d = 50                   # Distance du point traceur au centre du petit cercle
nb_points = 10000         # Nombre de points de la courbe
scale = 0.8*0.8             # Échelle de la courbe
turns = 1                # Nombre de tours

# Paramètres pour les p oints de peinture
espacement_peinture = 25     # Espacement entre les points
marge_peinture = 3        # Marge intérieure

# Paramètres pour le mouvement en Z
z_init = 5.0                  # Hauteur de proche du tableau

# Vitesses d'impression
feedrate_xy = 1200            # Vitesse XY (mm/min)
feedrate_z = 300              # Vitesse Z (mm/min)

# Chemins de fichiers
main_gcode_path = "courbe.gcode"
dot_gcode_path = "dot.gcode"
figure_path = "figure.png"

# Contrôle de l'envoi
send_main_gcode = False
send_dot_gcode = False




"""
68 12 72 0.8*0.8
R = 68   r = 12      d = 50   

"""
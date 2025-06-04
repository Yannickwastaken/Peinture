import os
import sys
import IPython

# Ajouter le chemin du projet à sys.path
project_dir = os.path.dirname(os.path.abspath(__file__))
if project_dir not in sys.path:
    sys.path.append(project_dir)

# Importer les modules internes
from functions import courbe, PrinterCode, calcul
import config  # <-- ici tu mets tes variables globales

# Préparer l'environnement IPython
banner = "🧠 IPython prêt avec : courbes, gcode, utils, config"

# Injecter tout dans l'environnement utilisateur
IPython.start_ipython(argv=[], user_ns={
    'courbes': courbe,
    'gcode': PrinterCode,
    'utils': calcul,
    'config': config,
}, banner1=banner)

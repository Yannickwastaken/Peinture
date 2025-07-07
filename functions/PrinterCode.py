import serial
import time
import re
import serial
import time
import numpy as np


def send_gcode_to_printerold(gcode_path, port='/dev/ttyUSB0', baudrate=115200, delay=0.1):
    """
    Envoie un fichier G-code ligne par ligne à une imprimante 3D via port série, avec gestion des réponses.
    """
    try:
        with serial.Serial(port, baudrate, timeout=5) as ser:
            print(f"📡 Connexion établie sur {port} à {baudrate} bauds.")
            time.sleep(2)  # Laisser le temps à l'imprimante de redémarrer si besoin
            ser.reset_input_buffer()  # Nettoyer le buffer d'entrée

            with open(gcode_path, 'r') as file:
                for line in file:
                    clean_line = line.strip()
                    if clean_line:
                        ser.write((clean_line + '\n').encode('utf-8'))
                        print(f"→ {clean_line}")

                        # Attendre une réponse "ok" du firmware
                        while True:
                            response = ser.readline().decode('utf-8').strip()
                            if response:
                                print(f"← {response}")
                                if 'ok' in response.lower():
                                    break
                            else:
                                print("⏳ En attente de réponse...")
                        time.sleep(delay)

            print("✅ G-code envoyé avec succès.")
    except serial.SerialException as e:
        print(f"❌ Erreur de connexion série : {e}")
    except FileNotFoundError:
        print(f"❌ Fichier introuvable : {gcode_path}")


def send_gcode_to_printer(gcode_path, port='/dev/ttyUSB0', baudrate=115200, delay=0.05):
    try:
        with serial.Serial(port, baudrate, timeout=5) as ser:
            print(f"📡 Connexion établie sur {port} à {baudrate} bauds.")
            time.sleep(2)  # Temps pour que l'imprimante démarre
            ser.reset_input_buffer()

            with open(gcode_path, 'r') as file:
                for line in file:
                    clean_line = line.strip()
                    if clean_line:
                        ser.write((clean_line + '\n').encode('utf-8'))
                        print(f"→ {clean_line}")

                        # Attente de l'accusé de réception
                        while True:
                            response = ser.readline().decode('utf-8').strip()
                            if response:
                                print(f"← {response}")
                                if 'ok' in response.lower():
                                    break
                            else:
                                print("⏳ Attente de réponse...")
                        # Optionnel : attendre un peu entre les commandes simples
                        if not clean_line.startswith('G1'):
                            time.sleep(delay)

                        # Si c'est un mouvement, attendre la fin avec M400
                        if clean_line.startswith('G1'):
                            ser.write(('M400\n').encode('utf-8'))
                            while True:
                                response = ser.readline().decode('utf-8').strip()
                                if response:
                                    print(f"← {response}")
                                    if 'ok' in response.lower():
                                        break

            print("✅ G-code envoyé avec synchronisation.")
    except serial.SerialException as e:
        print(f"❌ Erreur de connexion série : {e}")
    except FileNotFoundError:
        print(f"❌ Fichier introuvable : {gcode_path}")
import serial
import time

def send_gcode_with_sync(gcode_path, port='/dev/ttyUSB0', baudrate=115200, delay=0.05):
    try:
        with serial.Serial(port, baudrate, timeout=5) as ser:
            print(f"📡 Connexion établie sur {port} à {baudrate} bauds.")
            time.sleep(2)
            ser.reset_input_buffer()

            with open(gcode_path, 'r') as file:
                for line in file:
                    clean_line = line.strip()
                    if not clean_line or clean_line.startswith(';'):
                        continue

                    # Envoie de la ligne de G-code
                    ser.write((clean_line + '\n').encode('utf-8'))
                    print(f"→ {clean_line}")

                    # Attente de la réponse "ok"
                    while True:
                        response = ser.readline().decode('utf-8').strip()
                        if response:
                            print(f"← {response}")
                            if 'ok' in response.lower():
                                break

                    # Si c'est un mouvement, on ajoute un M400
                    if clean_line.startswith(('G0', 'G1')):
                        ser.write(('M400\n').encode('utf-8'))
                        print(f"→ M400")
                        while True:
                            response = ser.readline().decode('utf-8').strip()
                            if response:
                                print(f"← {response}")
                                if 'ok' in response.lower():
                                    break
                    time.sleep(delay)

            print("✅ G-code envoyé avec synchronisation complète.")
    except serial.SerialException as e:
        print(f"❌ Erreur de connexion série : {e}")
    except FileNotFoundError:
        print(f"❌ Fichier introuvable : {gcode_path}")


def send_gcodeline_to_printer(gcode_txt, port='/dev/ttyUSB0', baudrate=115200, delay=0.1):
    """
    Envoie un fichier G-code ligne par ligne à une imprimante ou CNC via port série.

    Paramètres :
    - gcode_txt : txt G-code
    - port : port série (ex: 'COM3' sur Windows, '/dev/ttyUSB0' sur Linux)
    - baudrate : vitesse de communication (souvent 115200 ou 250000)
    - delay : délai entre chaque ligne envoyée (en secondes)
    """
    try:
        with serial.Serial(port, baudrate, timeout=1) as ser:
            print(f"📡 Connexion établie sur {port} à {baudrate} bauds.")
            ser.write((gcode_txt + '\n').encode('utf-8'))
            print("✅ G-code envoyé avec succès.")
    except serial.SerialException as e:
        print(f"❌ Erreur de connexion série : {e}")




def generate_gcode(x, y, feedrate = 1500, center_x =0 , center_y=0, Z_init= 20):
    gcode = []
    gcode.append("G90")  # mode absolu
    #gcode.append("G28")  # homing
    gcode.append(f"G1 Z{Z_init+20}")  # lever pinceau
    gcode.append("G21")  # unités mm
    gcode.append(f"G1 X{center_x} Y{center_y} F{feedrate}")  # centre
    gcode.append(f"G1 X{x[0]:.2f} Y{y[0]:.2f} F{feedrate}")  # point de départ
    gcode.append(f"G1 Z{Z_init-5} F300")  # baisser le pinceau

    for xi, yi in zip(x, y):
        gcode.append(f"G1 X{xi:.2f} Y{yi:.2f} F{feedrate}")

    gcode.append(f"G1 F1500 Z{Z_init + 20} F300")  # relever pinceau
    gcode.append("G1 F1500 X0 Y0")     # retour origine
    return gcode

def generate_paint_points_gcode(paint_points, z_init, feedrate_xy=1500, feedrate_z=1500):
    """
    Génère un G-code optimisé pour déposer un point de peinture.

    :param paint_points: tableau Nx2 des points (X, Y)
    :param z_init: hauteur de base (proche toile)
    :return: liste G-code optimisé
    """
    gcode = []
    gcode.append("G90")  # mode absolu
    gcode.append("G21")  # mm
    gcode.append("G1 Z{:.2f} F{}".format(z_init + 10, feedrate_z))  # lever pinceau

    # Optimiser les déplacements
    sorted_points = optimiser_ordre_points(paint_points)

    for x, y in sorted_points:
        gcode.append(f"G1 X{x:.2f} Y{y:.2f} F{feedrate_xy}")
        gcode.append("G1 F500 Z{:.2f} F{}".format(z_init - 2, feedrate_z))  # toucher
        gcode.append("G1 F1500 Z{:.2f} F{}".format(z_init + 5, feedrate_z))  # relever

    return gcode

def optimiser_ordre_points(paint_points):
    """
    Réorganise les points pour minimiser les déplacements (nearest neighbor TSP).

    :param paint_points: tableau Nx2 des points (X, Y)
    :return: tableau Nx2 trié selon l’ordre optimisé
    """
    if len(paint_points) == 0:
        return paint_points

    points = paint_points.copy()
    visited = []
    current_index = 0
    remaining = list(range(1, len(points)))
    visited.append(current_index)

    while remaining:
        current_point = points[current_index]
        dists = np.linalg.norm(points[remaining] - current_point, axis=1)
        next_idx_in_remaining = np.argmin(dists)
        next_index = remaining.pop(next_idx_in_remaining)
        visited.append(next_index)
        current_index = next_index

    return points[visited]

def save_gcode(gcode_lines, output_path):
    with open(output_path, "w") as f:
        for line in gcode_lines:
            f.write(line + "\n")
    print(f"✅ G-code enregistré dans : {output_path}")

def get_printer_position(port="/dev/ttyUSB0", baudrate=115200, timeout=2):
    """
    Se connecte à l'imprimante 3D via port série et récupère les coordonnées actuelles (X, Y, Z) avec la commande M114.

    :param port: port série (ex: 'COM3' sous Windows, '/dev/ttyUSB0' sous Linux)
    :param baudrate: vitesse de communication (par défaut 115200 pour la plupart des firmwares)
    :param timeout: délai d'attente en secondes
    :return: dictionnaire {'X': float, 'Y': float, 'Z': float} ou None en cas d'erreur
    """
    try:
        with serial.Serial(port, baudrate, timeout=timeout) as ser:
            # Attendre que l'imprimante soit prête (délai initial)
            time.sleep(2)
            ser.reset_input_buffer()

            # Envoyer la commande
            ser.write(b"M114\n")
            time.sleep(0.5)  # Laisser le temps de répondre

            # Lire la réponse
            response = ser.read(ser.in_waiting).decode('utf-8', errors='ignore')

            # Exemple attendu : "X:120.00 Y:120.00 Z:0.00 E:0.00 Count X: 9600 Y: 9600 Z: 0"
            match = re.search(r"X:([-\d.]+)\s+Y:([-\d.]+)\s+Z:([-\d.]+)", response)
            if match:
                x, y, z = map(float, match.groups())
                return {'X': x, 'Y': y, 'Z': z}
            else:
                print("❌ Impossible de lire la position dans la réponse :", response)
                return None

    except serial.SerialException as e:
        print(f"❌ Erreur de connexion série : {e}")
        return None

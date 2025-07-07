import numpy as np
from functions.calcul import calculer_rayon_min_max, pause_pour_continuer

from functions.courbe import (
    generate_hypotrochoid_points,
    generer_points_couronne,
    plot_epicycloid_with_paint_points,
    trouver_parametres_optimaux
)
from functions.PrinterCode import (
    generate_gcode,
    generate_paint_points_gcode,
    save_gcode,
    send_gcode_to_printer,
    get_printer_position,
    send_gcodeline_to_printer,
    send_gcode_with_sync
)

from config import (
    port, baudrate,
    R, r, d, nb_points, scale, turns,
    espacement_peinture, marge_peinture,mode,n_cercles, tolerance,
    z_init,
    feedrate_xy, feedrate_z,
    main_gcode_path, dot_gcode_path, figure_path,
    send_main_gcode, send_dot_gcode
)
# === FICHIERS ===
main_gcode_path = f"Gdire/main_epicycloide_Paint_R{R}_r{r}_d{d}.gcode"
dot_gcode_path = f"Gdire/main_epicycloide_Dot_R{R}_r{r}_d{d}.gcode"
figure_path = f"figures/epicycloide_R{R}_r{r}_d{d}.png"


def sequence_complete():
    #TODO Renommer x,y en courbe pour simplifier des params des fontions

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

    # # === Étape 3 : Générer les points de peinture initiaux (avant recentrage) ===
    paint_points = generer_points_couronne(center_x=0,
                                           center_y=0,
                                           r_min=Rmin+10,
                                           r_max=Rmax-5,
                                           espacement=espacement_peinture,
                                           marge=marge_peinture,
                                           mode="cerclage",   #mode = cerclage ou quadriage
                                           courbe=(0.9*x,0.9*y),
                                           n_cercles=4,
                                           tolerance=0.1)

    # === Étape 4 : Visualisation initiale de la courbe et des points de peinture ===
    plot_epicycloid_with_paint_points(
        x, y, R, r, d, paint_points,
        center_x=0, center_y=0,
        save_path=figure_path,
        show=True
    )
    send_gcodeline_to_printer("G28", port= port, baudrate=115200, delay=0.1)

    # === Étape 5 : Instructions manuelles à l'utilisateur ===
    pause_pour_continuer("➡️ Si cela convient, appuyez sur 'o'. Prochaine étape : mettre le feutre au centre de la toile.")

    #remetre au centre
    cmd=f"G1 F1500 Z40"
    send_gcodeline_to_printer(cmd, port= port, baudrate=115200, delay=0.1)
    cmd=f"G1 F1500 X110 Z30 Y130"
    send_gcodeline_to_printer(cmd, port= port, baudrate=115200, delay=0.1)


    pause_pour_continuer("➡️ Si le stylo est bien positionné (au centre, proche de la toile), appuyez sur 'o' pour continuer au dessin.")

    # === Étape 6 : Lecture de la position actuelle de l’imprimante ===
    position = get_printer_position(port, baudrate)
    if not position:
        print("❌ Impossible de lire la position de l'imprimante.")
        position['X'], position['Y'], position['Z'] = 0, 0, 0
        input("X,Y,Z", position['X'], position['Y'], position['Z'])

    print(f"📍 Position actuelle : X={position['X']}, Y={position['Y']}, Z={position['Z']}")
    pause_pour_continuer(f"Confirmez que le feutre est très proche de la toile. Appuyez sur 'o' pour générer le G-code des points.")

    #TODO
    """print la hauteur safe + marge, et la hauteur de dessin pour le feutre."""

    #mettre une zone de "large" avant le homing
    cmd=f"G1 F500 Z{position['Z'] + 20}"
    send_gcodeline_to_printer(cmd, port= port, baudrate=115200, delay=0.1)

    # === Étape 7 : Recentrage de la courbe selon la position réelle de l’imprimante ===
    center_x, center_y = position['X'], position['Y']
    x += center_x
    y += center_y

    # === Étape 8 : Recalcul des points de peinture avec la nouvelle origine ===

    paint_points = generer_points_couronne(center_x=center_x,
                                           center_y=center_y,
                                           r_min=Rmin+10,
                                           r_max=Rmax,
                                           espacement=espacement_peinture,
                                           marge=marge_peinture,
                                           mode="cerclage",   #mode = cerclage ou quadriage
                                           courbe=(x,y),
                                           n_cercles=4,
                                           tolerance=0.1)



    # === Étape 9 : Génération du G-code pour les points de peinture ===
    gcode_points = generate_paint_points_gcode(
        paint_points,
        z_init=position['Z'],
        feedrate_xy= feedrate_xy,
        feedrate_z=feedrate_z
    )
    save_gcode(gcode_points, dot_gcode_path)

    # === Étape 10 : Visualisation mise à jour avec recentrage ===
    plot_epicycloid_with_paint_points(
        x, y, R, r, d, paint_points,
        center_x=center_x, center_y=center_y,
        save_path=figure_path,
        show=True
    )

    # pause ou envoi du G-code à l’imprimante
    if send_main_gcode:
        print('envoie Gcode')
        #send_gcode_to_printer(main_gcode_path, port, baudrate)
        send_gcode_with_sync(main_gcode_path, port, baudrate)
    else:
        pause_pour_continuer("✅ G-code des points sauvegardé. Lancez-le sur l'imprimante.")

    pause_pour_continuer("🖊️ Une fois le G-code terminé, appuyez sur 'o'.")

    #remetre au centre
    cmd=f"G1 F500 X{position['X']} Y{position['Y']}"
    send_gcodeline_to_printer(cmd, port= port, baudrate=115200, delay=0.1)

    pause_pour_continuer("🖌️ Positionnez le pinceau au centre et appuyez sur 'o'.")

    # === Étape 11 : Lecture de la position actuelle avec pinceau ===
    position = get_printer_position(port, baudrate)
    if not position:
        print("❌ Impossible de lire la position de l'imprimante.")
        return

    print(f"📍 Nouvelle position : X={position['X']}, Y={position['Y']}, Z={position['Z']}")

    # === Étape 12 : Génération du G-code de la courbe (dessin principal) ===
    gcode_curve = generate_gcode(
        x, y,
        feedrate_xy,
        center_x=position['X'],
        center_y=position['Y'],
        Z_init=position['Z']
    )
    save_gcode(gcode_curve, main_gcode_path)

    if send_main_gcode:
        send_gcode_to_printer(main_gcode_path, port, baudrate)

    print("✅ G-code principal généré et prêt à l'envoi.")


    #mettre une zone de "large" avant le homing
    cmd=f"G1 F500 Z{position['Z'] + 20}"
    send_gcodeline_to_printer(cmd, port= port, baudrate=115200, delay=0.1)





if __name__ == "__main__":
    sequence_complete()

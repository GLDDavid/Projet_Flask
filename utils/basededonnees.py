import os
import sqlite3


def f_creerbasededonnees ():
    if os.path.isfile('base_chauffeurs.db'):
        print("la base existe déjà.")
    else :
        connexion = sqlite3.connect("base_chauffeurs.db")
        curseur = connexion.cursor()
        curseur.execute("""
                CREATE TABLE kms_chauffeurs (
                    prenom_bdd VARCHAR(100),
                    nom_bdd VARCHAR(100),
                    sexe_bdd CHARACTER(20),
                    camion_bdd VARCHAR(50),
                    kms_bdd INT,
                    commentaire_bdd TEXT
                    )
                """)
        connexion.commit()
        connexion.close()
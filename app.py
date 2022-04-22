# pip install -r requirements.txt
from dotenv import load_dotenv

from flask import Flask, render_template, request, flash

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, NumberRange

import sqlite3
from utils.basededonnees import f_creerbasededonnees

load_dotenv()

app = Flask(__name__)

f_creerbasededonnees()

# Configuration de l'application

app. config['CACHE_TYPE'] = 'null'
app.config['SECRET_KEY'] = "motdepasse"

# # Classe du formulaire
class c_formulaire(FlaskForm):
    cf_prenom = StringField("Prénom", validators = [DataRequired()])
    cf_nom    = StringField("Nom", validators = [DataRequired()])
    cf_sexe   = SelectField("Sexe", validators = [DataRequired()], choices=[('Homme'), ('Femme')])
    cf_camion = SelectField("Type de Camions", validators = [DataRequired()], choices=[('camion citerne'), ('camion benne'), ('camion frigorifique'), ('camion fourgon')])
    cf_kms    = IntegerField("Nombre de kilomètres", validators = [DataRequired(), NumberRange(min=0)])
    cf_commentaires = TextAreaField("Commentaires")

    cf_envoyer = SubmitField("Envoyer")

@app.route('/')
def f_index() :
    f_titre = "Accueil"
    connexion = sqlite3.connect("base_chauffeurs.db")
    curseur = connexion.cursor()

    type_camion = curseur.execute("SELECT DISTINCT camion_bdd FROM kms_chauffeurs")
    camions = []
    for camion in type_camion:
        for cam in camion:
            camions.append(cam)
    print(camions)

    sum_kms = curseur.execute("SELECT SUM(kms_bdd) FROM kms_chauffeurs GROUP BY camion_bdd")
    kms_camion = []
    for km in sum_kms:
        for k in km :
            kms_camion.append(k)

    chauffeurs = curseur.execute("SELECT sexe_bdd, prenom_bdd, nom_bdd  FROM kms_chauffeurs")
    liste_chauffeurs = []
    for ligne in chauffeurs:
        liste_chauffeurs.append(ligne)

    nb_kms = curseur.execute("SELECT SUM(kms_bdd) FROM kms_chauffeurs")
    kms_total = []
    for nb_km in nb_kms:
        kms_total.append(nb_km)
    kms_total = kms_total[0][0]

    nb_chauffeurs = curseur.execute("SELECT COUNT(*) FROM kms_chauffeurs")
    liste_nb_chauffeurs = []
    for nombre in nb_chauffeurs:
        liste_nb_chauffeurs.append(nombre)
    liste_nb_chauffeurs = liste_nb_chauffeurs[0][0]

    return render_template("index.html",
                            t_titre = f_titre,
                            t_camions = camions,
                            t_kms_camion = kms_camion,
                            t_liste_chauffeurs = liste_chauffeurs,
                            t_kms_total = kms_total,
                            t_liste_nb_chauffeurs = liste_nb_chauffeurs
                            )


@app.route("/formulaire", methods=["GET", "POST"])
def f_formulaire():
    f_formulaire = c_formulaire()

    if f_formulaire.validate_on_submit():
        f_nom = f_formulaire.cf_nom.data
        f_prenom = f_formulaire.cf_prenom.data
        f_sexe = f_formulaire.cf_sexe.data
        f_camion = f_formulaire.cf_camion.data
        f_kms = f_formulaire.cf_kms.data
        f_commentaires = f_formulaire.cf_commentaires.data
        # v_formulaire.wtf_nom.data = ""
        #flash("Les données ont bien été saisies.")
        return render_template("resultat.html",
                                    t_nom = f_nom,
                                    t_prenom = f_prenom,
                                    t_sexe = f_sexe,
                                    t_camion = f_camion,
                                    t_kms = f_kms,
                                    t_commentaires = f_commentaires
                            )
    return render_template("formulaire.html" ,
                        titre = "Formulaire d'inscription",
                        t_formulaire = f_formulaire)


@app.route('/resultat',methods = ['POST', 'GET'])
def ajouter_chauffeurs():
    if request.method == 'POST':
        try:
            f_nom = request.form['cf_nom']
            f_prenom = request.form['cf_prenom']
            f_sexe = request.form['cf_sexe']
            f_camion = request.form['cf_camion']
            f_kms = request.form['cf_kms']
            f_commentaires = request.form['cf_commentaires']

            connexion = sqlite3.connect("base_chauffeurs.db")
            curseur = connexion.cursor()
            curseur.executemany("INSERT INTO kms_chauffeurs VALUES (?,?,?,?,?,?)", [(f_prenom, f_nom, f_sexe, f_camion, f_kms, f_commentaires)])
            connexion.commit()
            f_message = "Enregistrement inscrit dans la base."
        except:
            connexion.rollback()
            f_message = "Un problème est apparu pendant l'enregistrement."
        finally:
            connexion.close()
            return render_template("resultat.html",t_message = f_message, t_nom = f_nom, t_prenom = f_prenom )




@app.route('/liste_chauffeurs', methods=["GET", "POST"])
def f_listechauffeurs() :
    f_titre = "Liste chauffeurs"
    connexion = sqlite3.connect("base_chauffeurs.db")
    requete = "SELECT * FROM kms_chauffeurs"
    result = connexion.execute(requete)
    f_info = []
    for ligne in result:
        f_info.append(ligne)
    return render_template("listechauffeurs.html", t_info = f_info , t_titre = f_titre)
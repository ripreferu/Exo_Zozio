import mysql_test as api
toto = api.user("Toto", "Tata", "toto@tata", "mot_de_passe")
toto.save()  # inscrit l'utilisateur dans la base de données
# Remarque il est nécessaire d'inscire de sauvegarder un utilisateur
# avant de l'authentifier car le processus d'authentification
# cherche l'utilisateur dans la base de données
api.auth("toto@tata", "pas_de_mots_de_passe")  # echec car mauvais mot de passe
api.auth("toto@tata", "mot_de_passe")  # réussite
toto.password
del toto  # supprime l'objet python
annuaire = api.load_users()
# récupère les utilisateur de la base sql sous la forme d'une liste
toto = annuaire[0]
# en supposant que l'annuaire ne contiennent qu'un seul utilisateur

# une fois que le script est terminé il est souhaitable de fermer la connexion
# avec la base de données

api.close_conn()

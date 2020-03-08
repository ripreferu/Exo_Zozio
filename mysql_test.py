# coding: utf-8
"""
Ce module est un prototype de gestion de base de données d'utilisateurs
"""
__author__ = "pierre FUR"
__license__ = "GPLv3"
__status__ = "prototype"
import mysql.connector
import getpass
import hashlib
conn = mysql.connector.connect(host="localhost", user=getpass.getuser(),
                               password=None, database="test")
# CETTE LIGNE EST A MODIFIER VIS A VIS DE VOTRE PROPRE CONFIGURATION
""" dans ma configuration la communication entre le serveur sql et le client
 n'est pas sécurisé elle apparaît donc en clair dans la boucle locale"""


########################################################################
# l'utilisation de certificat SSL est possible mais ne fait pas partie #
# de la configuration par défaut de MariaDB                            #
########################################################################

cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
id int(5) NOT NULL AUTO_INCREMENT,
name varchar(50) DEFAULT NULL,
surname varchar(50) DEFAULT NULL,
enc_pass BLOB DEFAULT NULL,
email varchar(50) DEFAULT NULL,
PRIMARY KEY(id));
""")
"""
Ceci permet de créer la table users si celle si n'existe pas
"""


class user():
    """
    La classe user définit des utilisateurs par leur noms, leurs prénoms
    et leurs emails
    le mot de passe peut-être définit ou non
    Si celui-ci n'est pas définit il sera demandé par le programme


    ############################################
    # AVERTISSEMENT!:                          #
    # ---------------                          #
    #                                          #
    # SEUL LE MOT DE PASSE EST ENCRYPTÉ!       #
    # LES AUTRES DONNEES APPARAISSENT EN CLAIR #
    # DANS LA BASE DE DONNÉES ET DANS LA RAM.  #
    ############################################

    Remarque importante:
    --------------------
    Le programme utilise le sha512 pour l'encryption
    ce cryptage est assez faible puisque 2 mot de passe identique
    renvoie le même hash
    Pour un déployement plus sûr il est conseillé d'utiliser Argon2
    en employant des paramètres adaptés.
    https://github.com/p-h-c/phc-winner-argon2

    Le choix du mot de passe est laissé libre
    (pas de longueur minimale, de limitation au niveau du jeux de caractères,
    chiffre lettre etc).
    L'api ne demande par ailleurs aucune confirmation du mot de passe

    Ressource pour créer un mot de passe fort selon la CNIL
    https://www.cnil.fr/fr/generer-un-mot-de-passe-solide
    """
    def __init__(self, nom, prenom, email, mot_de_passe=None,
                 ispassword_hashed=False):
        """ Constructeur:
        l'option ispassword_hashed n'est utile que pour recupérer les
        utilisateurs de la base de données
        """
        assert type(nom) == str
        assert type(prenom) == str
        assert type(email) == str and "@" in email
        self._nom = nom
        self._prenom = prenom
        self._email = email
        if ispassword_hashed and mot_de_passe is not None:
            self.__mot_de_passe = mot_de_passe
        elif (mot_de_passe is not None and type(mot_de_passe) == str
                and not ispassword_hashed):
            mot_de_passe = mot_de_passe.encode("utf-8")
            self.__mot_de_passe = hashlib.new("sha512")
            self.__mot_de_passe.update(mot_de_passe)
        else:
            self.__mot_de_passe = hashlib.new("sha512")
            test = getpass.getpass("Veuillez entrer le mot_de_passe: ")
            test = test.encode('utf-8')
            self.__mot_de_passe.update(test)

    def get_nom(self):
        return self._nom

    def set_nom(self, nouv_nom):
        assert nouv_nom != self._nom, "Le nouveau nom est identique à l'ancien"
        assert type(nouv_nom) == str, "Erreur le nouveau nom n'est pas une" \
            "chaine de caractères"
        self._nom = nouv_nom
    nom = property(get_nom, set_nom, None, "nom de l'utilisateur")

    def get_prenom(self):
        return self._prenom

    def set_prenom(self, nouv_prenom):
        assert nouv_prenom != self._prenom, "Le nouveau prenom est identique" \
            "à l'ancien"
        assert type(nouv_prenom) == str, "Erreur le nouveau prenom n'est pas" \
            "une chaine de caractères"
        self._prenom = nouv_prenom
    prenom = property(get_prenom, set_prenom, None, "prenom de l'utilisateur")

    def get_email(self):
        """Retourne l'email """
        return self._email

    def set_email(self, nouv_email):
        assert type(nouv_email) == str and "@" in nouv_email, \
            "E-Mail invalide"
        self._email = nouv_email
    mail = property(get_email, set_email, None, "email de l'utilisateur")

    def set_mot_de_passe(self, nouv_mot2passe=None):
        """permet de reset le mot de passe """
        print("Attention le mot de passe de l'utilisateur"
              "{} a été modifié".format(self))
        self.__mot_de_passe = hashlib.new("sha512")
        if nouv_mot2passe is None:
            self.__mot_de_passe.update(
                getpass.getpass("Nouveau mot de passe:").encode("utf-8"))
        else:
            nouv_mot2passe = str(nouv_mot2passe)
            nouv_mot2passe = nouv_mot2passe.encode("utf-8")
            self.__mot_de_passe.update(nouv_mot2passe)

    def get_password(self):
        """ retourne le password sous sa forme encryptée"""
        if type(self.__mot_de_passe) == bytes:
            return self.__mot_de_passe.decode("utf-8")
        else:
            return self.__mot_de_passe.hexdigest()
    password = property(get_password, set_mot_de_passe, None)

    def save(self):
        """
        Utilité
        -------
        Ajoute un objet user à la base de donnée

        Etape 1:
        --------
        vérifier si l'utilisateur n'est pas déjà inscrit dans la base
        de données C-a-d
        Verifier si l'email n'est pas dans la base de données

        Etape 2:
        --------
        Ajouter l'utilisateur dans la base de données

        """
        # Etape 1
        if self.isinsql():
            print("l'utilisateur est déjà dans la base de donnée")
        else:
            # Etape 2
            utilisateur = (self.nom, self.prenom,
                           self.password, self.mail)
            req = """INSERT into users (name, surname, enc_pass, email)
            VALUES(%s, %s, %s, %s)"""
            cursor.execute(req, utilisateur)
            conn.commit()

    def delete_user(self):
        """ supprimer un utilisateur
        initialment conçu comme une surcharge de l'opérateur __del__
        il est préférable de la laisser en fonction non surchargé
        car python supprime les object créer en employant la méthode del
        """
        if self.isinsql():
            req = """
            DELETE FROM users
            WHERE users.email like "{}"
            """.format(self.mail)
            cursor.execute(req)
            conn.commit()
        del self

    def isinsql(self):
        """retourne True si l'utisateur est dans la base sql
        L'existance de l'utilisateur dans la base de données sql est
        basé uniquement sur email de l'utilisateur """
        req = """ SELECT email FROM users
        WHERE users.email like "{}"
        """.format(self.mail)
        cursor.execute(req)
        rows = cursor.fetchall()
        return len(rows) != 0


def load_users():
    """
    Lis la base sql et renvoie la liste des objet python users associés
    """
    req = """
    select name, surname,enc_pass, email
    FROM users
    """
    annuaire = []
    cursor.execute(req)
    rows = cursor.fetchall()
    for (nom, prenom, mot2passe, email) in rows:
        utilisateur = user(nom, prenom, email, mot2passe, True)
        annuaire.append(utilisateur)
    return annuaire


def auth(user_email, user_password):
    """
    Principe
    --------
    L'utilisateur s'authentifie avec son adresse email et son mot de passe
    retourne True si les données fournies sont exacte
    retourne False sinon

    Etape 1
    -------
    Verifier si l'utilisateur est bien dans la base de données
    un utilisateur est doté d'une addresse email unique

    Etape 2
    -------
    Verifier si le mot de passe est bien celui de la base de données


    Remarque: le False ne renvoie pas d'Erreur mais print des logs dans
    la console on peut adapter cette partie en fonction de l'usage de l'API

    """
    encrypted_pass = hashlib.new('sha512')
    encrypted_pass.update(user_password.encode("utf-8"))
    req = """
    select id from users
    where email like "{}"
    """.format(user_email)
    cursor.execute(req)
    rows = cursor.fetchall()
    if len(rows) == 0:
        print("l'utilisateur n'existe pas")
        print("Veuillez vérifier l'addresse mail")
        return False
    elif len(rows) > 1:
        print(" Ambiguïté ")
        print("Il y a plusieurs utlisateurs disposant de cette addresse mails")
        print("Veuillez reporter le problème au responsable informatique")
        return False
    else:
        req = """
        SELECT enc_pass from users
        WHERE id={}
        """.format(rows[0][0])
        cursor.execute(req)
        sql_pass = cursor.fetchone()
        sql_pass = sql_pass[0].decode("utf-8")
        if sql_pass == encrypted_pass.hexdigest():
            print("l'utilisateur est bien authentifié")
            return True
        else:
            print("le mot de passe n'est pas bon")
            return False


def close_conn():
    conn.close()


#pierre = user("Nom", "PIERRE", "yolo@mail", "test")

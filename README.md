Ceci est une API qui a servi d'exercice d'embauche:

Consigne de l'exercice
---
> Faire une API (python ou NodeJS) et [une] base de donné (SQL ou MongoDB) de gestion d'utilisateurs.
> L'API doit permettre de créer un nouvel utilisateur et de pouvoir valider (ou non) des identifiants (mail+mot de passe)/
> Enregistre les mots de passe de manière sécurisée.
> Il faudrait stocker en plus ou deux champs par utilisateur, par example nom et prénoms
> Ne rajoute pas pleins de fonctionnalités, on préfère un truc propre fonctionnel et bien documenté

Structure du projet
---
Forme du Rendu API CLASSIQUE (pas de WEB)
Language utilisé python3.8

Le script python s'appelle mysql_test.py

Les fichiers documentation disponibles sont:
- brouillon.org expliquant quelques choix de conceptions
- server_sql.org (finalisation requise)
- exemples.org (en cours de rédaction)
- installation.org (TODO)
Le fichier sql\_cnf correspond à ma configuration sql et sql\_param est le résultat de la commande mysql --help sur mon PC

Remarques Importantes
---
L'algorithme répond aux exclusivement besoin de l'exercice
Il ne répond pas explicitement aux notions légales tel que la RGPD ou autres.
Comme indiqué dans le programme, seul les mots de passe sont encrypté.
L'algorithme de cryptage utilisé est bien trop faible pour se permettre de mettre ce programme en production à échelle réelle.

Améliorations futures envisageables
-----
Améliorér l'interfaçage (actuellement shell python)
Par exemple introduire une interface web avec un formulaire pour s'incrire 
Même chose pour l'authentification

Plus terre à terre
création d'un fonction à partir d'une addresse email renvoie l'objet python user associé

# Substitutor_foods_website
Site django de recherche de substitut d'aliments.
# Application de recherche de substitut d'aliments
Application qui permet d'obtenir le substitut d'un produit à partir de la recherche effectuée par un utilisateur.  
Les produits de cette application sont des produits téléchargés à partir de l'api d'Open Food Facts.
# Installation de l'application en local
## Téléchager le code source de l'application
Dans la console linux, télechargez le code du projet avec `git clone https://github.com/crispinpigla/subtitutor_foods.git`
Nous appelerons ici `contain_application` le dossier qui contient l'application
## Installer La base de données
### Installer Postgresql
Dans la console linux, installer le système de gestion de base de donnée Postgresql grace à la commande `sudo apt install postgresql`  
S'il vous est demandé d'entrer votre mot de passe, entrez le  
Dans la console linux il est demandé si vous souhaitez continuer. Entrer `o` pour oui  
### Créer l'utilisateur postgresql de l'application
Dans la console linux, entrer la commande `sudo -i -u postgres`  
Dans la console linux, entrer la commande `psql`  
Dans postgresql entrer la commande `CREATE USER substitutor_foods_user WITH CREATEDB;`  
Dans postgresql entrer la commande `CREATE DATABASE substitutor_foods OWNER substitutor_foods_user;`  
Dans postgresql entrer la commande `ALTER USER substitutor_foods_user WITH ENCRYPTED PASSWORD 'substitutor_foods_password';`  
Dans postgresql entrer la commande `\q`  
Dans linux se deconnecter de l'utilisateur postgres en entrant la commande `exit`  
Dans la console linux entrer la commande `sudo chmod o+rwx '/etc/postgresql/[0-9]{2}/main/pg_hba.conf'` (exp: `'/etc/postgresql/14/main/pg_hba.conf'`)
S'il vous est demandé d'entrer votre mot de passe, entrez le  
Ouvrir le fichier `'/etc/postgresql/[0-9]{2}/main/pg_hba.conf'` et chercher la ligne `local   all             postgres                                peer`  
Insérer la ligne `local   all             substitutor_foods_user                                md5` juste après la ligne `local   all             postgres                                peer`  
Enregistrer la modification et fermer le fichier  
Dans la console linux entrez la commande `sudo chmod o-rwx '/etc/postgresql/[0-9]{2}/main/pg_hba.conf'`  
S'il vous est demandé d'entrer votre mot de passe, entrez le  
Dans la console linux redemarrez postgresql en entrant la commande `sudo service postgresql restart`  
S'il vous est demandé d'entrer votre mot de passe, entrez le  
## Installer et activer l'environement virtuelle
Entrer dans la console linux `sudo sudo pip3 install pipenv`  
S'il vous est demandé d'entrer votre mot de passe, entrez le  
## Installer les dépendances
Dans la console linux,, dans l'invite commande, naviguer jusqu'au répertoire du fichier contenant l'application et executer la commande `sudo pipenv install`  
Dans la console, se rendre dans le répertoire du projet ( le répertoire qui contient le fichier `manage.py` )  
Mettre à jour les logiciels du système d'exploitation `sudo apt-get update`  
Installer pip3 `sudo apt-get install python3-pip`  
Installer pipenv `sudo pip3 install pipenv`
Dans la console linux entrez la commande `pipenv install`  
Dans la console linux entrez la commande `pipenv shell`  
## Creation de la base de données
Dans la console linux, entrer `./manage.py migrate`  
Remplir la base de données en entrant dans la console `./manage.py loaddata substitutor/dumps/substitutor.json`  
## Lancer l'application
Dans la console linux,, dans l'invite commande, naviguer jusqu'au répertoire du fichier contenant l'application et executer la commande `./manage.py runserver`  
Ouvrir un navigateur et rendez vous à l'adresse `http://127.0.0.1:8000/` ou `http://localhost:8000/`  
# Désinstaller l'application
## Supprimer la base de données et l'utilisateur de la base de donnée
Dans la console linux, entrer la commande `sudo -i -u postgres`  
Dans la console linux, se connecter à la base de données postgresql grace à la commandee `psql`  
Dans la console postgresql, supprimer la base de données de l'application en entrant la commande `DROP DATABASE IF EXISTS substitutor_foods;`  
Dans la console postgresql, supprimer l'utilisateur de la base de données de l'application en entrant la commande `DROP USER IF EXISTS substitutor_foods_user;`  
Dans postgresql entrer la commande `\q`  
Dans la console linux se deconnecter de l'utilisateur postgres en entrant la commande `exit`  
Dans la console linux supprimer postgresql en entrant la commande `sudo apt-get --purge remove postgresql postgresql-doc postgresql-common`  
Une fenetre 'Configuration de postgresql-12' s'affiche dans la console  
A l'aide de flèches directionnelles sélectionner `oui` et appuyer sur `la touche entrer`  
## Supprimer l'application
Supprimer le fichier contenant l'application ( que nous avons appellé `contain_application`  )
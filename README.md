# Superbowlapp Application Mobile

Prérequis

- 	Visual Studio Code
-  	Extension Python pour VS Code
-  	Git
-  	Python 3.9
-  	MySQL: Le serveur de base de données MySQL doit être en cours d'exécution. AivenCloud
- 	MongoDB

1. Installation et déploiement

Lancez VSCode et installez l’extension « Python » publiée par Microsoft. Après avoir créé le dossier 'superbowlapp'. Ouvrez un terminal intégré dans VS Code pour faire le clonage du dépôt et exécuter les commandes suivantes :

  	« git clone https://github.com/VitorPinto1/superbowlapp.git »
  	« cd superbowlapp »
   
2. Configuration de l'environnement

Activez l'environnement virtuel Python dans le terminal :

  	« source env/bin/activate »  # Sur Unix ou MacOS
  	« env\Scripts\activate »    # Sur Windows

Si l'environnement virtuel n'existe pas encore, vous pouvez le créer avec :

  	« python -m venv env » 

3. Installer les dépendances

Installez les paquets nécessaires à partir du fichier requirements.txt si disponible.

  	« pip install -r requirements.txt »

4. Lancement de l’application

Exécutez l’application  dans le teminal :

  	« python main.py »

5. Accéder à l’application

En suivant ces étapes, vous devriez être en mesure de déployer l'application mobile localement et tester ses fonctionnalités.


Information des archives 

Dossier ecrans:
Contient les fichiers Python (.py) pour les différents écrans de l'application. Chaque fichier dans ce dossier définit la logique et les interactions spécifiques pour un écran particulier de l'application.
- login_screen.py : Gestion de la logique pour l'écran de connexion.
- welcome_screen.py : Gestion de la logique pour l'écran d'accueil.
- pari_detail_screen.py : Gestion de la logique pour l'écran des détails des paris.
- notifications.py : Gestion des notifications

Dossier outils:
Contient des utilitaires et outils utilisés par l'application.
- db_manager.py: Gestion des interactions avec la base de données. Ce fichier fournit des services pour la connexion à la base de données, la 		 récupération des données des utilisateurs, la vérification des mots de passe et la gestion des paris.
- mongo_outils.py: Gestion des interactions avec la base de données NoSQL MongoDB

Fichier ecrans.kv: Définit les styles et la disposition visuelle des différents écrans de l'application.

Fichier main.py: Point de départ de l'application. Ce fichier initialise l'application, charge la disposition définie dans ecrans.kv, et configure le ScreenManager pour gérer la navigation entre les différents écrans. Configuration des variables d'environnement pour la base de données. Initialisation et affichage de l'interface utilisateur.


Déploiement avec Docker

Prérequis :

- Docker Desktop installé

Lancer l'application avec Docker Compose

	« docker-compose up »

Construction manuelle 
Construire et lancer sans docker-compose :

	«	docker build -t vitorpinto500/apppython:latest .
		docker run -it --rm -e DISPLAY=host.docker.internal:0 -v /tmp/.X11-unix:/tmp/.X11-unix vitorpinto500/apppython:latest

CI/CD à chaque git push sur main :

- L'image Docker est automatiquement construite avec GitHub Actions

- L'image est poussée sur DockerHub sous : vitorpinto500/apppython:latest

Auteur

Projet réalisé par Vitor Pinto Passionné par le développement et l'IA.
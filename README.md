# Superbowlapp Application Mobile

Prérequis

- 	Visual Studio Code
-  	Extension Python pour VS Code
-  	Git
-  	Python 3.9
-  	MySQL: Le serveur de base de données MySQL doit être en cours d'exécution. AivenCloud

1.  	Installation et déploiement

Lancez VSCode et installez l’extension « Python » publiée par Microsoft. Après avoir créé le dossier 'superbowlapp'. Ouvrez un terminal intégré dans VS Code pour faire le clonage du dépôt et exécuter les commandes suivantes :

  	« git clone https://github.com/VitorPinto1/superbowlapp.git »
  	« cd superbowlapp »
   

2.  	Configuration de l'environnement

Activez l'environnement virtuel Python dans le terminal :

  	« source env/bin/activate »  # Sur Unix ou MacOS
  	« env\Scripts\activate »    # Sur Windows

Si l'environnement virtuel n'existe pas encore, vous pouvez le créer avec :

  	« python -m venv env » 

3.  	Installer les dépendances

Installez les paquets nécessaires à partir du fichier requirements.txt si disponible.

  	« pip install -r requirements.txt »

4.  	Lancement de l’application

Exécutez l’application  dans le teminal :

  	« python main.py »

5.  	Accéder à l’application

Conclusion

En suivant ces étapes, vous devriez être en mesure de déployer l'application mobile localement et tester ses fonctionnalités.

import mysql.connector
from werkzeug.security import check_password_hash
import os
from dotenv import load_dotenv

load_dotenv()
db_host = os.environ.get('DB_HOST')
db_user = os.environ.get('DB_USER')
db_password = os.environ.get('DB_PASSWORD')
db_name = os.environ.get('DB_NAME')
db_port = os.environ.get('DB_PORT')

class DatabaseService:
    # Méthode pour obtenir les informations d'un utilisateur en fonction de son email
    def get_user_by_email(self, email):
        try:
            conn = mysql.connector.connect(
                host=db_host, 
                user=db_user, 
                password=db_password, 
                database=db_name, 
                port=db_port
            )
            cursor = conn.cursor()
            query = "SELECT * FROM users WHERE email = %s"
            cursor.execute(query, (email,))
            user = cursor.fetchone()
            cursor.close()
            conn.close()
            return user
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None
        
    # Méthode pour vérifier si le mot de passe fourni correspond au hash stocké
    def check_password(self, stored_password_hash, provided_password):
        return check_password_hash(stored_password_hash, provided_password)

    # Méthode pour obtenir les paris de l'utilisateur en fonction de son ID
    def get_user_bets(self, user_id):
        try:
            conn = mysql.connector.connect(
                host=db_host, 
                user=db_user, 
                password=db_password, 
                database=db_name, 
                port=db_port
            )
            cursor = conn.cursor()
            query = """
                SELECT matchs.id, matchs.equipe1, matchs.equipe2, matchs.jour, matchs.debut, 
                matchs.fin, matchs.score, matchs.statut, mises.mise1, mises.mise2, mises.resultat1, mises.resultat2, mises.equipe1, mises.equipe2, matchs.vainqueur, matchs.commentaires
                FROM mises
                JOIN matchs ON mises.id_match = matchs.id
                WHERE mises.id_utilisateur = %s
            """
            cursor.execute(query, (user_id,))
            bets = cursor.fetchall()
            cursor.close()
            conn.close()
            return bets
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []

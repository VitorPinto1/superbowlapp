import mysql.connector
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

def sync_stats_to_mongo():
    # Connexion MySQL
    mysql_conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME")
    )
    cursor = mysql_conn.cursor(dictionary=True)

    # Connexion MongoDB
    mongo_uri = os.getenv("MONGO_URI")
    mongo_client = MongoClient(mongo_uri)
    mongo_db = mongo_client["records"]
    collection = mongo_db["mises_stats"]

    # Requête MySQL avec vainqueur
    cursor.execute("""
        SELECT 
            u.id AS utilisateur_id, u.nom, u.prenom,
            m.id AS match_id, m.equipe1, m.equipe2, m.score, m.vainqueur,
            mi.mise1, mi.mise2, mi.cote1, mi.cote2
        FROM mises mi
        JOIN users u ON mi.id_utilisateur = u.id
        JOIN matchs m ON mi.id_match = m.id
        WHERE m.vainqueur IS NOT NULL
    """)

    rows = cursor.fetchall()
    stats_par_user = {}

    for row in rows:
        uid = row["utilisateur_id"]
        mise1 = row.get("mise1")
        mise2 = row.get("mise2")
        vainqueur = row.get("vainqueur")
        equipe1 = row["equipe1"]
        equipe2 = row["equipe2"]

        # Cas sans mise
        if not mise1 and not mise2:
            mise_sur = None
            cote = None
            mise = 0
            gagne = False
            montant_resultat = 0
        else:
            mise_sur = equipe1 if (mise1 or 0) > 0 else equipe2
            cote = row["cote1"] if (mise1 or 0) > 0 else row["cote2"]
            mise = mise1 if (mise1 or 0) > 0 else mise2
            # Détermination du gain selon le vainqueur
            gagne = vainqueur and vainqueur == mise_sur
            montant_resultat = round(mise * cote, 2) if gagne else -mise

        if uid not in stats_par_user:
            stats_par_user[uid] = {
                "utilisateur_id": uid,
                "nom": row["nom"],
                "prenom": row["prenom"],
                "mises": [],
                "total_gagne": 0
            }

        stats_par_user[uid]["mises"].append({
            "equipe1": equipe1,
            "equipe2": equipe2,
            "score_final": row["score"],
            "vainqueur": vainqueur,
            "mise_sur": mise_sur,
            "montant_mise": float(mise),
            "cote": cote,
            "gagne": gagne,
            "montant_resultat": float(montant_resultat)
        })

        stats_par_user[uid]["total_gagne"] += montant_resultat

    for doc in stats_par_user.values():
        doc["total_gagne"] = float(round(doc["total_gagne"], 2))
        collection.update_one(
            {"utilisateur_id": doc["utilisateur_id"]},
            {"$set": doc},
            upsert=True
        )

    

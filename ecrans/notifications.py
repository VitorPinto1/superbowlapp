from kivy.uix.screenmanager import Screen
from kivymd.uix.list import TwoLineListItem, ThreeLineListItem
from pymongo import MongoClient
import os
from kivy.properties import NumericProperty

class NotificationsEcran(Screen):
    user_id = None

    def on_pre_enter(self):
        print("USER ID:", self.user_id)  
        self.afficher_stats_utilisateur()

    def afficher_stats_utilisateur(self):
        mongo_uri = os.getenv("MONGO_URI")
        client = MongoClient(mongo_uri)
        db = client["records"]
        stats = db["mises_stats"].find_one({"utilisateur_id": self.user_id})
        
        self.ids.stats_list.clear_widgets()

        if stats:
            for mise in stats.get('mises', []):
                ligne1 = mise['equipe1']
                ligne2 = mise['equipe2']
                ligne3 = f"Score: {mise['score_final']} | " + (
                    f"Gagné: {mise['montant_resultat']}€" if mise['gagne'] else f"Perdu: {mise['montant_resultat']}€"
                )
                
                item = ThreeLineListItem(text=ligne1, secondary_text=ligne2, tertiary_text=ligne3 )
                item._no_ripple_effect = True  

                self.ids.stats_list.add_widget(item)
        else:
            pass

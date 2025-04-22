from kivy.uix.screenmanager import Screen
from kivymd.uix.list import ThreeLineListItem
from kivy.clock import Clock
from outils.db_manager import DatabaseService
from outils.mongo_outils import sync_stats_to_mongo
from pymongo import MongoClient

import os

class WelcomeEcran(Screen):
    user_id = None  
    
    # Méthode appelée juste avant que l'écran ne devienne visible
    def on_pre_enter(self, *args):
        self.notifications_lues = True
        # Charger le nombre de mises actuel depuis Mongo
        mongo_uri = os.getenv("MONGO_URI")
        client = MongoClient(mongo_uri)
        db = client["records"]
        stats = db["mises_stats"].find_one({"utilisateur_id": self.user_id})
        self.last_nb_mises = len(stats.get("mises", [])) if stats else 0

        self.update_bets()
        self.sync_stats_and_check()
    
        Clock.schedule_interval(lambda dt: self.update_bets(), 30)
        Clock.schedule_interval(lambda dt: self.sync_stats_and_check(), 30)

    # Méthode pour mettre à jour la liste des paris
    def update_bets(self):
        self.ids.bets_list.clear_widgets()
        db_service = DatabaseService()
        user_bets = db_service.get_user_bets(self.user_id)
        
        for bet in user_bets:
            bet_info = {
                'equipe1': bet[1],
                'equipe2': bet[2],
                'debut': bet[4],
                'fin': bet[5],
                'mise1': bet[8],
                'mise2': bet[9],
                'resultat1': bet[10],
                'resultat2': bet[11],
                'equipemise1': bet[12],
                'equipemise2': bet[13],
                'vainqueur': bet[14],
                'score': bet[6],
                'commentaires': bet[15]
            }

            line_one = f"{bet[1]} vs {bet[2]}"
            line_two = f"Date: {bet[3]}, Debut: {bet[4]}, Fin: {bet[5]}"
            line_three = f"Score: {bet[6] if bet[6] is not None else '-'} , Statut: {bet[7]}, Vainqueur: {bet[14]}"

            if bet[7] == "En cours":
                list_item = ThreeLineListItem(
                    text=line_one,
                    secondary_text=line_two,
                    tertiary_text=line_three,
                    on_release=lambda x, bet_info=bet_info: self.open_bet_details(bet_info)
                )
            else:
                list_item = ThreeLineListItem(
                    text=line_one,
                    secondary_text=line_two,
                    tertiary_text=line_three,
                    theme_text_color='Secondary',
                    on_release=lambda x, bet_info=bet_info: self.open_bet_details(bet_info)
                )

            self.ids.bets_list.add_widget(list_item)

    # Méthode pour ouvrir les détails d'un pari spécifique
    def open_bet_details(self, bet_info):
        bet_detail_screen = self.manager.get_screen('pari_detail')
        bet_detail_screen.bet_data = bet_info
        
        couleur_resultat1 = '33ff33' if bet_info.get('vainqueur') == bet_info.get('equipemise1') else 'ff3333'
        couleur_resultat2 = '33ff33' if bet_info.get('vainqueur') == bet_info.get('equipemise2') else 'ff3333'

        statut1 = "Gagné" if couleur_resultat1 == '33ff33' else "Perdu"
        statut2 = "Gagné" if couleur_resultat2 == '33ff33' else "Perdu"
    
        details = [
            f"{bet_info['equipe1']} VS {bet_info['equipe2']}",
            f"Debut: {bet_info['debut']}",
            f"Fin: {bet_info['fin']}",
            f"Mise {bet_info['equipemise1']}: {str(int(bet_info['mise1']))}" if bet_info['mise1'] is not None else "",
            f"Mise {bet_info['equipemise2']}: {str(int(bet_info['mise2']))}" if bet_info['mise2'] is not None else "",
            f"[color={couleur_resultat1}]Resultat : {str(int(bet_info['mise1'])) if couleur_resultat1 == 'ff3333' else str(bet_info['resultat1'])}  ({statut1})[/color]" if bet_info.get('resultat1') is not None and bet_info.get('vainqueur') != '-' else "",
            f"[color={couleur_resultat2}]Resultat : {str(int(bet_info['mise2'])) if couleur_resultat2 == 'ff3333' else str(bet_info['resultat2'])}  ({statut2})[/color]" if bet_info.get('resultat2') is not None and bet_info.get('vainqueur') != '-' else "",
            f"Score: {bet_info['score']}" if bet_info['score'] is not None else "",
            f"Commentaires: {bet_info['commentaires']}" if bet_info['commentaires'] != ' - ' else "",
            f"Vainqueur: {bet_info['vainqueur']}" if bet_info['vainqueur'] != '-' else ""
        ]

        detail_text = "\n".join(filter(None, details))
        bet_detail_screen.ids.detail_label.markup = True
        bet_detail_screen.ids.detail_label.text = detail_text
        bet_detail_screen.user_id = self.user_id  
        self.manager.current = 'pari_detail'
    
    def sync_stats_and_check(self):
        sync_stats_to_mongo()
        mongo_uri = os.getenv("MONGO_URI")
        client = MongoClient(mongo_uri)
        db = client["records"]
        collection = db["mises_stats"]
        stats = collection.find_one({"utilisateur_id": self.user_id})

        if stats:
            nb_mises = len(stats.get("mises", []))
            icon = self.ids.notification_button
            if nb_mises > self.last_nb_mises:
                if self.notifications_lues:
                    icon.icon = "bell-badge-outline"
                    icon.text_color = (1, 0, 0, 1)
                    self.notifications_lues = False  
                else:
                    pass
            else:
                if self.notifications_lues:
                    icon.icon = "bell-outline"
                    icon.text_color = (1, 1, 1, 1)
                else:
                    icon.icon = "bell-badge-outline"
                    icon.text_color = (1, 0, 0, 1)

            # 🔁 mettre à jour seulement après comparaison
            self.last_nb_mises = nb_mises

    def open_notifications(self, *args):         
        notif_screen = self.manager.get_screen('notifications')
        notif_screen.user_id = self.user_id 
        self.notifications_lues = True
        self.manager.current = 'notifications'
        Clock.schedule_once(lambda dt: notif_screen.afficher_stats_utilisateur(self.user_id), 0)
        icon = self.ids.notification_button
  
        mongo_uri = os.getenv("MONGO_URI")
        client = MongoClient(mongo_uri)
        db = client["records"]
        collection = db["mises_stats"]
        stats = collection.find_one({"utilisateur_id": self.user_id})
        stats = db["mises_stats"].find_one({"utilisateur_id": self.user_id})
        if stats:
            self.last_nb_mises = len(stats.get("mises", []))

    # Méthode appelée lorsque l'écran n'est plus visible
    def on_leave(self, *args):
        # Annule la mise à jour périodique des paris
        Clock.unschedule(self.update_bets)
        Clock.unschedule(self.sync_stats_and_check)
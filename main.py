from kivy.core.window import Window
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from ecrans import LoginEcran, WelcomeEcran, PariDetailEcran

import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()
db_host = os.environ.get('DB_HOST')
db_user = os.environ.get('DB_USER')
db_password = os.environ.get('DB_PASSWORD')
db_name = os.environ.get('DB_NAME')
db_port = os.environ.get('DB_PORT')

Window.size = (360, 640)

class MyApp(MDApp):
    def build(self):
        # Charger le fichier KV 
        Builder.load_file('ecrans.kv')
        # Créer un ScreenManager pour gérer les différentes écrans
        self.screen_manager = ScreenManager()
        self.screen_manager.add_widget(LoginEcran(name='login'))
        self.screen_manager.add_widget(WelcomeEcran(name='welcome'))
        self.screen_manager.add_widget(PariDetailEcran(name='pari_detail'))
        return self.screen_manager
    
    def on_start(self):
        Window.orientation = 'portrait'
    
    # Méthode pour afficher des boîtes de dialogue d'erreur depuis n'importe quel écran
    def show_error_dialog(self, message):
        self.screen_manager.current_screen.show_error_dialog(message)

    # Méthode pour changer l'écran actuel à l'écran de connexion
    def go_to_login(self):
        self.screen_manager.current = 'login'
    # Méthode pour changer l'écran actuel à l'écran d'accueil
    def go_to_welcome(self):
        self.screen_manager.current = 'welcome'

if __name__ == '__main__':
    MyApp().run()

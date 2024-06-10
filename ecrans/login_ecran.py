from kivy.uix.screenmanager import Screen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from outils.db_manager import DatabaseService

class LoginEcran(Screen):
    # Cette méthode est appelée lorsqu'un utilisateur tente de se connecter.
    def login(self):
        username = self.ids.username_field.text
        password = self.ids.password_field.text

        if not username or not password:
            self.show_error_dialog("Veuillez saisir l'adresse e-mail et le mot de passe")
            return
              
        # Crée une instance du service de base de données pour interagir avec la base de données.
        db_service = DatabaseService()
        user = db_service.get_user_by_email(username)
        
        if user:
            if db_service.check_password(user[4], password):
                welcome_screen = self.manager.get_screen('welcome')
                welcome_screen.user_id = user[0] # Associe l'ID de l'utilisateur à l'écran de bienvenue.
                self.manager.current = 'welcome'
            else:
                self.show_error_dialog("Le mot de passe est incorrect")
        else:
            self.show_error_dialog("L'utilisateur n'a pas été trouvé.")

    def show_error_dialog(self, message):
        # affichage d'error et fermeture
        ok_button = MDFlatButton(
            text="OK",
            on_release=lambda x: self.dialog.dismiss()
        )
        if hasattr(self, 'dialog'):
            self.dialog.text = message
            self.dialog.buttons = [ok_button]
        else:
            self.dialog = MDDialog(
                text=message,
                buttons=[ok_button]
            )
        self.dialog.open()

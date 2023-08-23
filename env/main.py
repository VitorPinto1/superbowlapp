from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
import mysql.connector

# Design
KV = '''
ScreenManager:
    LoginScreen:
    WelcomeScreen:

<LoginScreen>:
    name: 'login'
    
    BoxLayout:
        orientation: 'vertical'
        spacing: '10dp'
        padding: '20dp'
        
        MDLabel:
            text: 'Login'
            theme_text_color: 'Primary'
            font_style: 'H4'
            
        MDTextField:
            id: username_field
            hint_text: 'Email'
            required: True
            
        MDTextField:
            id: password_field
            hint_text: 'Mot de passe'
            required: True
            password: True
            
        MDRaisedButton:
            text: 'Se connecter'
            on_release: app.login()

<WelcomeScreen>:
    name: 'welcome'
    
    BoxLayout:
        orientation: 'vertical'
        
        MDLabel:
            id: bet_teams_label
            text: ''
            theme_text_color: 'Primary'
            font_style: 'H4'
        
        MDRaisedButton:
            text: 'Retourner au login'
            on_release: app.go_to_login()

'''

class LoginScreen(Screen):
    pass


class WelcomeScreen(Screen):
    def on_pre_enter(self):
        # Obtener el ID de usuario desde el inicio de sesión
        login_screen = self.manager.get_screen('login')
       

        try:
            # Establecer conexión a la base de datos MySQL
            conn = mysql.connector.connect(
                host='localhost',
                user='PEPE',
                password='PEPE',
                database='bdsuperbowl'
            )

            cursor = conn.cursor()
            query = """
                SELECT matchs.equipe1, matchs.equipe2, matchs.jour, matchs.debut, matchs.fin,
                CASE WHEN matchs.statut = 'Terminé' THEN matchs.score ELSE '  ' END AS score
                FROM mises
                JOIN matchs ON mises.id_match = matchs.id
                WHERE mises.id_utilisateur = %s
            """

            cursor.execute(query, (self.user_id,))
            user_bets = cursor.fetchall()

            cursor.close()
            conn.close()

            # Mostrar los nombres de los equipos en la pantalla
            bet_teams = '\n'.join([f"{row[0]} vs {row[1]} - Date: {row[2]}, Debut: {row[3]}, Fin: {row[4]} {row[5]} " for row in user_bets])
            self.ids.bet_teams_label.text = f"Mises:\n{bet_teams}"

        except mysql.connector.Error as err:
            print(f"Error: {err}")


class MyApp(MDApp):
    def build(self):
        """
        self.screen_manager = ScreenManager()
        self.screen_manager.add_widget(LoginScreen(name='login'))
        self.screen_manager.add_widget(WelcomeScreen(name='welcome'))
        self.screen_manager.current = 'login'
        return self.screen_manager
        """
        self.screen_manager = Builder.load_string(KV)
        return self.screen_manager
      
    def login(self):
        login_screen = self.screen_manager.get_screen('login')
        username = login_screen.ids.username_field.text
        password = login_screen.ids.password_field.text
        
        try:
            # Establecer conexión a la base de datos MySQL
            conn = mysql.connector.connect(
                host='localhost',
                user='PEPE',
                password='PEPE',
                database='bdsuperbowl'
            )
            
            cursor = conn.cursor()
            query = "SELECT * FROM users WHERE email = %s AND mot_de_passe = %s"
            cursor.execute(query, (username, password))
            user = cursor.fetchone()
            
            if user:
                welcome_screen = self.screen_manager.get_screen('welcome')
                welcome_screen.user_id = user[0]
                self.screen_manager.current = 'welcome'
            else:
                self.screen_manager.current = 'login'
            
            cursor.close()
            conn.close()
            
        except mysql.connector.Error as err:
            print(f"Error: {err}")
    
  

    def go_to_login(self):
        self.screen_manager.current = 'login'

if __name__ == '__main__':
    MyApp().run()